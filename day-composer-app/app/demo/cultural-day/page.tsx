import { CinematicEditorial } from "@/components/templates/cinematic-editorial";
import {
  SAMPLE_PLAN_GARRY_CULTURAL_DAY_EN,
  TRIP_CONTEXT_GARRY_CULTURAL_DAY,
} from "@/lib/data/sample-plan-en";

export const metadata = {
  title: "Garry · Cultural Day — Day Composer",
};

/**
 * Demo route: Garry's SF cultural day, rendered in the Cinematic Editorial
 * template (Vogue-flavored magazine spread).
 */
export default function GarryCulturalDayPage() {
  return (
    <CinematicEditorial
      plan={SAMPLE_PLAN_GARRY_CULTURAL_DAY_EN}
      tripContext={TRIP_CONTEXT_GARRY_CULTURAL_DAY}
    />
  );
}
