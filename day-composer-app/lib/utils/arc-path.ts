import { line, curveCatmullRom } from "d3-shape";
import type { ArcPoint } from "@/lib/types/trip-plan";

/**
 * Build an SVG path string for the emotional arc curve from derived ArcPoints.
 *
 * X axis = point.x in [0..1] mapped to [marginX, width - marginX].
 * Y axis = (1 - point.y) so higher vibe = higher on viewport.
 *
 * Returns { pathD, points }: pathD is the `d` attribute; points carries
 * absolute coords + label/time for dots and captions.
 */
export interface ArcDrawPoint {
  x: number;
  y: number;
  label: string;
  time: string;
}

export function buildArcPath(
  arc: ArcPoint[],
  width: number,
  height: number,
  margins: { top: number; bottom: number; left: number; right: number } = {
    top: 30,
    bottom: 40,
    left: 60,
    right: 60,
  },
): { pathD: string; points: ArcDrawPoint[] } {
  if (arc.length === 0) return { pathD: "", points: [] };

  const innerW = width - margins.left - margins.right;
  const innerH = height - margins.top - margins.bottom;

  const points: ArcDrawPoint[] = arc.map((p) => ({
    x: margins.left + p.x * innerW,
    y: margins.top + (1 - p.y) * innerH,
    label: p.label,
    time: p.time,
  }));

  const generator = line<{ x: number; y: number }>()
    .x((p) => p.x)
    .y((p) => p.y)
    .curve(curveCatmullRom.alpha(0.5));

  const pathD = generator(points) ?? "";
  return { pathD, points };
}
