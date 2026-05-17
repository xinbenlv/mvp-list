"use client";

import { motion } from "framer-motion";
import type { TripPlan } from "@/lib/types/trip-plan";
import { buildArcPath } from "@/lib/utils/arc-path";
import { deriveArc } from "@/lib/utils/derive-arc";

interface ArcCardProps {
  plan: TripPlan;
}

export function ArcCard({ plan }: ArcCardProps) {
  const width = 1000;
  const height = 200;
  const arc = deriveArc(plan.stops, plan.theme_anchor);
  const { pathD, points } = buildArcPath(arc, width, height, {
    top: 30,
    bottom: 50,
    left: 125,
    right: 125,
  });

  // Area path: close to bottom
  const areaD = pathD
    ? `${pathD} L ${points[points.length - 1]?.x},${height} L ${points[0]?.x},${height} Z`
    : "";

  const NODE_COLORS = ["#FFBCBC", "#FFD3B6", "#C97B8C", "#D4E4D4"];

  return (
    <section className="px-10 py-20 text-center max-md:py-12">
      <div
        className="mb-4"
        style={{
          fontFamily: "var(--font-dm-mono), monospace",
          fontSize: 10,
          letterSpacing: ".32em",
          textTransform: "uppercase",
          color: "var(--accent-deep)",
        }}
      >
        The Shape of the Day
      </div>
      <h2
        className="mb-[50px]"
        style={{
          fontFamily: "var(--font-cormorant), serif",
          fontStyle: "italic",
          fontWeight: 300,
          fontSize: 44,
          color: "var(--ink)",
          letterSpacing: "-.01em",
        }}
      >
        a slow rise,{" "}
        <em style={{ color: "var(--accent-deep)" }}>a peak</em>, a soft fall
      </h2>
      <div
        className="relative mx-auto max-w-[1000px] rounded-[36px] border p-10 max-md:rounded-3xl max-md:p-5"
        style={{
          background: "rgba(255,255,255,.5)",
          backdropFilter: "blur(24px)",
          borderColor: "rgba(255,255,255,.7)",
          boxShadow: "0 30px 80px -30px rgba(201,123,140,.3)",
        }}
      >
        <svg
          viewBox={`0 0 ${width} ${height}`}
          preserveAspectRatio="none"
          className="block h-[200px] w-full"
        >
          <defs>
            <linearGradient id="au-arcGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#FFD3B6" />
              <stop offset="35%" stopColor="#F8C8DC" />
              <stop offset="65%" stopColor="#C97B8C" />
              <stop offset="100%" stopColor="#D4E4D4" />
            </linearGradient>
            <filter id="au-glow">
              <feGaussianBlur stdDeviation="4" />
              <feMerge>
                <feMergeNode />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          <motion.path
            d={areaD}
            fill="url(#au-arcGrad)"
            opacity={0.18}
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 0.18 }}
            viewport={{ once: true }}
            transition={{ duration: 1.5 }}
          />
          <motion.path
            d={pathD}
            fill="none"
            stroke="url(#au-arcGrad)"
            strokeWidth={2.8}
            filter="url(#au-glow)"
            initial={{ pathLength: 0 }}
            whileInView={{ pathLength: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 1.8, ease: "easeInOut" }}
          />
          {points.map((p, i) => (
            <motion.circle
              key={i}
              cx={p.x}
              cy={p.y}
              r={i === 2 ? 14 : 11}
              fill={NODE_COLORS[i % NODE_COLORS.length]}
              filter="url(#au-glow)"
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
          ))}
          {points.map((p, i) => (
            <text
              key={`lbl-${i}`}
              x={p.x}
              y={20}
              textAnchor="middle"
              fill="var(--accent-deep)"
              style={{
                fontFamily: "var(--font-cormorant), serif",
                fontStyle: "italic",
                fontSize: 16,
              }}
            >
              {p.label}
            </text>
          ))}
          {points.map((p, i) => {
            const time = plan.stops[i]?.time ?? "";
            return (
              <text
                key={`t-${i}`}
                x={p.x}
                y={height - 10}
                textAnchor="middle"
                fill="var(--ink-soft)"
                style={{
                  fontFamily: "var(--font-dm-mono), monospace",
                  fontSize: 10,
                  letterSpacing: ".18em",
                  textTransform: "uppercase",
                }}
              >
                {time}
              </text>
            );
          })}
        </svg>
      </div>
    </section>
  );
}
