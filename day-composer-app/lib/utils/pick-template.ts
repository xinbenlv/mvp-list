import type { TripContext, TripPlan, TemplateId } from "@/lib/types/trip-plan";

/**
 * Pick a template based on plan + (optional) trip context.
 *
 * `mood_tags` are FREE strings now (no enum), so we lowercase-join the array
 * and use substring matching. Well-known anchors:
 *   - restorative / reflective / quietly cultural / sun-warmed → polaroid
 *   - celebratory / lively / vlog / golden-hour / cinematic    → cinematic
 *   - intimate / romantic                                       → aurora
 */
export function pickTemplate(
  plan: TripPlan,
  tripContext?: TripContext,
): TemplateId {
  const mood = plan.mood_tags.join(" ").toLowerCase();
  const has = (needle: string) => mood.includes(needle);
  const companions = tripContext?.companions ?? [];
  const hasBabyOrFamily = companions.some((c) =>
    /baby|family|kid|child/i.test(c),
  );

  // Cinematic / lively wins over polaroid if both signal — vlog-ready,
  // golden-hour, cinematic are strong cues.
  if (
    has("cinematic") ||
    has("vlog") ||
    has("golden-hour") ||
    has("celebratory") ||
    has("lively")
  ) {
    return "cinematic";
  }

  if (
    (has("restorative") || has("reflective") || has("quietly cultural") || has("sun-warmed") || has("low-friction") || has("grounding")) &&
    (hasBabyOrFamily || companions.length === 0)
  ) {
    return "polaroid";
  }

  if ((has("intimate") || has("romantic")) && companions.length === 1) {
    return "aurora";
  }

  return "polaroid";
}
