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
      className="relative flex min-h-screen flex-col items-center justify-center px-10 pb-10 pt-20 text-center"
    >
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.4, delay: 0.2, ease: EASE_EXPO }}
        className="mb-8"
        style={{
          fontFamily: "var(--font-dm-mono), monospace",
          fontSize: 11,
          letterSpacing: ".36em",
          textTransform: "uppercase",
          color: "var(--accent-deep)",
        }}
      >
        {tripContext ? (
          <>
            <span className="mx-[14px] opacity-75">{tripContext.date_label}</span>
            ·
            <span className="mx-[14px] opacity-75">{tripContext.time_window}</span>
          </>
        ) : (
          <span>{plan.day_theme}</span>
        )}
      </motion.div>
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.6, delay: 0.4, ease: EASE_EXPO }}
        className="mb-9 max-md:text-[44px]"
        style={{
          fontFamily: "var(--font-cormorant), serif",
          fontStyle: "italic",
          fontWeight: 300,
          fontSize: "clamp(54px,9vw,128px)",
          lineHeight: 0.95,
          letterSpacing: "-.02em",
          maxWidth: 1000,
          backgroundImage:
            "linear-gradient(135deg,var(--ink) 0%,var(--accent) 50%,var(--accent-deep) 100%)",
          WebkitBackgroundClip: "text",
          backgroundClip: "text",
          color: "transparent",
        }}
      >
        {plan.day_theme}
      </motion.h1>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.4, delay: 0.8, ease: EASE_EXPO }}
        className="mb-7 flex max-w-[620px] flex-wrap justify-center gap-2"
      >
        {plan.mood_tags.map((tag, i) => (
          <span
            key={tag}
            className="rounded-full border px-4 py-[6px]"
            style={{
              fontFamily: "var(--font-dm-sans), sans-serif",
              fontWeight: 300,
              fontSize: 13,
              background:
                i === 0 ? "rgba(201,123,140,.25)" : "rgba(255,255,255,.55)",
              backdropFilter: "blur(8px)",
              borderColor: i === 0 ? "rgba(201,123,140,.35)" : "rgba(61,46,61,.08)",
              letterSpacing: ".04em",
              color: "var(--ink)",
            }}
          >
            {formatMoodTag(tag)}
          </span>
        ))}
      </motion.div>
      {tripContext && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.4, delay: 1, ease: EASE_EXPO }}
          className="max-w-[540px]"
          style={{
            fontFamily: "var(--font-cormorant), serif",
            fontStyle: "italic",
            fontWeight: 300,
            fontSize: 19,
            color: "var(--ink-soft)",
            letterSpacing: ".02em",
          }}
        >
          <span className="mx-[14px]">from {tripContext.origin},</span>
          <span className="mx-[14px]">with {tripContext.companions.join(", ")},</span>
          <span className="mx-[14px]">by {tripContext.vehicle}.</span>
        </motion.p>
      )}
      <div
        className="absolute bottom-10 left-1/2"
        style={{
          fontFamily: "var(--font-cormorant), serif",
          fontStyle: "italic",
          fontSize: 14,
          color: "var(--accent-deep)",
          opacity: 0.7,
          animation: "au-bob 3s ease-in-out infinite",
          transform: "translateX(-50%)",
        }}
      >
        ~ scroll, slowly ~
      </div>
    </section>
  );
}
