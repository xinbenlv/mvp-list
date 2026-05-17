"use client";

import { motion } from "framer-motion";

interface PullQuoteProps {
  text: string;
  meta: string;
}

export function PullQuote({ text, meta }: PullQuoteProps) {
  return (
    <motion.section
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.9, ease: "easeOut" }}
      className="relative overflow-hidden px-[50px] py-[100px] text-center max-md:px-6 max-md:py-[50px]"
      style={{ background: "var(--jet)", color: "var(--ivory)" }}
    >
      <div
        className="absolute left-0 right-0 top-0 h-[6px]"
        style={{ background: "var(--red)" }}
      />
      <div
        className="mb-6"
        style={{
          fontFamily: "var(--font-bodoni), serif",
          fontStyle: "italic",
          fontSize: 140,
          color: "var(--red)",
          lineHeight: 0.4,
        }}
      >
        “
      </div>
      <p
        className="mx-auto mb-[22px] max-md:text-[28px]"
        style={{
          fontFamily: "var(--font-bodoni), serif",
          fontStyle: "italic",
          fontSize: 48,
          lineHeight: 1.25,
          maxWidth: 920,
          color: "var(--ivory)",
          letterSpacing: "-.02em",
        }}
      >
        {text}
      </p>
      <div
        style={{
          fontFamily: "var(--font-jetbrains), monospace",
          fontSize: 10,
          letterSpacing: ".4em",
          textTransform: "uppercase",
          color: "var(--red)",
          fontWeight: 700,
        }}
      >
        {meta}
      </div>
    </motion.section>
  );
}
