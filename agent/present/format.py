"""format_proposals — pure template that wraps N PlanResults into one bundle.

Phase 3b: emits a real ProposalSet markdown with:
  - Title header "你的周六，{N} 种走法" (N-aware)
  - Intake summary header
  - Comparison table (one row per plan, columns: Theme / Pitch /
    First stop / Vibe)
  - Each PlanResult.markdown rendered verbatim, separated by `---`

No LLM, no I/O — this is the deterministic "stitch the plans together"
step the Composer pipeline ends with.
"""

from __future__ import annotations

from agent.types import PlanResult


def _vibe_text(plan: PlanResult) -> str:
    """Comma-joined mood tags, falling back to theme_anchor label."""
    if plan.mood_tags:
        return ", ".join(plan.mood_tags)
    return plan.theme_anchor.value


def _first_stop_name(plan: PlanResult) -> str:
    """Display name for the first stop; fall back to place_id, then placeholder."""
    if plan.stop_names:
        name = plan.stop_names[0].strip()
        if name:
            return name
    if plan.stop_place_ids:
        pid = plan.stop_place_ids[0].strip()
        if pid:
            return pid
    return "未指定"


def _escape_cell(text: str) -> str:
    """Make a string safe for a markdown table cell.

    Pipes break the column count; newlines turn one row into many.
    Replace both with safe equivalents. (Table cells in CommonMark
    can't carry block content, so this is the standard workaround.)
    """
    return text.replace("|", "\\|").replace("\n", " ").strip()


def format_proposals(plans: list[PlanResult], intake_summary: str) -> str:
    """Render N PlanResults into one ProposalSet markdown document."""
    if not plans:
        return "# No plans available\n\n> intake produced no viable candidates.\n"

    n = len(plans)
    parts: list[str] = []
    parts.append(f"# 你的周六，{n} 种走法")
    parts.append("")
    summary = (intake_summary or "我听到了你想要的方向,下面是几种可能。").strip()
    parts.append(f"> {summary}")
    parts.append("")

    # Comparison table
    parts.append("## 速览对比")
    parts.append("")
    parts.append("| Theme | Pitch | First stop | Vibe |")
    parts.append("| --- | --- | --- | --- |")
    for plan in plans:
        theme = _escape_cell(plan.theme_anchor.value)
        pitch = _escape_cell(plan.pitch or "—")
        first = _escape_cell(_first_stop_name(plan))
        vibe = _escape_cell(_vibe_text(plan))
        parts.append(f"| {theme} | {pitch} | {first} | {vibe} |")
    parts.append("")

    # Plan bodies, separated by horizontal rules
    for plan in plans:
        parts.append("---")
        parts.append("")
        parts.append(plan.markdown.strip())
        parts.append("")

    return "\n".join(parts)


__all__ = ["format_proposals"]
