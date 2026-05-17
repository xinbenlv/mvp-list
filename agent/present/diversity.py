"""Diversity enforcement across N PlanResults — Phase 3b.

Implements the structural diversity guarantees from eng design §14:

    1. No two plans share the same first stop (`stop_place_ids[0]`).
    2. No two plans share more than 1 stop overall.
    3. All plan `theme_anchor`s are distinct.

`check_diversity` reports violations as human-readable strings.
`deduplicate_first_stops` performs a metadata-only swap when 2+ plans
share their first stop, by promoting a later stop in the offending plan
to position 0 (chosen from a non-conflicting candidate).

Caveat (documented inline below): metadata reordering does NOT rewrite
the plan's markdown body. The Composer LLM still wrote the original
ordering. For demo correctness we accept this gap; Phase 4 Critic +
re-compose will close it by re-asking the LLM to author the swapped
plan from scratch.
"""

from __future__ import annotations

from agent.types import PlaceCandidate, PlanResult


def check_diversity(plans: list[PlanResult]) -> list[str]:
    """Return list of diversity violations; empty list means all good.

    Each violation is a one-line human-readable string suitable for
    stderr logging or test assertion messages.
    """
    violations: list[str] = []
    if len(plans) < 2:
        return violations

    # Rule 1: distinct first stops
    first_stops: list[str] = []
    for idx, plan in enumerate(plans):
        first = plan.stop_place_ids[0] if plan.stop_place_ids else ""
        if first and first in first_stops:
            other_idx = first_stops.index(first)
            violations.append(
                f"plan[{idx}] shares first stop '{first}' with plan[{other_idx}]"
            )
        first_stops.append(first)

    # Rule 2: pairwise overlap <= 1 stop
    for i in range(len(plans)):
        for j in range(i + 1, len(plans)):
            a = {pid for pid in plans[i].stop_place_ids if pid}
            b = {pid for pid in plans[j].stop_place_ids if pid}
            overlap = a & b
            if len(overlap) > 1:
                violations.append(
                    f"plan[{i}] and plan[{j}] share {len(overlap)} stops "
                    f"(>1): {sorted(overlap)}"
                )

    # Rule 3: distinct theme_anchors
    seen_themes: dict[str, int] = {}
    for idx, plan in enumerate(plans):
        key = plan.theme_anchor.value
        if key in seen_themes:
            violations.append(
                f"plan[{idx}] reuses theme_anchor '{key}' from plan[{seen_themes[key]}]"
            )
        else:
            seen_themes[key] = idx

    return violations


def deduplicate_first_stops(
    plans: list[PlanResult], candidates: list[PlaceCandidate]
) -> list[PlanResult]:
    """If 2+ plans share `stop_place_ids[0]`, swap later plans' first stops.

    Strategy:
      - Keep plan[0] anchor as-is (treated as canonical).
      - For plan[1], plan[2], ...: if its first stop is already taken by
        an earlier plan, scan its `stop_place_ids[1:]` and promote the
        first non-conflicting one to position 0 (swap in place).
      - If no internal swap resolves the conflict, leave the plan as-is
        — a future Critic pass can re-trigger the Composer.

    Returns a new list of PlanResults (Pydantic model_copy with
    `stop_place_ids` updated). `markdown` body is intentionally NOT
    rewritten; see module docstring for rationale.

    `candidates` is currently unused for the swap (we only reshuffle
    within each plan's existing stop set), but is accepted to keep the
    signature future-proof for Phase 4, when we might pull a fresh
    anchor from the pool instead of reshuffling.
    """
    _ = candidates  # reserved for Phase 4 — see docstring
    taken: set[str] = set()
    out: list[PlanResult] = []

    for plan in plans:
        ids = list(plan.stop_place_ids)
        names = list(plan.stop_names) if plan.stop_names else []

        if not ids:
            out.append(plan)
            continue

        first = ids[0]
        if first not in taken:
            taken.add(first)
            out.append(plan)
            continue

        # Conflict — try to swap with a later non-conflicting stop.
        swap_idx = next(
            (
                i
                for i in range(1, len(ids))
                if ids[i] and ids[i] not in taken and ids[i] != first
            ),
            None,
        )
        if swap_idx is None:
            # Unresolvable inside this plan's existing pool — leave as-is.
            # Phase 4 Critic could re-compose. Don't mark first as taken
            # twice (it already is).
            out.append(plan)
            continue

        ids[0], ids[swap_idx] = ids[swap_idx], ids[0]
        if names and swap_idx < len(names):
            names[0], names[swap_idx] = names[swap_idx], names[0]
        taken.add(ids[0])
        out.append(plan.model_copy(update={"stop_place_ids": ids, "stop_names": names}))

    return out


__all__ = ["check_diversity", "deduplicate_first_stops"]
