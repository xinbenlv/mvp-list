"use client";

import type { CSSProperties } from "react";
import type { TemplateProps } from "@/lib/types/trip-plan";
import { usePalette } from "@/lib/hooks/use-palette";
import { Cover } from "./cover";
import { ArcCurve } from "./arc-curve";
import { StopPage } from "./stop-page";
import { Branches } from "./branches";
import { RefineBar } from "./refine-bar";

export function PolaroidKeepsake({ plan, tripContext, onRefine }: TemplateProps) {
  const palette = usePalette(plan, "polaroid");
  return (
    <div
      className="pk-root pk-noise relative min-h-screen px-5 pb-[110px] pt-10"
      style={palette as CSSProperties}
    >
      <Cover plan={plan} tripContext={tripContext} />
      <ArcCurve plan={plan} />
      {plan.stops.map((stop, i) => (
        <StopPage
          key={`${stop.place_id}-${i}`}
          stop={stop}
          index={i}
          isLast={i === plan.stops.length - 1}
        />
      ))}
      <Branches branches={plan.adaptive_branches} />
      <div
        className="mx-auto mb-[60px] max-w-[560px] px-0 py-[30px] text-center"
        style={{
          fontFamily: "var(--font-caveat), cursive",
          fontWeight: 500,
          fontSize: 30,
          color: "var(--ink-soft)",
          lineHeight: 1.3,
          transform: "rotate(-.6deg)",
        }}
      >
        “A day rhythm,
        <br />
        not four points on a map.”
        <small
          className="mt-[18px] block"
          style={{
            fontFamily: "var(--font-elite), monospace",
            fontSize: 11,
            letterSpacing: ".3em",
            color: "var(--rose-deep)",
            textTransform: "uppercase",
          }}
        >
          composed · not scheduled
        </small>
      </div>
      <RefineBar onRefine={onRefine} />
    </div>
  );
}
