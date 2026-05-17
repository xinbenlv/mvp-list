"""CLI entrypoint — wires intake / backend / concepts / composer end-to-end.

Phase 1b + 2 wiring: real Anthropic client (from .env) drives the intake
orchestrator; mock backend reads poc-demo/demo_places.json; rule-based
concept generator produces 2-3 distinct Concepts; the Phase 0 Composer
stub still runs for the compose step (Phase 3a will replace it with a real
LLM-backed PlanComposer).

Usage:
    # Real intake + stub composer (requires ANTHROPIC_API_KEY in .env):
    python -m agent.main < tests/fixtures/mia_first_turn.txt

    # All-stub flow (no API key needed) — pass --mock-intake:
    python -m agent.main --mock-intake < tests/fixtures/mia_first_turn.txt

The --mock-intake flag short-circuits the Anthropic client and skips the
intake loop, instead loading a default persona (Mia) as the starting
IntakeState. Useful for: smoke tests in CI, demos when API is flaky, and
running through Phase 2+ without burning tokens on intake.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from agent.compose.composer import PlanComposer
from agent.compose.concepts import generate_concepts_simple
from agent.intake.orchestrator import InitialInput, IntakeOrchestrator
from agent.present.format import format_proposals
from agent.state import (
    EnergyProfile,
    IntakeState,
    Slot,
    TasteSignatureSlot,
    _ScalarSlot,
    serialize_to_experience_request,
)
from agent.tools.backend import BackendClient
from agent.types import (
    ChaosTolerance,
    EmotionalRole,
    EnergyLevel,
    NoveltyLevel,
    PlanResult,
    TasteSignature,
    VibeTag,
    VibeWeight,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv() -> None:
    """Load .env from repo root if present; tolerate missing python-dotenv."""
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
    except ImportError:
        # Fallback: parse minimal KEY=VAL ourselves
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def _make_anthropic_client() -> object:
    """Build a real AsyncAnthropic client; raise if API key missing."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key or "PASTE" in api_key or api_key == "sk-ant-...":
        raise SystemExit(
            "ANTHROPIC_API_KEY not set or placeholder. "
            "Add your key to .env or run with --mock-intake."
        )
    from anthropic import AsyncAnthropic

    return AsyncAnthropic(api_key=api_key)


def _load_mock_state_from_persona(persona_id: str = "mia") -> IntakeState:
    """Load a persona JSON and produce a usable IntakeState for stub runs.

    This is a CLI shortcut for --mock-intake mode; the real flow goes through
    IntakeOrchestrator. Persona JSON has a flat schema (per its _meta note),
    so we only populate the fields the downstream pipeline actually reads.
    """
    persona_file = REPO_ROOT / "poc-demo" / f"{persona_id}_persona.json"
    if not persona_file.exists():
        # Fall back: empty state — downstream will use uniform ranking.
        return IntakeState()
    raw = json.loads(persona_file.read_text())

    # Build a TasteSignatureSlot from the persona's taste_signature.vibe_weights.
    ts_block = raw.get("taste_signature", {})
    vw_raw = ts_block.get("vibe_weights", [])
    # Filter to controlled VibeTag vocab — persona JSON uses some extended tags
    # (e.g., "restorative", "natural_light") that aren't in the strict enum.
    # Composer side reads loose strings via ComposerVibeWeight; here we only
    # populate the typed taste_signature with vocab-controlled tags.
    valid_tags = {tag.value for tag in VibeTag}
    vibe_weights = [
        VibeWeight(tag=VibeTag(item["tag"]), weight=float(item["weight"]))
        for item in vw_raw
        if item.get("tag") in valid_tags and "weight" in item
    ]
    taste_signature = TasteSignature(
        vibe_weights=vibe_weights,
        summary=ts_block.get("summary", ""),
        confidence=0.9,
    )

    # Pull emotional_intent (flat-schema persona JSON nests it as `intake_state`)
    ei_raw = raw.get("intake_state", {})
    ei_values = [
        EmotionalRole(v) for v in ei_raw.get("values", []) if v in {e.value for e in EmotionalRole}
    ]

    # Pull energy_profile
    ep_raw = raw.get("energy_profile", {})
    energy_profile = EnergyProfile()
    if ep_raw.get("energy_level") in {e.value for e in EnergyLevel}:
        energy_profile = energy_profile.model_copy(
            update={
                "energy_level": _ScalarSlot[EnergyLevel](
                    value=EnergyLevel(ep_raw["energy_level"]), confidence=0.9
                )
            }
        )
    if ep_raw.get("chaos_tolerance") in {c.value for c in ChaosTolerance}:
        energy_profile = energy_profile.model_copy(
            update={
                "chaos_tolerance": _ScalarSlot[ChaosTolerance](
                    value=ChaosTolerance(ep_raw["chaos_tolerance"]), confidence=0.9
                )
            }
        )
    if ep_raw.get("novelty_appetite") in {n.value for n in NoveltyLevel}:
        energy_profile = energy_profile.model_copy(
            update={
                "novelty_appetite": _ScalarSlot[NoveltyLevel](
                    value=NoveltyLevel(ep_raw["novelty_appetite"]), confidence=0.9
                )
            }
        )

    state = IntakeState()
    state = state.model_copy(
        update={
            "taste_signature": TasteSignatureSlot(
                value=taste_signature,
                confidence=0.9,
                provenance="inferred_from_screenshots",
            ),
            "emotional_intent": Slot[EmotionalRole](
                values=ei_values,
                confidence=ei_raw.get("confidence", 0.9),
                provenance="user_stated",
            ),
            "emotional_intent_rationale": ei_raw.get("rationale", ""),
            "energy_profile": energy_profile,
        }
    )
    return state


async def run_once(initial_text: str, *, mock_intake: bool = False) -> str:
    """End-to-end pipeline. Returns the final ProposalSet markdown.

    With API key in .env: real intake (when not mock_intake) + real Composer.
    With --mock-intake AND no key: stub Composer (Phase 0-style placeholder).
    With --mock-intake AND key present: stub intake (Mia persona) + REAL Composer.
    """

    # Resolve client once. If missing, run in stub mode for the Composer too.
    anthropic_client: object | None = None
    try:
        anthropic_client = _make_anthropic_client()
    except SystemExit:
        if not mock_intake:
            raise  # live intake requires a key
        # Mock-intake without key → Composer also runs in stub mode

    if mock_intake:
        state = _load_mock_state_from_persona("mia")
    else:
        assert anthropic_client is not None  # guaranteed by branch above
        orchestrator = IntakeOrchestrator(anthropic_client=anthropic_client)
        state = await orchestrator.run(InitialInput(text=initial_text, images=[]))

    backend = BackendClient()
    request = serialize_to_experience_request(state)
    candidates = await backend.search_places(request)

    concepts = generate_concepts_simple(state, candidates)

    composer = PlanComposer(anthropic_client=anthropic_client)
    plans: list[PlanResult] = await asyncio.gather(
        *(composer.run(c, candidates, state) for c in concepts)
    )

    intake_summary = f'你说: "{initial_text.strip()[:60]}"'
    if mock_intake:
        intake_summary += " — mock-intake run (Mia persona)."
    return format_proposals(plans, intake_summary)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Day Composer POC — runs intake → backend → concepts → compose"
    )
    parser.add_argument(
        "--mock-intake",
        action="store_true",
        help="Skip live intake; use Mia persona as default IntakeState",
    )
    args = parser.parse_args()

    _load_dotenv()
    initial_text = sys.stdin.read()
    markdown = asyncio.run(run_once(initial_text, mock_intake=args.mock_intake))
    sys.stdout.write(markdown)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
