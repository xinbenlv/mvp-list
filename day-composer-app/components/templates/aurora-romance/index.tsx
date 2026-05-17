"use client";

import type { CSSProperties } from "react";
import type { TemplateProps } from "@/lib/types/trip-plan";
import { usePalette } from "@/lib/hooks/use-palette";
import { deriveArc } from "@/lib/utils/derive-arc";
import { Hero } from "./hero";
import { ArcCard } from "./arc-card";
import { StopRow } from "./stop-row";
import { Branches } from "./branches";
import { RefineBar } from "./refine-bar";

export function AuroraRomance({ plan, tripContext, onRefine }: TemplateProps) {
  const palette = usePalette(plan, "aurora");
  return (
    <div
      className="au-root au-mesh relative min-h-screen pb-[110px]"
      style={palette as CSSProperties}
    >
      {/* Sparkles */}
      <div className="pointer-events-none fixed inset-0 z-[-1]">
        {[
          { top: "12%", left: "18%", delay: "0s", size: 4 },
          { top: "30%", left: "75%", delay: "1.2s", size: 6 },
          { top: "50%", left: "8%", delay: "2.4s", size: 4 },
          { top: "65%", left: "88%", delay: ".6s", size: 5 },
          { top: "80%", left: "42%", delay: "3s", size: 4 },
          { top: "20%", left: "50%", delay: "1.8s", size: 3 },
          { top: "90%", left: "25%", delay: "2s", size: 4 },
          { top: "42%", left: "60%", delay: ".4s", size: 4 },
        ].map((s, i) => (
          <span
            key={i}
            className="au-sparkle"
            style={{
              top: s.top,
              left: s.left,
              width: s.size,
              height: s.size,
              animationDelay: s.delay,
            }}
          />
        ))}
      </div>
      <Hero plan={plan} tripContext={tripContext} />
      <ArcCard plan={plan} />
      <section className="mx-auto max-w-[1280px] px-10 pb-[60px] pt-10 max-md:px-6">
        {(() => {
          const arc = deriveArc(plan.stops, plan.theme_anchor);
          return plan.stops.map((stop, i) => {
            const isLast = i === plan.stops.length - 1;
            return (
              <StopRow
                key={`${stop.place_id}-${i}`}
                stop={stop}
                index={i}
                pacingLabel={arc[i]?.label}
                orderRecs={stop.order_recommendations}
                transitionText={!isLast ? stop.transition_to_next : null}
                transitionDriveMin={!isLast ? stop.transition_drive_min : null}
              />
            );
          });
        })()}
      </section>
      <Branches branches={plan.adaptive_branches} />
      <div
        className="relative mx-auto mb-20 max-w-[680px] rounded-[32px] border px-7 py-10 text-center max-md:px-5"
        style={{
          fontFamily: "var(--font-cormorant), serif",
          fontStyle: "italic",
          fontWeight: 300,
          fontSize: 28,
          color: "var(--ink)",
          lineHeight: 1.5,
          background: "rgba(255,255,255,.4)",
          backdropFilter: "blur(20px)",
          borderColor: "rgba(255,255,255,.6)",
        }}
      >
        “a day is not <em style={{ color: "var(--accent-deep)" }}>four places</em> —
        <br />
        it is a <em style={{ color: "var(--accent-deep)" }}>rhythm</em>,
        <br />a feeling carried from light into dark.”
        <small
          className="mt-[18px] block"
          style={{
            fontFamily: "var(--font-dm-mono), monospace",
            fontSize: 11,
            letterSpacing: ".32em",
            textTransform: "uppercase",
            color: "var(--accent-deep)",
            fontStyle: "normal",
          }}
        >
          composed · not scheduled
        </small>
      </div>
      <RefineBar onRefine={onRefine} />
    </div>
  );
}
