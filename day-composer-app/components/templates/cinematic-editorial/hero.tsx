"use client";

import { motion } from "framer-motion";
import type { TripContext, TripPlan } from "@/lib/types/trip-plan";
import { formatMoodTag } from "@/lib/utils/format-logistics";

const EASE_EXPO: [number, number, number, number] = [0.16, 1, 0.3, 1];

interface HeroProps {
  plan: TripPlan;
  tripContext?: TripContext;
}

export function Hero({ plan, tripContext }: HeroProps) {
  return (
    <section
      className="relative flex flex-col justify-end overflow-hidden px-[50px] pb-[70px] pt-[60px] max-md:px-6 max-md:pb-[60px] max-md:pt-10"
      style={{
        height: "100vh",
        minHeight: 720,
        background: "linear-gradient(155deg,#1c2028 0%,#0a0d12 55%,#000 100%)",
        color: "var(--ivory)",
      }}
    >
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background: `
            radial-gradient(ellipse at 75% 25%,rgba(221,15,44,.18) 0%,transparent 50%),
            radial-gradient(ellipse at 25% 75%,rgba(255,255,255,.06) 0%,transparent 55%)
          `,
        }}
      />
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            "linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,0) 60%,rgba(0,0,0,.7) 100%)",
        }}
      />
      <div className="relative z-[2] max-w-[1200px]">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, delay: 0.2, ease: EASE_EXPO }}
          className="mb-9 flex items-center gap-[18px]"
          style={{
            fontFamily: "var(--font-jetbrains), monospace",
            fontSize: 10,
            letterSpacing: ".5em",
            color: "var(--ivory)",
            textTransform: "uppercase",
          }}
        >
          <span
            className="inline-block h-[1px] w-[60px]"
            style={{ background: "var(--red)" }}
          />
          {tripContext?.origin ?? "Bay Area"} ·{" "}
          <em style={{ color: "var(--red)", fontStyle: "normal" }}>A Saturday Spread</em> · Look 01
        </motion.div>
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.2, delay: 0.35, ease: EASE_EXPO }}
          style={{
            fontFamily: "var(--font-bodoni), serif",
            fontWeight: 900,
            fontSize: "clamp(56px,10vw,180px)",
            lineHeight: 0.92,
            letterSpacing: "-.045em",
            marginBottom: 30,
            color: "var(--ivory)",
          }}
        >
          {plan.day_theme}
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.2, delay: 0.6, ease: EASE_EXPO }}
          className="mb-10"
          style={{
            fontFamily: "var(--font-bodoni), serif",
            fontStyle: "italic",
            fontSize: 24,
            lineHeight: 1.4,
            maxWidth: 640,
            color: "var(--ivory)",
          }}
        >
          {plan.mood_tags.map(formatMoodTag).join(" · ")}. {plan.stops.length} stops, one arc.
        </motion.p>
        <div
          className="flex flex-wrap gap-x-[50px] gap-y-6 border-t pt-6"
          style={{
            borderColor: "rgba(248,246,240,.25)",
            fontFamily: "var(--font-jetbrains), monospace",
            fontSize: 10,
            letterSpacing: ".2em",
            textTransform: "uppercase",
            color: "var(--silver)",
          }}
        >
          {tripContext && (
            <>
              <div>
                <span>Date</span>
                <b className="mt-1 block" style={{ color: "var(--ivory)", fontSize: 15, fontFamily: "var(--font-bodoni), serif", fontWeight: 700, textTransform: "none", letterSpacing: "-.01em" }}>
                  {tripContext.date_label}
                </b>
              </div>
              <div>
                <span>Window</span>
                <b className="mt-1 block" style={{ color: "var(--ivory)", fontSize: 15, fontFamily: "var(--font-bodoni), serif", fontWeight: 700, textTransform: "none", letterSpacing: "-.01em" }}>
                  {tripContext.time_window}
                </b>
              </div>
              <div>
                <span>Origin</span>
                <b className="mt-1 block" style={{ color: "var(--ivory)", fontSize: 15, fontFamily: "var(--font-bodoni), serif", fontWeight: 700, textTransform: "none", letterSpacing: "-.01em" }}>
                  {tripContext.origin}
                </b>
              </div>
              <div>
                <span>Company</span>
                <b className="mt-1 block" style={{ color: "var(--ivory)", fontSize: 15, fontFamily: "var(--font-bodoni), serif", fontWeight: 700, textTransform: "none", letterSpacing: "-.01em" }}>
                  {tripContext.companions.join(" · ")}
                </b>
              </div>
            </>
          )}
        </div>
      </div>
    </section>
  );
}
