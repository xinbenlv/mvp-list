"use client";

import { motion } from "framer-motion";
import type { Stop } from "@/lib/types/trip-plan";
import { formatLogisticsChips } from "@/lib/utils/format-logistics";
import { MenuBlock } from "./menu-block";

interface StopPageProps {
  stop: Stop;
  index: number;
  isLast: boolean;
}

const POLAROID_GRADIENTS = [
  "linear-gradient(135deg,#E5B091 0%,#C28D8A 60%,#7E4F4F 100%)",
  "linear-gradient(135deg,#C8D4B8 0%,#9DAD93 55%,#5F7864 100%)",
  "linear-gradient(135deg,#D89A8A 0%,#A86E6B 50%,#6B3D49 100%)",
  "linear-gradient(135deg,#A77B85 0%,#6B3D49 60%,#2B232B 100%)",
];

const ROTATIONS = ["-2.5deg", "2deg", "-1.2deg", "1.5deg"];

const STAMP_LABELS = ["opening", "breathing", "peak", "closing"];
const STAMP_VARIANTS = ["rose", "sage", "default", "sage"] as const;

interface PolaroidProps {
  stop: Stop;
  index: number;
}

function Polaroid({ stop, index }: PolaroidProps) {
  const grad = POLAROID_GRADIENTS[index % POLAROID_GRADIENTS.length];
  const rotation = ROTATIONS[index % ROTATIONS.length];
  return (
    <div
      className="relative px-[18px] pb-[70px] pt-[18px] transition-transform duration-300 hover:rotate-0 hover:scale-[1.02]"
      style={{
        background: "var(--paper)",
        boxShadow:
          "0 14px 35px -8px rgba(43,35,43,.28),0 0 0 1px rgba(43,35,43,.05)",
        transform: `rotate(${rotation})`,
      }}
    >
      <div
        className="absolute left-1/2 top-[-12px] h-[22px] w-[90px]"
        style={{
          transform: "translateX(-50%) rotate(3deg)",
          background: "var(--tape-rose)",
          boxShadow: "0 1px 3px rgba(0,0,0,.06)",
        }}
      />
      <div
        className="relative flex aspect-square w-full items-end overflow-hidden p-6 text-white"
        style={{ background: grad }}
      >
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background:
              "radial-gradient(ellipse at center,transparent 30%,rgba(0,0,0,.35) 100%)",
          }}
        />
        <div
          className="relative z-[2]"
          style={{
            fontFamily: "var(--font-playfair), serif",
            fontStyle: "italic",
            fontSize: 34,
            lineHeight: 1,
            textShadow: "0 2px 12px rgba(0,0,0,.4)",
          }}
        >
          {stop.place_name}
        </div>
      </div>
      <div
        className="absolute bottom-[18px] left-[18px] right-[18px] text-center"
        style={{
          fontFamily: "var(--font-caveat), cursive",
          fontWeight: 500,
          fontSize: 22,
          color: "var(--ink)",
          lineHeight: 1.2,
          transform: "rotate(-1deg)",
        }}
      >
        {stop.place_name.toLowerCase()}
      </div>
      <div
        className="absolute bottom-[30px] right-6"
        style={{
          fontFamily: "var(--font-elite), monospace",
          fontSize: 9,
          letterSpacing: ".2em",
          color: "var(--ink-soft)",
          opacity: 0.6,
          textTransform: "uppercase",
        }}
      >
        Jan 10 · {stop.time}
      </div>
    </div>
  );
}

export function StopPage({ stop, index, isLast }: StopPageProps) {
  const isEven = index % 2 === 1; // 0-indexed: first stop = "odd page"
  const chips = formatLogisticsChips(stop.logistics);
  const stampLabel =
    STAMP_LABELS[index] ?? STAMP_LABELS[STAMP_LABELS.length - 1];
  const stampVariant = STAMP_VARIANTS[index] ?? STAMP_VARIANTS[0];

  return (
    <>
      <motion.section
        initial={{ opacity: 0, y: 24 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-80px" }}
        transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
        className="relative mx-auto mb-[120px] max-w-[880px] px-5 py-[30px]"
      >
        <div
          className="absolute left-1/2 top-[-14px] -translate-x-1/2 px-[14px]"
          style={{
            fontFamily: "var(--font-elite), monospace",
            fontSize: 11,
            letterSpacing: ".3em",
            color: "var(--ink-soft)",
            background: "var(--bone)",
            textTransform: "uppercase",
          }}
        >
          — Page {index + 1} —
        </div>
        <div
          className="grid items-start gap-[50px] max-md:grid-cols-1"
          style={{
            gridTemplateColumns: isEven ? "1.2fr 1fr" : "1fr 1.2fr",
          }}
        >
          {isEven ? (
            <>
              <Notes
                stop={stop}
                chips={chips}
                stampLabel={stampLabel}
                stampVariant={stampVariant}
              />
              <Polaroid stop={stop} index={index} />
            </>
          ) : (
            <>
              <Polaroid stop={stop} index={index} />
              <Notes
                stop={stop}
                chips={chips}
                stampLabel={stampLabel}
                stampVariant={stampVariant}
              />
            </>
          )}
        </div>
      </motion.section>
      {!isLast && stop.transition_to_next && (
        <div
          className="relative mx-auto mb-[50px] mt-[30px] max-w-[600px] px-0 py-[14px] text-center"
          style={{
            fontFamily: "var(--font-caveat), cursive",
            fontWeight: 500,
            fontSize: 22,
            color: "var(--ink-soft)",
            lineHeight: 1.3,
          }}
        >
          {stop.transition_to_next.split(/→|·/).map((seg, i, arr) => (
            <span key={i}>
              {seg.trim()}
              {i < arr.length - 1 && (
                <span
                  className="mx-2 inline-block"
                  style={{
                    fontFamily: "var(--font-playfair), serif",
                    fontStyle: "italic",
                    fontSize: 26,
                    color: "var(--rose-deep)",
                  }}
                >
                  ~
                </span>
              )}
            </span>
          ))}
          {stop.transition_drive_min != null && (
            <>
              <span
                className="mx-2 inline-block"
                style={{
                  fontFamily: "var(--font-playfair), serif",
                  fontStyle: "italic",
                  fontSize: 26,
                  color: "var(--rose-deep)",
                }}
              >
                ·
              </span>
              {stop.transition_drive_min} min drive
            </>
          )}
        </div>
      )}
    </>
  );
}

interface NotesProps {
  stop: Stop;
  chips: string[];
  stampLabel: string;
  stampVariant: "rose" | "sage" | "default";
}

function Notes({ stop, chips, stampLabel, stampVariant }: NotesProps) {
  const stampColor =
    stampVariant === "rose"
      ? "var(--rose-deep)"
      : stampVariant === "sage"
        ? "var(--sage)"
        : "var(--wine)";
  return (
    <div className="relative px-[6px] py-[14px]">
      <span
        style={{
          fontFamily: "var(--font-playfair), serif",
          fontWeight: 700,
          fontSize: 42,
          color: "var(--ink)",
          letterSpacing: "-.02em",
          lineHeight: 1,
          display: "inline-block",
        }}
      >
        {stop.time}
      </span>
      <span
        className="ml-[14px] inline-block px-2 py-[3px] align-middle"
        style={{
          fontFamily: "var(--font-elite), monospace",
          fontSize: 10,
          letterSpacing: ".25em",
          color: stampColor,
          textTransform: "uppercase",
          border: `1.5px solid ${stampColor}`,
          transform: "rotate(-3deg)",
          opacity: 0.85,
        }}
      >
        {stampLabel}
      </span>
      <h3
        style={{
          fontFamily: "var(--font-playfair), serif",
          fontStyle: "italic",
          fontSize: 30,
          lineHeight: 1.1,
          color: "var(--ink)",
          margin: "14px 0 6px",
        }}
      >
        {stop.place_name}
      </h3>
      {stop.one_liner && (
        <p
          className="mb-[18px]"
          style={{
            fontFamily: "var(--font-playfair), serif",
            fontStyle: "italic",
            fontSize: 17,
            lineHeight: 1.55,
            color: "var(--ink-soft)",
          }}
        >
          {stop.one_liner}
        </p>
      )}
      <p
        className="mb-[18px]"
        style={{
          fontSize: 16,
          lineHeight: 1.8,
          color: "var(--ink)",
          fontWeight: 400,
        }}
      >
        {stop.why_fits_today}
      </p>
      {stop.tip && (
        <p
          className="my-[14px]"
          style={{
            fontFamily: "var(--font-caveat), cursive",
            fontWeight: 500,
            fontSize: 22,
            color: "var(--sage)",
            lineHeight: 1.3,
            transform: "rotate(-.6deg)",
          }}
        >
          »&nbsp;&nbsp;{stop.tip}
        </p>
      )}
      {chips.length > 0 && (
        <div className="my-[14px] flex flex-wrap gap-2">
          {chips.map((c, i) => (
            <span
              key={i}
              className="px-[10px] py-1"
              style={{
                fontFamily: "var(--font-elite), monospace",
                fontSize: 10,
                letterSpacing: ".12em",
                textTransform: "uppercase",
                color: "var(--ink)",
                background: "rgba(250,244,234,.7)",
                border: "1px solid var(--ink-soft)",
              }}
            >
              {c}
            </span>
          ))}
        </div>
      )}
      {stop.order_recommendations && (
        <MenuBlock rec={stop.order_recommendations} />
      )}
    </div>
  );
}
