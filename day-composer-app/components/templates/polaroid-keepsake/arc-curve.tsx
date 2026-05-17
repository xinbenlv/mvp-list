"use client";

import { motion } from "framer-motion";
import { useMemo } from "react";
import type { TripPlan } from "@/lib/types/trip-plan";
import { buildArcPath } from "@/lib/utils/arc-path";
import { deriveArc, peakIndex } from "@/lib/utils/derive-arc";

interface ArcCurveProps {
  plan: TripPlan;
}

export function ArcCurve({ plan }: ArcCurveProps) {
  const width = 1000;
  const height = 200;
  const arc = useMemo(
    () => deriveArc(plan.stops, plan.theme_anchor),
    [plan.stops, plan.theme_anchor],
  );
  const { pathD, points } = buildArcPath(arc, width, height, {
    top: 30,
    bottom: 55,
    left: 125,
    right: 125,
  });
  const peakIdx = peakIndex(arc);

  return (
    <section
      className="relative mx-auto mb-20 max-w-[760px] px-[30px] pb-10 pt-[30px]"
      style={{
        background: "rgba(250,244,234,.6)",
        border: "1px solid rgba(43,35,43,.15)",
        transform: "rotate(-.4deg)",
        boxShadow: "0 6px 24px -10px rgba(43,35,43,.16)",
      }}
    >
      <div
        className="absolute left-[30px] top-[-10px] h-5 w-[90px]"
        style={{ transform: "rotate(-4deg)", background: "var(--tape-sage)" }}
      />
      <div
        className="absolute right-[30px] top-[-10px] h-5 w-[90px]"
        style={{ transform: "rotate(3deg)", background: "var(--tape-rose)" }}
      />
      <div
        className="mb-[10px] text-center"
        style={{
          fontFamily: "var(--font-elite), monospace",
          fontSize: 10,
          letterSpacing: ".32em",
          textTransform: "uppercase",
          color: "var(--rose-deep)",
        }}
      >
        The Shape of the Day
      </div>
      <h2
        className="mb-3 text-center"
        style={{
          fontFamily: "var(--font-caveat), cursive",
          fontWeight: 500,
          fontSize: 36,
          color: "var(--ink)",
          transform: "rotate(-.5deg)",
        }}
      >
        ~ how the day rises &amp; falls ~
      </h2>
      <svg
        viewBox={`0 0 ${width} ${height}`}
        preserveAspectRatio="none"
        className="block h-[200px] w-full max-md:h-[160px]"
      >
        <defs>
          <filter id="pk-wiggle">
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.02"
              numOctaves={2}
              seed={3}
              stitchTiles="stitch"
            />
            <feDisplacementMap in="SourceGraphic" scale={3} />
          </filter>
        </defs>
        <motion.path
          d={pathD}
          fill="none"
          stroke="var(--sage)"
          strokeWidth={1.5}
          strokeLinecap="round"
          opacity={0.5}
          filter="url(#pk-wiggle)"
          transform="translate(0,4)"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 1.8, ease: "easeInOut" }}
        />
        <motion.path
          d={pathD}
          fill="none"
          stroke="var(--rose)"
          strokeWidth={2.4}
          strokeLinecap="round"
          strokeLinejoin="round"
          filter="url(#pk-wiggle)"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 1.8, ease: "easeInOut" }}
        />
        {points.map((p, i) => {
          const isPeak = i === peakIdx;
          return (
            <motion.circle
              key={i}
              cx={p.x}
              cy={p.y}
              r={isPeak ? 9 : 7}
              fill={isPeak ? "var(--rose-deep)" : "var(--wine)"}
              stroke="var(--ink)"
              strokeWidth={isPeak ? 2 : 1.5}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{
                delay: 1.2 + i * 0.12,
                type: "spring",
                stiffness: 300,
                damping: 20,
              }}
            />
          );
        })}
        {points.map((p, i) => (
          <text
            key={`t-${i}`}
            x={p.x}
            y={height - 8}
            textAnchor="middle"
            fill="var(--ink-soft)"
            style={{
              fontFamily: "var(--font-elite), monospace",
              fontSize: 10,
              letterSpacing: ".1em",
            }}
          >
            {p.time}
          </text>
        ))}
        {points.map((p, i) => (
          <text
            key={`lbl-${i}`}
            x={p.x}
            y={18}
            textAnchor="middle"
            fill="var(--ink)"
            style={{
              fontFamily: "var(--font-caveat), cursive",
              fontWeight: 500,
              fontSize: 16,
            }}
          >
            {p.label}
          </text>
        ))}
      </svg>
      {plan.emotional_arc_text && (
        <div
          className="mt-3 text-center"
          style={{
            fontFamily: "var(--font-playfair), serif",
            fontStyle: "italic",
            fontSize: 17,
            color: "var(--ink-soft)",
            lineHeight: 1.45,
          }}
        >
          {plan.emotional_arc_text}
        </div>
      )}
    </section>
  );
}
