"use client";

import { motion } from "framer-motion";
import { useMemo } from "react";
import type { TripPlan } from "@/lib/types/trip-plan";
import { buildArcPath } from "@/lib/utils/arc-path";
import { deriveArc, peakIndex } from "@/lib/utils/derive-arc";

const ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"];

interface TocProps {
  plan: TripPlan;
}

export function Toc({ plan }: TocProps) {
  const width = 1000;
  const height = 180;
  const arc = useMemo(
    () => deriveArc(plan.stops, plan.theme_anchor),
    [plan.stops, plan.theme_anchor],
  );
  const { pathD, points } = buildArcPath(arc, width, height, {
    top: 30,
    bottom: 40,
    left: 125,
    right: 125,
  });
  const peakIdx = peakIndex(arc);

  return (
    <section
      className="relative px-[50px] py-[90px] max-md:px-6 max-md:py-[50px]"
      style={{ background: "var(--ivory)" }}
    >
      <div
        className="mb-[10px]"
        style={{
          fontFamily: "var(--font-jetbrains), monospace",
          fontSize: 10,
          letterSpacing: ".4em",
          textTransform: "uppercase",
          color: "var(--red)",
          fontWeight: 700,
        }}
      >
        — Table of Contents
      </div>
      <h2
        className="mb-[60px] max-md:text-[54px]"
        style={{
          fontFamily: "var(--font-bodoni), serif",
          fontWeight: 900,
          fontSize: 88,
          letterSpacing: "-.04em",
          lineHeight: 0.95,
          color: "var(--jet)",
        }}
      >
        {plan.stops.length} <em style={{ fontStyle: "italic", fontWeight: 400 }}>movements,</em>
        <br />
        one <span style={{ color: "var(--red)" }}>day.</span>
      </h2>
      <div className="grid max-w-[1300px] grid-cols-2 items-start gap-[60px] max-md:grid-cols-1 max-md:gap-[30px]">
        <div
          className="relative p-10"
          style={{
            background: "var(--jet)",
            color: "var(--ivory)",
            borderLeft: "6px solid var(--red)",
          }}
        >
          <div
            className="absolute left-6 top-[-9px] px-[10px]"
            style={{
              background: "var(--jet)",
              color: "var(--red)",
              fontFamily: "var(--font-jetbrains), monospace",
              fontSize: 9,
              letterSpacing: ".32em",
              fontWeight: 700,
            }}
          >
            EMOTIONAL ARC
          </div>
          <svg
            viewBox={`0 0 ${width} ${height}`}
            preserveAspectRatio="none"
            className="block h-[180px] w-full"
          >
            <motion.path
              d={pathD}
              fill="none"
              stroke="var(--ivory)"
              strokeWidth={1.8}
              initial={{ pathLength: 0 }}
              whileInView={{ pathLength: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 1.8, ease: "easeInOut" }}
            />
            {points.map((p, i) => {
              const isPeak = i === peakIdx;
              return (
                <motion.circle
                  key={i}
                  cx={p.x}
                  cy={p.y}
                  r={isPeak ? 12 : 8}
                  fill={isPeak ? "var(--red)" : "var(--jet)"}
                  stroke="var(--ivory)"
                  strokeWidth={2}
                  initial={{ scale: 0 }}
                  whileInView={{ scale: 1 }}
                  viewport={{ once: true }}
                  transition={{
                    delay: 0.8 + i * 0.12,
                    type: "spring",
                    stiffness: 300,
                    damping: 22,
                  }}
                />
              );
            })}
            {points.map((p, i) => (
              <text
                key={`lbl-${i}`}
                x={p.x}
                y={18}
                textAnchor="middle"
                fill="var(--ivory)"
                style={{
                  fontFamily: "var(--font-bodoni), serif",
                  fontStyle: "italic",
                  fontSize: 13,
                }}
              >
                {p.label}
              </text>
            ))}
            {points.map((p, i) => (
              <text
                key={`t-${i}`}
                x={p.x}
                y={height - 6}
                textAnchor="middle"
                fill="var(--silver)"
                style={{
                  fontFamily: "var(--font-jetbrains), monospace",
                  fontSize: 9,
                  letterSpacing: ".14em",
                  textTransform: "uppercase",
                }}
              >
                {p.time}
              </text>
            ))}
          </svg>
          {plan.emotional_arc_text && (
            <div
              className="mt-3"
              style={{
                fontFamily: "var(--font-bodoni), serif",
                fontStyle: "italic",
                fontSize: 14,
                color: "var(--whisper)",
                lineHeight: 1.5,
              }}
            >
              {plan.emotional_arc_text}
            </div>
          )}
        </div>
        <div
          className="flex flex-col"
          style={{ borderTop: "3px solid var(--jet)" }}
        >
          {plan.stops.map((stop, i) => (
            <a
              key={i}
              href={`#s${i + 1}`}
              className="grid items-baseline gap-6 py-[22px] transition-[padding] hover:pl-[14px]"
              style={{
                gridTemplateColumns: "70px 1fr auto",
                borderBottom: "1px solid var(--hairline)",
                color: "var(--jet)",
                textDecoration: "none",
              }}
            >
              <div
                style={{
                  fontFamily: "var(--font-bodoni), serif",
                  fontStyle: "italic",
                  fontWeight: 400,
                  fontSize: 42,
                  color: "var(--red)",
                  lineHeight: 0.85,
                }}
              >
                {ROMAN[i] ?? `${i + 1}`}
              </div>
              <div>
                <h4
                  style={{
                    fontFamily: "var(--font-bodoni), serif",
                    fontWeight: 700,
                    fontSize: 24,
                    lineHeight: 1.1,
                    letterSpacing: "-.01em",
                    marginBottom: 4,
                  }}
                >
                  {stop.place_name}
                </h4>
                <p
                  style={{
                    fontFamily: "var(--font-jetbrains), monospace",
                    fontSize: 10,
                    letterSpacing: ".16em",
                    textTransform: "uppercase",
                    color: "var(--ash)",
                  }}
                >
                  {stop.place_id}
                </p>
              </div>
              <div
                style={{
                  fontFamily: "var(--font-jetbrains), monospace",
                  fontSize: 12,
                  letterSpacing: ".14em",
                  color: "var(--red)",
                  fontWeight: 700,
                }}
              >
                {stop.time}
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
