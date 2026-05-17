import { NextResponse } from "next/server";
import type { TripContext, TripPlan } from "@/lib/types/trip-plan";
import {
  SAMPLE_PLAN_GARRY_FAMILY_DAY_EN,
  SAMPLE_PLAN_GARRY_CULTURAL_DAY_EN,
  SAMPLE_PLAN_GARRY_GOLDEN_NIGHT_EN,
  TRIP_CONTEXT_GARRY_FAMILY_DAY,
  TRIP_CONTEXT_GARRY_CULTURAL_DAY,
  TRIP_CONTEXT_GARRY_GOLDEN_NIGHT,
} from "@/lib/data/sample-plan-en";

/**
 * GET /api/plans/[id]
 *
 * Returns one demo TripPlan + its TripContext. Backend can mirror this
 * shape when generating its own plans.
 *
 * IDs match the /demo route segments: family-day | cultural-day | golden-night
 */

interface Bundle {
  plan: TripPlan;
  trip_context: TripContext;
}

const BUNDLES: Record<string, Bundle> = {
  "family-day": {
    plan: SAMPLE_PLAN_GARRY_FAMILY_DAY_EN,
    trip_context: TRIP_CONTEXT_GARRY_FAMILY_DAY,
  },
  "cultural-day": {
    plan: SAMPLE_PLAN_GARRY_CULTURAL_DAY_EN,
    trip_context: TRIP_CONTEXT_GARRY_CULTURAL_DAY,
  },
  "golden-night": {
    plan: SAMPLE_PLAN_GARRY_GOLDEN_NIGHT_EN,
    trip_context: TRIP_CONTEXT_GARRY_GOLDEN_NIGHT,
  },
};

// Required for `output: 'export'` — enumerate every id so the build can
// prerender each as a static JSON file.
export function generateStaticParams() {
  return Object.keys(BUNDLES).map((id) => ({ id }));
}

export const dynamic = "force-static";

export function GET(
  _req: Request,
  { params }: { params: { id: string } },
) {
  const bundle = BUNDLES[params.id];
  if (!bundle) {
    return NextResponse.json(
      { error: `Unknown plan id: ${params.id}. Try /api/plans for the list.` },
      { status: 404 },
    );
  }
  return NextResponse.json(bundle);
}
