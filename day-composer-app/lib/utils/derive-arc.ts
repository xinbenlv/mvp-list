import type { ArcPoint, Stop } from "@/lib/types/trip-plan";

/**
 * Default vibe curve for a 4-stop day: opening (0.25) → breathing (0.40) →
 * peak (0.85) → closing (0.55). For other counts, linearly interpolate this
 * shape to N points.
 */
const DEFAULT_SHAPE = [0.25, 0.4, 0.85, 0.55];
const DEFAULT_LADDER = ["opening", "breathing", "peak", "closing"];

/** Anchor-specific label sequences. Falls through to DEFAULT_LADDER. */
const ANCHOR_LADDERS: Record<string, string[]> = {
  cultural_restorative: ["slow start", "breathing", "peak", "closing"],
  social_high_energy: ["spark", "rise", "peak", "afterglow"],
  vlog_cinematic: ["opening", "build", "climax", "fade"],
};

function sampleShape(n: number, shape: number[]): number[] {
  if (n <= 1) return [shape[Math.floor(shape.length / 2)]];
  const out: number[] = [];
  const last = shape.length - 1;
  for (let i = 0; i < n; i++) {
    const t = (i / (n - 1)) * last;
    const lo = Math.floor(t);
    const hi = Math.min(last, lo + 1);
    const frac = t - lo;
    out.push(shape[lo] * (1 - frac) + shape[hi] * frac);
  }
  return out;
}

function sampleLadder(n: number, ladder: string[]): string[] {
  if (n <= ladder.length) {
    // pick spread evenly: e.g. n=3 from 4 ladder → ladder[0], ladder[1], ladder[3]
    const out: string[] = [];
    for (let i = 0; i < n; i++) {
      const idx = Math.round((i * (ladder.length - 1)) / (n - 1 || 1));
      out.push(ladder[idx]);
    }
    return out;
  }
  // n > ladder.length: repeat by stretching
  const out: string[] = [];
  for (let i = 0; i < n; i++) {
    const idx = Math.min(ladder.length - 1, Math.floor((i * ladder.length) / n));
    out.push(ladder[idx]);
  }
  return out;
}

export function deriveArc(stops: Stop[], themeAnchor?: string | null): ArcPoint[] {
  const n = stops.length;
  if (n === 0) return [];
  const ys = sampleShape(n, DEFAULT_SHAPE);
  const ladder = (themeAnchor && ANCHOR_LADDERS[themeAnchor]) || DEFAULT_LADDER;
  const labels = sampleLadder(n, ladder);
  return stops.map((s, i) => ({
    x: n === 1 ? 0.5 : i / (n - 1),
    y: ys[i],
    label: labels[i],
    time: s.time,
  }));
}

/** Index of the peak (max y). */
export function peakIndex(arc: ArcPoint[]): number {
  let best = 0;
  let bestY = -Infinity;
  arc.forEach((p, i) => {
    if (p.y > bestY) {
      bestY = p.y;
      best = i;
    }
  });
  return best;
}
