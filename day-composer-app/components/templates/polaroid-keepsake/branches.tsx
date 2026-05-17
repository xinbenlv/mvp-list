"use client";

import { motion } from "framer-motion";
import type { AdaptiveBranch } from "@/lib/types/trip-plan";

interface BranchesProps {
  branches: AdaptiveBranch[];
}

export function Branches({ branches }: BranchesProps) {
  if (branches.length === 0) return null;
  return (
    <section
      className="relative mx-auto mb-[60px] mt-20 max-w-[760px] p-[30px]"
      style={{
        background: "rgba(250,244,234,.5)",
        border: "1px solid rgba(43,35,43,.15)",
        transform: "rotate(.4deg)",
        boxShadow: "0 6px 24px -10px rgba(43,35,43,.16)",
      }}
    >
      <div
        className="absolute left-1/2 top-[-10px] h-[22px] w-[110px]"
        style={{
          transform: "translateX(-50%) rotate(-2deg)",
          background: "var(--tape-rose)",
        }}
      />
      <h3
        className="mb-[6px] text-center"
        style={{
          fontFamily: "var(--font-playfair), serif",
          fontStyle: "italic",
          fontSize: 32,
          color: "var(--ink)",
        }}
      >
        If the day bends
      </h3>
      <div
        className="mb-6 text-center"
        style={{
          fontFamily: "var(--font-elite), monospace",
          fontSize: 10,
          letterSpacing: ".3em",
          textTransform: "uppercase",
          color: "var(--rose-deep)",
        }}
      >
        — adaptive notes —
      </div>
      {branches.map((b, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-40px" }}
          transition={{ duration: 0.6, delay: i * 0.15, ease: "easeOut" }}
          className="grid items-center gap-6 py-[18px] max-md:grid-cols-1"
          style={{
            gridTemplateColumns: "auto 1fr",
            borderTop: i === 0 ? "none" : "1px dashed var(--ink-soft)",
          }}
        >
          <div
            className="min-w-[170px]"
            style={{
              fontFamily: "var(--font-caveat), cursive",
              fontWeight: 600,
              fontSize: 24,
              color: "var(--wine)",
              lineHeight: 1.2,
              transform: "rotate(-1deg)",
            }}
          >
            if {b.condition}
          </div>
          <div
            style={{
              fontSize: 15,
              lineHeight: 1.6,
              color: "var(--ink)",
              fontFamily: "var(--font-crimson), serif",
            }}
          >
            <span style={{ color: "var(--rose-deep)", fontWeight: 700, fontSize: 18, marginRight: 8 }}>
              ➜
            </span>
            {b.alternative}
          </div>
        </motion.div>
      ))}
    </section>
  );
}
