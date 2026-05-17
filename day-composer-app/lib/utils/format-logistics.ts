import type { Logistics } from "@/lib/types/trip-plan";

/**
 * Render a stop's logistics as a list of short chip strings. Decomposes the
 * nested typed fields rather than using `logistics.raw` so templates can style
 * each chip independently.
 */
export function formatLogisticsChips(
  logistics: Logistics | undefined | null,
): string[] {
  if (!logistics) return [];
  const out: string[] = [];

  if (logistics.drive_time_min != null) {
    out.push(`🚗 ${logistics.drive_time_min}min`);
  }
  if (logistics.parking) {
    // Free-form. Truncate long descriptions to first comma / paren.
    const cleaned = logistics.parking
      .replace(/\s*\(.*?\)\s*/g, " ")
      .split(",")[0]
      .trim();
    out.push(`🅿 ${cleaned}`);
  }
  if (logistics.kid_friendly === true) {
    out.push(`👶 friendly`);
  } else if (logistics.kid_friendly === false) {
    out.push(`⚠ no baby`);
  }
  if (logistics.reservation_note) {
    const note = logistics.reservation_note.split(",")[0].trim();
    out.push(`🎟 ${note}`);
  }
  if (logistics.transit_estimate_usd != null) {
    out.push(`💵 ~$${logistics.transit_estimate_usd}`);
  }

  return out;
}

/**
 * Display name for a mood tag. With free-string tags from the backend, mostly
 * we just pass through — but some well-known underscore forms get prettified.
 */
const MOOD_DISPLAY: Record<string, string> = {
  // historical MoodTag enum entries — still seen in samples
  lightly_exploratory: "lightly exploratory",
  deeply_exploratory: "deeply exploratory",
  not_rushed: "not rushed",
  // emotional roles defensively
  restore: "restorative",
  explore: "exploratory",
  celebrate: "celebratory",
  reconnect: "warm",
  slow_down: "not rushed",
  feel_alive: "energizing",
};

export function formatMoodTag(tag: string): string {
  return MOOD_DISPLAY[tag] ?? tag.replace(/_/g, " ");
}
