"use client";

import type { CSSProperties } from "react";
import type { TemplateProps } from "@/lib/types/trip-plan";
import { usePalette } from "@/lib/hooks/use-palette";
import { deriveArc } from "@/lib/utils/derive-arc";
import { Masthead } from "./masthead";
import { Hero } from "./hero";
import { Toc } from "./toc";
import { PullQuote } from "./pull-quote";
import { Spread } from "./spread";
import { Restaurant } from "./restaurant";
import { Branches } from "./branches";
import { RefineBar } from "./refine-bar";

export function CinematicEditorial({ plan, tripContext, onRefine }: TemplateProps) {
  const palette = usePalette(plan, "cinematic");
  const arc = deriveArc(plan.stops, plan.theme_anchor);

  return (
    <div className="ce-root pb-[80px]" style={palette as CSSProperties}>
      <Masthead tripContext={tripContext} />
      <Hero plan={plan} tripContext={tripContext} />
      <Toc plan={plan} />
      {plan.stops.map((stop, i) => {
        const rec = stop.order_recommendations;
        const beat = arc[i];
        // Treat a stop as a "restaurant spread" if it has order recommendations.
        const isRestaurant = !!rec;
        return (
          <div key={`${stop.place_id}-${i}`}>
            {isRestaurant ? (
              <Restaurant stop={stop} index={i} rec={rec} />
            ) : (
              <Spread
                stop={stop}
                index={i}
                pacingLabel={beat?.label}
                arcVibe={beat?.y}
              />
            )}
            {i < plan.stops.length - 1 && stop.transition_to_next && (
              <PullQuote
                text={stop.transition_to_next}
                meta={
                  stop.transition_drive_min != null
                    ? `Transition · ${stop.transition_drive_min} min drive`
                    : "Transition"
                }
              />
            )}
          </div>
        );
      })}
      <Branches branches={plan.adaptive_branches} />
      <section
        className="px-[50px] py-[80px] text-center max-md:px-6 max-md:py-[50px]"
        style={{
          background: "var(--jet)",
          color: "var(--whisper)",
          borderTop: "6px solid var(--red)",
        }}
      >
        <p
          className="mx-auto mb-6"
          style={{
            fontFamily: "var(--font-bodoni), serif",
            fontStyle: "italic",
            fontSize: 32,
            color: "var(--ivory)",
            lineHeight: 1.35,
            maxWidth: 780,
            letterSpacing: "-.01em",
          }}
        >
          “A day rhythm, not four POIs.{" "}
          <em style={{ color: "var(--red)" }}>A composition,</em> not a checklist.”
        </p>
        <div
          style={{
            fontFamily: "var(--font-jetbrains), monospace",
            fontSize: 10,
            letterSpacing: ".4em",
            textTransform: "uppercase",
            color: "var(--red)",
            fontWeight: 700,
          }}
        >
          Day Composer · Issue I · MMXXVI · composed, not scheduled
        </div>
      </section>
      <RefineBar onRefine={onRefine} />
    </div>
  );
}
