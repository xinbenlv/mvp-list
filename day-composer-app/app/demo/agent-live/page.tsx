import Link from "next/link";
import { PolaroidKeepsake } from "@/components/templates/polaroid-keepsake";
import { CinematicEditorial } from "@/components/templates/cinematic-editorial";
import { AuroraRomance } from "@/components/templates/aurora-romance";
import {
  AGENT_GARRY_CULTURAL,
  AGENT_GARRY_OUTDOOR,
  AGENT_GARRY_SOCIAL,
} from "@/lib/data/agent-generated";

export const metadata = {
  title: "Live from the Agent — Day Composer",
};

/**
 * /demo/agent-live — three TripPlans produced end-to-end by the live Composer
 * (poc-demo/garry-demo/v3/*.json), each rendered through one of the three
 * existing templates so reviewers can see the same backend output styled three
 * ways.
 *
 * Unlike /demo/{family,cultural,golden}-day, the plans here are NOT hand
 * curated — they are exactly what the agent wrote. Image coverage is sparse
 * (most place_ids are not in the IMAGES map) so most stops render with the
 * template's gradient fallback. That is intentional: the visual story is
 * "this is what the agent really shipped, end-to-end."
 */
export default function AgentLiveDemoPage() {
  const sections: Array<{
    label: string;
    template: "Polaroid Keepsake" | "Cinematic Editorial" | "Aurora Romance";
    bundle: typeof AGENT_GARRY_CULTURAL;
    Render: React.ComponentType<{
      plan: typeof AGENT_GARRY_CULTURAL.plan;
      tripContext: typeof AGENT_GARRY_CULTURAL.trip_context;
    }>;
  }> = [
    {
      label: "Plan I · cultural_restorative",
      template: "Polaroid Keepsake",
      bundle: AGENT_GARRY_CULTURAL,
      Render: PolaroidKeepsake,
    },
    {
      label: "Plan II · outdoor_exploratory",
      template: "Cinematic Editorial",
      bundle: AGENT_GARRY_OUTDOOR,
      Render: CinematicEditorial,
    },
    {
      label: "Plan III · social_high_energy",
      template: "Aurora Romance",
      bundle: AGENT_GARRY_SOCIAL,
      Render: AuroraRomance,
    },
  ];

  return (
    <main style={{ background: "#0c0a08", color: "#f4f1e8" }}>
      <header
        style={{
          padding: "56px 40px 48px",
          borderBottom: "1px solid #2a2620",
          fontFamily: "system-ui, sans-serif",
          maxWidth: 1180,
          margin: "0 auto",
        }}
      >
        <div
          style={{
            fontSize: 11,
            letterSpacing: ".3em",
            textTransform: "uppercase",
            color: "#c9a87a",
            marginBottom: 14,
          }}
        >
          Day Composer · Live Agent Output
        </div>
        <h1
          style={{
            fontFamily: "var(--font-fraunces), 'Times New Roman', serif",
            fontWeight: 300,
            fontSize: 56,
            letterSpacing: "-.025em",
            lineHeight: 1.0,
            margin: "0 0 18px",
            color: "#f4f1e8",
          }}
        >
          Three plans, <em style={{ color: "#c9a87a" }}>written by the agent.</em>
        </h1>
        <p
          style={{
            fontFamily: "var(--font-fraunces), serif",
            fontStyle: "italic",
            fontWeight: 300,
            fontSize: 18,
            color: "#b8b2a4",
            maxWidth: 780,
            lineHeight: 1.55,
            margin: "0 0 20px",
          }}
        >
          What follows is the unmodified output of the live Composer pipeline for
          Garry — same JSON the backend produced, just routed into each of the
          three existing templates. Some stops render without a hero photo;
          that is the gradient fallback when an image is not on hand.
        </p>
        <div
          style={{
            fontFamily: "monospace",
            fontSize: 11,
            letterSpacing: ".18em",
            textTransform: "uppercase",
            color: "#8a8275",
          }}
        >
          Source · poc-demo/garry-demo/v3/*.json &nbsp;·&nbsp;{" "}
          <Link href="/demo" style={{ color: "#c9a87a" }}>
            ← back to /demo
          </Link>
        </div>
      </header>

      {sections.map(({ label, template, bundle, Render }, i) => (
        <section
          key={label}
          style={{
            background: "#f4f1e8",
            color: "#1c1814",
            borderTop: i === 0 ? "none" : "8px solid #0c0a08",
          }}
        >
          <div
            style={{
              maxWidth: 1180,
              margin: "0 auto",
              padding: "30px 40px 8px",
              fontFamily: "monospace",
              fontSize: 11,
              letterSpacing: ".24em",
              textTransform: "uppercase",
              color: "#8b4a4a",
              display: "flex",
              gap: 18,
              flexWrap: "wrap",
            }}
          >
            <span style={{ fontWeight: 700 }}>{label}</span>
            <span style={{ color: "#8a8275" }}>· rendered with {template}</span>
            <span style={{ color: "#8a8275" }}>
              · plan_id {bundle.plan.plan_id}
            </span>
          </div>
          <Render plan={bundle.plan} tripContext={bundle.trip_context} />
        </section>
      ))}
    </main>
  );
}
