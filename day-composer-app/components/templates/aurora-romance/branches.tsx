"use client";

import { motion } from "framer-motion";
import type { AdaptiveBranch } from "@/lib/types/trip-plan";

interface BranchesProps {
  branches: AdaptiveBranch[];
}

export function Branches({ branches }: BranchesProps) {
  if (branches.length === 0) return null;
  return (
    <section className="mx-auto mb-[100px] mt-[60px] max-w-[920px] px-10 max-md:px-6">
      <h3
        className="text-center"
        style={{
          fontFamily: "var(--font-cormorant), serif",
          fontStyle: "italic",
          fontWeight: 300,
          fontSize: 40,
          color: "var(--ink)",
          marginBottom: 8,
        }}
      >
        if the day <em style={{ color: "var(--accent-deep)" }}>bends</em>
      </h3>
      <div
        className="mb-10 text-center"
        style={{
          fontFamily: "var(--font-dm-mono), monospace",
          fontSize: 10,
          letterSpacing: ".32em",
          textTransform: "uppercase",
          color: "var(--accent-deep)",
        }}
      >
        — adaptive branches —
      </div>
      {branches.map((b, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.6, delay: i * 0.15, ease: "easeOut" }}
          className="relative mb-4 grid items-center gap-7 overflow-hidden rounded-3xl border p-8 max-md:grid-cols-1 max-md:gap-[10px]"
          style={{
            gridTemplateColumns: "auto 1fr",
            background: "rgba(255,255,255,.55)",
            backdropFilter: "blur(18px)",
            borderColor: "rgba(255,255,255,.7)",
            boxShadow: "0 10px 30px -15px rgba(201,123,140,.25)",
          }}
        >
          <div
            className="pointer-events-none absolute right-[-30px] top-[-30px] h-20 w-20"
            style={{
              background:
                i === 0
                  ? "radial-gradient(circle,var(--rose) 0%,transparent 70%)"
                  : "radial-gradient(circle,var(--sage-mist) 0%,transparent 70%)",
              opacity: 0.3,
            }}
          />
          <div
            className="relative z-[1] min-w-[200px] max-md:min-w-0"
            style={{
              fontFamily: "var(--font-cormorant), serif",
              fontStyle: "italic",
              fontWeight: 400,
              fontSize: 22,
              color: "var(--accent-deep)",
            }}
          >
            if {b.condition}
          </div>
          <div
            className="relative z-[1]"
            style={{
              fontSize: 15,
              lineHeight: 1.7,
              color: "var(--ink)",
              fontWeight: 300,
            }}
          >
            <span
              style={{
                color: "var(--accent)",
                fontFamily: "var(--font-cormorant), serif",
                fontStyle: "italic",
                fontSize: 24,
                marginRight: 6,
              }}
            >
              →
            </span>
            {b.alternative}
          </div>
        </motion.div>
      ))}
    </section>
  );
}
