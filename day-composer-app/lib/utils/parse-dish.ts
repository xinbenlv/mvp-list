/**
 * Parse a dish entry like `"88 烤生蚝 · grilled oyster"` or
 * `"Pour-over single origin"` into `{ menu_number, name }`.
 *
 * - If the string starts with a numeric token followed by a space, treat it
 *   as the menu number; everything after becomes the name.
 *   `"88 烤生蚝 · grilled oyster"` → `{ menu_number: "88", name: "烤生蚝 · grilled oyster" }`.
 * - Otherwise menu_number is null and the whole string is the name.
 *
 * Bilingual dish names (Chinese + ` · ` + English gloss) are intentional and
 * preserved as-is; the parser only strips the leading menu number.
 */
export interface ParsedDish {
  menu_number: string | null;
  name: string;
}

const MENU_PREFIX = /^(\d+[A-Za-z]?)\s+(.+)$/;

export function parseDish(raw: string): ParsedDish {
  const trimmed = raw.trim();
  const m = trimmed.match(MENU_PREFIX);
  if (m) {
    return { menu_number: m[1], name: m[2].trim() };
  }
  return { menu_number: null, name: trimmed };
}

/** Returns true if `bold_picks` contains the same dish string. */
export function isBoldPick(raw: string, boldPicks: string[]): boolean {
  return boldPicks.includes(raw);
}
