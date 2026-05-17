import { PolaroidKeepsake } from "@/components/templates/polaroid-keepsake";
import {
  SAMPLE_PLAN_GARRY_FAMILY_DAY_EN,
  TRIP_CONTEXT_GARRY_FAMILY_DAY,
} from "@/lib/data/sample-plan-en";

export const metadata = {
  title: "Garry · Family Day — Day Composer",
};

/**
 * Demo route: Garry's South Bay family-day, rendered in the Polaroid template.
 * Pure render, no controls — meant for sharing / screenshots.
 */
export default function GarryFamilyDayPage() {
  return (
    <PolaroidKeepsake
      plan={SAMPLE_PLAN_GARRY_FAMILY_DAY_EN}
      tripContext={TRIP_CONTEXT_GARRY_FAMILY_DAY}
    />
  );
}
