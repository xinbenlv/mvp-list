"""vision_extract_taste — Sonnet 4.6 + vision call (Phase 1b).

Loads 1–10 user screenshots, asks Claude Sonnet to extract a `TasteSignature`
(weighted vibe vector), retries once with a stricter prompt on bad output,
returns an empty TasteSignature + warning if both attempts fail.

The Anthropic client is **injected** so the Phase 1b tests can pass in a fake
that returns scripted responses (no network calls, no cassettes needed). The
real path is documented in `agent/intake/orchestrator.py`.
"""

from __future__ import annotations

import base64
import json
import logging
import re
from pathlib import Path
from typing import Any, Protocol

from agent.types import TasteSignature, VibeTag, VibeWeight

logger = logging.getLogger(__name__)

VISION_MODEL = "claude-sonnet-4-5-20250929"
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "vision.md"

# Be permissive on file extensions; map to Anthropic-accepted media types.
_MEDIA_TYPES: dict[str, str] = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


class _AnthropicLike(Protocol):
    """Structural typing — accepts the real AsyncAnthropic OR a test fake.

    We only call `.messages.create(...)`, so anything that exposes that
    coroutine satisfies us.
    """

    messages: Any  # has async `create(...)` returning an obj with `.content`


def _load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _encode_image(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    media_type = _MEDIA_TYPES.get(p.suffix.lower(), "image/png")
    data = base64.standard_b64encode(p.read_bytes()).decode("ascii")
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media_type, "data": data},
    }


def _extract_text(response: Any) -> str:
    """Pull the first text block out of a Messages API response.

    Tolerates the SDK shape (response.content = list[ContentBlock]) and the
    test-fake shape (a dict with `content` = list of dicts).
    """
    content = getattr(response, "content", None)
    if content is None and isinstance(response, dict):
        content = response.get("content")
    if not content:
        return ""
    for block in content:
        text = getattr(block, "text", None)
        if text is None and isinstance(block, dict):
            text = block.get("text")
        if isinstance(text, str) and text.strip():
            return text
    return ""


def _parse_taste_json(raw: str) -> TasteSignature | None:
    """Parse the JSON envelope the prompt asks for; tolerate code fences."""
    text = raw.strip()
    # Strip ```json ... ``` if the model wrapped despite instructions.
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    # Else find the first {...} blob.
    elif not text.startswith("{"):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None

    vibe_weights_raw = payload.get("vibe_weights", [])
    if not isinstance(vibe_weights_raw, list):
        return None
    weights: list[VibeWeight] = []
    for entry in vibe_weights_raw:
        if not isinstance(entry, dict):
            continue
        tag = entry.get("tag")
        weight = entry.get("weight")
        if not isinstance(tag, str) or not isinstance(weight, int | float):
            continue
        # TasteSignature.vibe_weights is typed as VibeTag; coerce the model's
        # free string to the controlled StrEnum, skipping tags outside the
        # vocab. Out-of-vocab tags (e.g. "restorative", "natural_light" that
        # personas carry) are not lost downstream — the Composer reads loose
        # strings via ComposerVibeWeight in state.serialize_for_composer.
        try:
            vibe_tag = VibeTag(tag)
        except ValueError:
            continue
        try:
            weights.append(
                VibeWeight(tag=vibe_tag, weight=max(0.0, min(1.0, float(weight))))
            )
        except Exception:
            continue

    summary = str(payload.get("summary", ""))
    confidence = float(payload.get("confidence", 0.0))
    confidence = max(0.0, min(1.0, confidence))
    return TasteSignature(vibe_weights=weights, summary=summary, confidence=confidence)


async def _call_vision(
    client: _AnthropicLike,
    image_blocks: list[dict[str, Any]],
    system_prompt: str,
    stricter_suffix: str = "",
) -> str:
    system = system_prompt
    if stricter_suffix:
        system = system + "\n\n" + stricter_suffix
    response = await client.messages.create(
        model=VISION_MODEL,
        max_tokens=1024,
        system=system,
        messages=[
            {
                "role": "user",
                "content": [
                    *image_blocks,
                    {
                        "type": "text",
                        "text": (
                            "Extract the TasteSignature. Return ONLY the JSON object "
                            "described in the system prompt."
                        ),
                    },
                ],
            }
        ],
    )
    return _extract_text(response)


async def vision_extract_taste(
    image_paths: list[str],
    anthropic_client: _AnthropicLike,
) -> TasteSignature:
    """Sonnet 4.6 + vision: image paths -> TasteSignature.

    Empty / missing paths return a zero-confidence empty TasteSignature
    cleanly so the orchestrator can skip the vision step without branching.
    """
    if not image_paths:
        return TasteSignature()

    image_blocks = [_encode_image(p) for p in image_paths]
    system_prompt = _load_prompt()

    # Attempt 1
    raw = await _call_vision(client=anthropic_client, image_blocks=image_blocks,
                             system_prompt=system_prompt)
    parsed = _parse_taste_json(raw)
    if parsed is not None:
        return parsed

    # Attempt 2 — stricter
    logger.warning("vision_extract_taste: bad output on attempt 1, retrying with strict prompt")
    stricter = (
        "REPLY WITH JSON ONLY. No prose, no Markdown fences. The very first "
        "character of your reply must be `{` and the last must be `}`."
    )
    raw2 = await _call_vision(client=anthropic_client, image_blocks=image_blocks,
                              system_prompt=system_prompt, stricter_suffix=stricter)
    parsed2 = _parse_taste_json(raw2)
    if parsed2 is not None:
        return parsed2

    logger.warning(
        "vision_extract_taste: bad output after retry, returning empty TasteSignature"
    )
    return TasteSignature()


__all__ = ["vision_extract_taste"]
