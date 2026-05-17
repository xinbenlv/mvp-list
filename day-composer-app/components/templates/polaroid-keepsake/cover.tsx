"use client";

import { motion } from "framer-motion";
import type { TripContext, TripPlan } from "@/lib/types/trip-plan";
import { formatMoodTag } from "@/lib/utils/format-logistics";

const EASE_EXPO: [number, number, number, number] = [0.16, 1, 0.3, 1];

interface CoverProps {
  plan: TripPlan;
  tripContext?: TripContext;
}

export function Cover({ plan, tripContext }: CoverProps) {
  return (
    <motion.section
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.2, ease: EASE_EXPO }}
      className="relative mx-auto mb-20 max-w-[760px] px-10 py-[60px] text-center"
      style={{
        background: "rgba(250,244,234,.55)",
        border: "1px solid rgba(43,35,43,.15)",
        boxShadow: "0 6px 30px -10px rgba(43,35,43,.18)",
      }}
    >
      <div
        className="absolute left-1/2 top-[-12px] h-6 w-[120px]"
        style={{
          transform: "translateX(-50%) rotate(-3deg)",
          background: "var(--tape-rose)",
          boxShadow: "0 2px 4px rgba(0,0,0,.08)",
        }}
      />
      <div
        className="absolute right-8 top-[30px] flex h-[110px] w-[110px] flex-col items-center justify-center rounded-full text-center"
        style={{
          border: "3px solid var(--wine)",
          color: "var(--wine)",
          fontFamily: "var(--font-elite), monospace",
          transform: "rotate(-15deg)",
          opacity: 0.78,
          lineHeight: 1.1,
        }}
      >
        <div style={{ fontSize: 9, letterSpacing: ".3em" }}>DAY · NO</div>
        <div style={{ fontSize: 22, fontWeight: 700, margin: "4px 0", letterSpacing: ".05em" }}>001</div>
        <div style={{ fontSize: 8, letterSpacing: ".2em" }}>COMPOSED</div>
      </div>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 0.2, ease: EASE_EXPO }}
        className="mb-[30px]"
        style={{
          fontFamily: "var(--font-elite), monospace",
          fontSize: 11,
          letterSpacing: ".4em",
          textTransform: "uppercase",
          color: "var(--rose-deep)",
        }}
      >
        Travel Journal · Vol. I
      </motion.div>
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 0.4, ease: EASE_EXPO }}
        className="mb-5"
        style={{
          fontFamily: "var(--font-playfair), serif",
          fontStyle: "italic",
          fontWeight: 400,
          fontSize: "clamp(40px, 6vw, 64px)",
          lineHeight: 1.05,
          color: "var(--ink)",
          letterSpacing: "-.01em",
        }}
      >
        {plan.day_theme}
      </motion.h1>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.2, delay: 0.7, ease: EASE_EXPO }}
        className="mx-0 my-[14px] mb-6"
        style={{
          fontFamily: "var(--font-caveat), cursive",
          fontWeight: 500,
          fontSize: 32,
          color: "var(--sage)",
          transform: "rotate(-1deg)",
        }}
      >
        recovering, but alive
      </motion.div>
      <div className="my-5 flex flex-wrap justify-center gap-[10px]">
        {plan.mood_tags.map((tag, i) => (
          <motion.span
            key={tag}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.9 + i * 0.08, ease: EASE_EXPO }}
            className="px-[14px]"
            style={{
              fontFamily: "var(--font-caveat), cursive",
              fontWeight: 500,
              fontSize: 20,
              color: "var(--rose-deep)",
            }}
          >
            {formatMoodTag(tag)}
            {i < plan.mood_tags.length - 1 && (
              <span className="ml-[14px] opacity-50">·</span>
            )}
          </motion.span>
        ))}
      </div>
      {tripContext && (
        <div
          className="flex flex-wrap justify-around gap-[14px] pt-6"
          style={{
            fontFamily: "var(--font-elite), monospace",
            fontSize: 12,
            letterSpacing: ".18em",
            textTransform: "uppercase",
            color: "var(--ink-soft)",
            borderTop: "1px dashed var(--ink-soft)",
          }}
        >
          <span>{tripContext.date_label}</span>
          <span>{tripContext.time_window}</span>
          <span>{tripContext.origin}</span>
          <span>{tripContext.companions.join(" ")}</span>
        </div>
      )}
    </motion.section>
  );
}
