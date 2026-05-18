import Link from "next/link";
import { PolaroidKeepsake } from "@/components/templates/polaroid-keepsake";
import { CinematicEditorial } from "@/components/templates/cinematic-editorial";
import { AuroraRomance } from "@/components/templates/aurora-romance";
import {
  AGENT_MIA_CULTURAL,
  AGENT_MIA_OUTDOOR,
  AGENT_MIA_QUIET,
} from "@/lib/data/agent-generated";

export const metadata = {
  title: "Mia · Solo Sunday — Live from the Agent",
};

/**
 * /demo/agent-live-mia — three TripPlans produced end-to-end by the live
 * Composer for Mia's solo Sunday scenario ("不带宝宝, 脑子累, 自然光好, 慢一点").
 *
 * Companion route to /demo/agent-live (which renders Garry's plans). Same
 * three templates, same gradient-fallback story for missing images. Source
 * JSONs at poc-demo/mia-sunday/v3/*.json.
 */
export default function AgentLiveMiaDemoPage() {
  const sections: Array<{
    label: string;
    template: "Polaroid Keepsake" | "Cinematic Editorial" | "Aurora Romance";
    bundle: typeof AGENT_MIA_CULTURAL;
    Render: React.ComponentType<{
      plan: typeof AGENT_MIA_CULTURAL.plan;
      tripContext: typeof AGENT_MIA_CULTURAL.trip_context;
    }>;
  }> = [
    {
      label: "Plan I · cultural_restorative",
      template: "Polaroid Keepsake",
      bundle: AGENT_MIA_CULTURAL,
      Render: PolaroidKeepsake,
    },
    {
      label: "Plan II · outdoor_exploratory",
      template: "Cinematic Editorial",
      bundle: AGENT_MIA_OUTDOOR,
      Render: CinematicEditorial,
    },
    {
      label: "Plan III · quiet_intimate",
      template: "Aurora Romance",
      bundle: AGENT_MIA_QUIET,
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
          Day Composer · Live Agent Output · Mia
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
          A Sunday <em style={{ color: "#c9a87a" }}>alone in Marin.</em>
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
          Mia asked for a solo Sunday — no baby, brain tired, natural light, slow,
          not too far. The agent answered with three different Marin shapes:
          slow culture in Mill Valley, an outdoor walk anchored on Tomales Bay,
          and a deep quiet ritual ending at Osmosis. Same plumbing as Garry,
          different intake, different output.
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
          Source · poc-demo/mia-sunday/v3/*.json &nbsp;·&nbsp;{" "}
          <Link href="/demo" style={{ color: "#c9a87a" }}>
            ← back to /demo
          </Link>{" "}
          &nbsp;·&nbsp;{" "}
          <Link href="/demo/agent-live" style={{ color: "#c9a87a" }}>
            see Garry's set
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
