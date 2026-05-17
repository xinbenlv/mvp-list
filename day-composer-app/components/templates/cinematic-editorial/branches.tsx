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
      className="px-[50px] py-[90px] max-md:px-6 max-md:py-[50px]"
      style={{ background: "var(--ivory)", borderTop: "1px solid var(--hairline)" }}
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
        — Editor’s Notes · Adaptive Branches
      </div>
      <h2
        className="mb-[50px] max-md:text-[40px]"
        style={{
          fontFamily: "var(--font-bodoni), serif",
          fontWeight: 900,
          fontSize: 68,
          letterSpacing: "-.04em",
          lineHeight: 0.95,
          color: "var(--jet)",
        }}
      >
        <em style={{ fontStyle: "italic", fontWeight: 400 }}>If the day</em>{" "}
        <span style={{ color: "var(--red)" }}>bends.</span>
      </h2>
      <div className="mx-auto grid max-w-[1300px] grid-cols-2 gap-10 max-md:grid-cols-1">
        {branches.map((b, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.6, delay: i * 0.15, ease: "easeOut" }}
            className="relative p-9"
            style={{
              background: "var(--jet)",
              color: "var(--ivory)",
              borderLeft: "6px solid var(--red)",
            }}
          >
            <div
              className="absolute left-[30px] top-[-12px] px-3"
              style={{
                background: "var(--jet)",
                color: "var(--red)",
                fontFamily: "var(--font-jetbrains), monospace",
                fontSize: 9,
                letterSpacing: ".36em",
                fontWeight: 700,
              }}
            >
              {`ALTERNATE ${String.fromCharCode(65 + i)}`}
            </div>
            <div
              className="mb-4"
              style={{
                fontFamily: "var(--font-bodoni), serif",
                fontStyle: "italic",
                fontSize: 28,
                color: "var(--ivory)",
                letterSpacing: "-.01em",
              }}
            >
              If {b.condition}
            </div>
            <div
              style={{
                fontFamily: "var(--font-dm-sans), sans-serif",
                fontSize: 15,
                lineHeight: 1.7,
                color: "var(--whisper)",
                fontWeight: 300,
              }}
            >
              <span style={{ color: "var(--red)", fontWeight: 700, fontSize: 18 }}>→ </span>
              {b.alternative}
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
