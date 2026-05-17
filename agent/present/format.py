"""format_proposals — pure template that wraps N PlanResults into one bundle.

Phase 0 stub: emits a minimal but well-formed ProposalSet markdown so the
end-to-end smoke flow produces non-empty output. Phase 3b fills in the
comparison table and intake-summary header per eng design §11 / Pre-Decision #15.
"""

from __future__ import annotations

from agent.types import PlanResult


def format_proposals(plans: list[PlanResult], intake_summary: str) -> str:
    """Render a list of PlanResults into one ProposalSet markdown document."""
    if not plans:
        return "# No plans available\n\n> intake produced no viable candidates.\n"

    parts: list[str] = []
    parts.append("# 你的周六，三种走法")
    parts.append("")
    parts.append(f"> {intake_summary or '我听到了你想要的方向,下面是几种可能。'}")
    parts.append("")
    parts.append("| Theme | Pitch | First stop |")
    parts.append("| --- | --- | --- |")
    for plan in plans:
        first_stop = plan.stop_place_ids[0] if plan.stop_place_ids else "(none)"
        parts.append(
            f"| {plan.theme_anchor.value} | {plan.pitch} | {first_stop} |"
        )
    parts.append("")
    for plan in plans:
        parts.append("---")
        parts.append("")
        parts.append(plan.markdown)
        parts.append("")
    return "\n".join(parts)


__all__ = ["format_proposals"]
