"use client";

import { motion } from "framer-motion";
import type { Stop } from "@/lib/types/trip-plan";
import { formatLogisticsChips } from "@/lib/utils/format-logistics";

const ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"];
const PACING_LABEL: Record<string, string> = {
  opening: "Opening",
  breathing: "Breathing",
  peak: "Peak",
  recovery: "Recovery",
  closing: "Closing",
};

const IMG_GRADIENTS = [
  "linear-gradient(155deg,#3a4554 0%,#1a2330 50%,#000 100%)",
  "linear-gradient(155deg,#3a5560 0%,#152830 50%,#000 100%)",
  "linear-gradient(155deg,#7a0a1c 0%,#3a0510 50%,#000 100%)",
  "linear-gradient(155deg,#1a1f30 0%,#0a0d18 60%,#000 100%)",
];

interface SpreadProps {
  stop: Stop;
  index: number;
  pacingLabel?: string;
  arcVibe?: number | null;
}

export function Spread({ stop, index, pacingLabel, arcVibe }: SpreadProps) {
  const isFlip = index % 2 === 1;
  const chips = formatLogisticsChips(stop.logistics);
  const eyebrow = pacingLabel
    ? PACING_LABEL[pacingLabel] ?? pacingLabel
    : "Movement";
  return (
    <motion.section
      id={`s${index + 1}`}
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.9, ease: [0.25, 0.46, 0.45, 0.94] }}
      className="relative px-[50px] pb-[90px] pt-[100px] max-md:px-6 max-md:py-[50px]"
      style={{ background: "var(--ivory)", borderTop: "1px solid var(--hairline)" }}
    >
      <div
        className="absolute left-[50px] top-[30px] max-md:left-6"
        style={{
          fontFamily: "var(--font-jetbrains), monospace",
          fontSize: 10,
          letterSpacing: ".36em",
          textTransform: "uppercase",
          color: "var(--ash)",
        }}
      >
        <strong
          style={{
            color: "var(--red)",
            fontFamily: "var(--font-bodoni), serif",
            fontStyle: "italic",
            fontSize: 20,
            letterSpacing: 0,
            marginRight: 6,
            fontWeight: 700,
            textTransform: "none",
          }}
        >
          {ROMAN[index] ?? `${index + 1}`}
        </strong>
        Movement {ROMAN[index]?.toUpperCase()} of {ROMAN[3]?.toUpperCase() ?? "IV"}
      </div>
      <div
        className={`mx-auto mt-[30px] grid max-w-[1300px] items-center gap-[70px] max-md:grid-cols-1 max-md:gap-[30px]`}
        style={{ gridTemplateColumns: "1fr 1fr" }}
      >
        <div
          className={`relative flex aspect-[3/4] items-end overflow-hidden p-9 max-md:order-1 ${
            isFlip ? "md:order-2" : ""
          }`}
          style={{
            background: stop.image_url
              ? `url(${stop.image_url}) center/cover`
              : IMG_GRADIENTS[index % IMG_GRADIENTS.length],
            color: "var(--ivory)",
          }}
        >
          <div
            className="pointer-events-none absolute inset-0"
            style={{
              background:
                "radial-gradient(ellipse at 30% 30%,transparent 30%,rgba(0,0,0,.55) 100%)",
            }}
          />
          <div
            className="absolute left-6 top-6 z-[3] px-[10px] py-[5px]"
            style={{
              fontFamily: "var(--font-jetbrains), monospace",
              fontSize: 9,
              letterSpacing: ".32em",
              textTransform: "uppercase",
              color: "var(--ivory)",
              background: "rgba(10,10,10,.6)",
              backdropFilter: "blur(8px)",
              borderLeft: "2px solid var(--red)",
            }}
          >
            Look 0{index + 1}
          </div>
          <div
            className="relative z-[2]"
            style={{
              fontFamily: "var(--font-jetbrains), monospace",
              fontSize: 10,
              letterSpacing: ".2em",
              textTransform: "uppercase",
              color: "var(--silver)",
            }}
          >
            <em
              className="mb-2 block"
              style={{
                fontFamily: "var(--font-bodoni), serif",
                fontStyle: "italic",
                fontWeight: 400,
                fontSize: 32,
                lineHeight: 1.05,
                letterSpacing: "-.01em",
                textTransform: "none",
                color: "var(--ivory)",
                textShadow: "0 2px 16px rgba(0,0,0,.6)",
              }}
            >
              “{stop.one_liner}”
            </em>
            {stop.place_name}
          </div>
        </div>
        <div className="py-[10px]">
          <div
            className="mb-[14px]"
            style={{
              fontFamily: "var(--font-jetbrains), monospace",
              fontSize: 10,
              letterSpacing: ".4em",
              textTransform: "uppercase",
              color: "var(--red)",
              fontWeight: 700,
            }}
          >
            {eyebrow}
            {arcVibe != null ? ` · ${Math.round(arcVibe * 100)}` : ""}
          </div>
          <div
            className="mb-[18px] inline-block"
            style={{
              fontFamily: "var(--font-bodoni), serif",
              fontWeight: 900,
              fontSize: 80,
              color: "var(--jet)",
              lineHeight: 0.85,
              letterSpacing: "-.04em",
            }}
          >
            {stop.time}
            <span
              className="mt-[14px] block h-1 w-[60px]"
              style={{ background: "var(--red)" }}
            />
          </div>
          <h2
            className="mb-[18px] max-md:text-4xl"
            style={{
              fontFamily: "var(--font-bodoni), serif",
              fontWeight: 700,
              fontSize: 46,
              lineHeight: 1.02,
              letterSpacing: "-.025em",
              color: "var(--jet)",
            }}
          >
            {stop.place_name}
          </h2>
          {stop.one_liner && (
            <div
              className="mb-6 pl-[14px]"
              style={{
                fontFamily: "var(--font-bodoni), serif",
                fontStyle: "italic",
                fontSize: 18,
                lineHeight: 1.55,
                color: "var(--ash)",
                borderLeft: "3px solid var(--red)",
              }}
            >
              {stop.one_liner}
            </div>
          )}
          <p
            className="mb-6"
            style={{ fontSize: 16, lineHeight: 1.85, color: "#1a1a1a", maxWidth: 540 }}
          >
            {stop.why_fits_today}
          </p>
          {chips.length > 0 && (
            <div
              className="mb-5 flex flex-wrap max-w-fit"
              style={{ border: "1px solid var(--jet)" }}
            >
              {chips.map((c, i) => (
                <span
                  key={i}
                  className="px-[14px] py-[6px]"
                  style={{
                    fontFamily: "var(--font-jetbrains), monospace",
                    fontSize: 10,
                    letterSpacing: ".14em",
                    textTransform: "uppercase",
                    background: "var(--ivory)",
                    color: "var(--jet)",
                    borderRight: i === chips.length - 1 ? "none" : "1px solid var(--jet)",
                  }}
                >
                  {c}
                </span>
              ))}
            </div>
          )}
          {stop.tip && (
            <p
              className="my-[14px] pl-[14px]"
              style={{
                fontFamily: "var(--font-bodoni), serif",
                fontStyle: "italic",
                fontSize: 16,
                color: "var(--red)",
                borderLeft: "2px solid var(--red)",
                lineHeight: 1.5,
              }}
            >
              {stop.tip}
            </p>
          )}
        </div>
      </div>
    </motion.section>
  );
}
