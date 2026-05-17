import { NextResponse } from "next/server";

/**
 * GET /api/plans
 *
 * Returns the list of demo TripPlans available. For backend handoff —
 * lets the backend introspect what IDs the frontend currently knows about.
 */

const PLANS = [
  {
    id: "family-day",
    label: "Garry · Family Day",
    template: "polaroid",
    demo_url: "/demo/family-day",
    json_url: "/api/plans/family-day",
  },
  {
    id: "cultural-day",
    label: "Garry · Cultural Day",
    template: "cinematic",
    demo_url: "/demo/cultural-day",
    json_url: "/api/plans/cultural-day",
  },
  {
    id: "golden-night",
    label: "Garry · Golden Night",
    template: "aurora",
    demo_url: "/demo/golden-night",
    json_url: "/api/plans/golden-night",
  },
];

export function GET() {
  return NextResponse.json({
    plans: PLANS,
    schema_doc: "/lib/types/trip-plan.ts",
    note: "Each /api/plans/<id> returns a full TripPlan JSON object — the exact shape the frontend renders.",
  });
}
