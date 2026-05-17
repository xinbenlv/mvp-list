import { AuroraRomance } from "@/components/templates/aurora-romance";
import {
  SAMPLE_PLAN_GARRY_GOLDEN_NIGHT_EN,
  TRIP_CONTEXT_GARRY_GOLDEN_NIGHT,
} from "@/lib/data/sample-plan-en";

export const metadata = {
  title: "Garry · Golden Night — Day Composer",
};

/**
 * Demo route: Garry's SF cinematic night ending at Top of the Mark,
 * rendered in the Aurora Romance template (dreamy / golden-hour palette).
 */
export default function GarryGoldenNightPage() {
  return (
    <AuroraRomance
      plan={SAMPLE_PLAN_GARRY_GOLDEN_NIGHT_EN}
      tripContext={TRIP_CONTEXT_GARRY_GOLDEN_NIGHT}
    />
  );
}
