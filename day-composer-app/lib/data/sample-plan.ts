import type { SamplesFile, TripContext, TripPlan } from "@/lib/types/trip-plan";
import samplesJson from "./sample-plans.json";

/**
 * Loads `sample-plans.json` (4 plans: mia_v1, mia_v2, garry_v1, garry_v2)
 * from the real backend dry-run output. See `mvp-list/poc-demo/sample-plans.json`
 * (copied into this app's lib/data/ for clean webpack import).
 *
 * NOTE: Plans loaded from JSON are in the original Chinese. For the English
 * demo, see `sample-plan-en.ts` (`SAMPLE_PLAN_MIA_V1_EN`).
 */
const FILE = samplesJson as unknown as SamplesFile;

const byId = new Map<string, TripPlan>();
for (const p of FILE.plans) byId.set(p.plan_id, p);

export const SAMPLE_FILE: SamplesFile = FILE;
export const SAMPLE_PLANS: TripPlan[] = FILE.plans;

/** Default sample = the first plan (mia_v1). */
export const SAMPLE_PLAN: TripPlan = byId.get("mia_v1") ?? FILE.plans[0];

export const SAMPLE_PLAN_MIA_V1: TripPlan = byId.get("mia_v1") ?? FILE.plans[0];
export const SAMPLE_PLAN_MIA_V2: TripPlan = byId.get("mia_v2") ?? FILE.plans[0];
export const SAMPLE_PLAN_GARRY_V1: TripPlan =
  byId.get("garry_v1") ?? FILE.plans[0];
export const SAMPLE_PLAN_GARRY_V2: TripPlan =
  byId.get("garry_v2") ?? FILE.plans[0];

export function getPlanById(id: string): TripPlan | undefined {
  return byId.get(id);
}

/** Frontend convenience metadata — not in TripPlan schema. */
export const SAMPLE_TRIP_CONTEXT: TripContext = {
  date_label: "Sat · Jan 10 · 2026",
  time_window: "14:30 → 22:00",
  origin: "Sunnyvale",
  companions: ["+1", "+baby"],
  vehicle: "car",
};
