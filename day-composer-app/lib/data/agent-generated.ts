/**
 * Agent-generated TripPlans (v3) from the live Composer pipeline.
 *
 * Source: poc-demo/garry-demo/v3/*.json — copied into ./agent-v3/ at integration
 * time so Next.js can import them without crossing the app boundary
 * (`experimental.externalDir` is not enabled). When the backend wires up
 * Pattern 1 (POST /compose), this static-import path goes away.
 *
 * Distinct from `sample-plan-en.ts`, which holds buddy's hand-curated
 * reference plans rendered at /demo/{family,cultural,golden}-day.
 *
 * Image coverage caveat: most v3 stops use place_ids absent from the
 * IMAGES map (or empty strings); those stops render with the template's
 * gradient fallback. Today only `top_of_the_mark` matches.
 */
import type { TripContext, TripPlan } from "@/lib/types/trip-plan";
import { imageForPlace } from "@/lib/data/sample-plan-en";

import culturalRaw from "./agent-v3/garry_cultural_restorative.json";
import outdoorRaw from "./agent-v3/garry_outdoor_exploratory.json";
import socialRaw from "./agent-v3/garry_social_high_energy.json";

export interface AgentPlanBundle {
  plan: TripPlan;
  trip_context: TripContext;
}

interface RawBundle {
  plan: unknown;
  trip_context: Record<string, unknown>;
}

/**
 * Coerce a raw JSON bundle into the strict frontend types.
 *
 * The JSONs include extra trip_context fields (`persona_id`, `intake_summary`,
 * `today_is`) that are not on the TripContext type — we strip them down to the
 * five fields the templates actually consume.
 *
 * Stops carry a literal `image_url: null`; we inject from the IMAGES map by
 * place_id so any overlap with buddy's reference set (e.g. top_of_the_mark)
 * picks up a real photo for free. Unmapped place_ids stay null → template
 * renders a gradient.
 */
function adoptBundle(raw: RawBundle): AgentPlanBundle {
  const plan = raw.plan as TripPlan;
  for (const stop of plan.stops) {
    if (!stop.image_url) {
      stop.image_url = imageForPlace(stop.place_id);
    }
  }
  const ctx = raw.trip_context;
  const trip_context: TripContext = {
    date_label: String(ctx.date_label ?? ""),
    time_window: String(ctx.time_window ?? ""),
    origin: String(ctx.origin ?? ""),
    companions: Array.isArray(ctx.companions)
      ? (ctx.companions as string[])
      : [],
    vehicle: String(ctx.vehicle ?? ""),
  };
  return { plan, trip_context };
}

export const AGENT_GARRY_CULTURAL: AgentPlanBundle = adoptBundle(
  culturalRaw as RawBundle,
);
export const AGENT_GARRY_OUTDOOR: AgentPlanBundle = adoptBundle(
  outdoorRaw as RawBundle,
);
export const AGENT_GARRY_SOCIAL: AgentPlanBundle = adoptBundle(
  socialRaw as RawBundle,
);

export const AGENT_GARRY_PLANS: AgentPlanBundle[] = [
  AGENT_GARRY_CULTURAL,
  AGENT_GARRY_OUTDOOR,
  AGENT_GARRY_SOCIAL,
];
