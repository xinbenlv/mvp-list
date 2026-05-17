"use client";

import { motion } from "framer-motion";
import type { OrderRecs, Stop } from "@/lib/types/trip-plan";
import { formatLogisticsChips } from "@/lib/utils/format-logistics";
import { MenuCard } from "./menu-card";

const STOP_GRADIENTS = [
  "linear-gradient(135deg,var(--peach),var(--rose))",
  "linear-gradient(135deg,var(--sage-mist),var(--lavender-soft),var(--peach))",
  "linear-gradient(135deg,var(--rose),var(--accent),var(--accent-deep))",
  "linear-gradient(135deg,var(--lavender-soft),var(--blush),var(--ink))",
];

const POEMS = [
  "a quiet adobe\nholding its breath",
  "ducks, geese,\nthe slow water",
  "nine plates,\none long table",
  "the last laugh\nof the night",
];

const ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"];

const PACING_LABEL: Record<string, string> = {
  opening: "Opening",
  breathing: "Breathing",
  peak: "Peak",
  recovery: "Recovery",
  closing: "Closing",
  "slow start": "Slow start",
  spark: "Spark",
  rise: "Rise",
  climax: "Climax",
  afterglow: "Afterglow",
  build: "Build",
  fade: "Fade",
};

interface StopRowProps {
  stop: Stop;
  index: number;
  pacingLabel?: string;
  orderRecs?: OrderRecs | null;
  /** Pulled from the previous stop's `transition_to_next` + drive min. */
  transitionText?: string | null;
  transitionDriveMin?: number | null;
}

/** booking_links may be string or {label,url}. Return first URL or null. */
function firstBookingUrl(stop: Stop): string | null {
  const links = stop.logistics?.booking_links;
  if (!links || links.length === 0) return null;
  const first = links[0];
  return typeof first === "string" ? first : first.url;
}

export function StopRow({
  stop,
  index,
  pacingLabel,
  orderRecs,
  transitionText,
  transitionDriveMin,
}: StopRowProps) {
  const isEven = index % 2 === 1;
  const chips = formatLogisticsChips(stop.logistics);
  const grad = STOP_GRADIENTS[index % STOP_GRADIENTS.length];
  const poem = POEMS[index % POEMS.length];
  const eyebrow = `Movement ${ROMAN[index] ?? index + 1} · ${
    pacingLabel ? PACING_LABEL[pacingLabel] ?? pacingLabel : "Stop"
  }`;
  const useDarkPoemColor = index >= 2;
  const bookingUrl = firstBookingUrl(stop);

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-80px" }}
        transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
        className={`relative mb-[140px] grid items-center gap-[60px] max-md:mb-[90px] max-md:grid-cols-1 max-md:gap-[30px] max-md:p-0 ${
          isEven ? "pl-[60px]" : "pr-[60px]"
        } max-md:!pl-0 max-md:!pr-0`}
        style={{ gridTemplateColumns: "1fr 1fr" }}
      >
        <div
          className={`relative flex aspect-[4/5] items-end overflow-hidden rounded-[28px] p-9 transition-transform duration-300 hover:rotate-0 hover:scale-[1.02] ${
            isEven ? "order-2 max-md:order-none" : ""
          }`}
          style={{
            background: grad,
            color: index >= 2 ? "#fff" : "var(--ink)",
            boxShadow: "0 40px 100px -30px rgba(201,123,140,.5)",
            transform: isEven ? "rotate(2deg)" : "rotate(-1.5deg)",
          }}
        >
          <div
            className="absolute left-[30px] right-[30px] top-[30px] z-[2]"
            style={{
              fontFamily: "var(--font-caveat), cursive",
              fontWeight: 500,
              fontSize: 22,
              opacity: 0.8,
              lineHeight: 1.2,
              transform: "rotate(-1deg)",
              color: useDarkPoemColor ? undefined : "var(--accent-deep)",
              whiteSpace: "pre-line",
            }}
          >
            {poem}
          </div>
          <div className="relative z-[2]">
            <div
              style={{
                fontFamily: "var(--font-cormorant), serif",
                fontStyle: "italic",
                fontWeight: 300,
                fontSize: 72,
                lineHeight: 1,
                textShadow: "0 2px 20px rgba(0,0,0,.2)",
              }}
            >
              {stop.time}
            </div>
            <div
              className="mt-2 opacity-95"
              style={{
                fontFamily: "var(--font-dm-mono), monospace",
                fontSize: 11,
                letterSpacing: ".22em",
                textTransform: "uppercase",
              }}
            >
              {stop.place_name ?? stop.place_id}
            </div>
          </div>
        </div>
        <div className="relative">
          <div
            className="pointer-events-none absolute left-[-30px] top-[-40px] max-md:left-[-10px] max-md:top-[-30px]"
            style={{
              fontFamily: "var(--font-cormorant), serif",
              fontStyle: "italic",
              fontWeight: 300,
              fontSize: 160,
              color: "var(--accent)",
              opacity: 0.15,
              lineHeight: 1,
            }}
          >
            {ROMAN[index] ?? index + 1}
          </div>
          <div
            className="relative z-[1] mb-[14px]"
            style={{
              fontFamily: "var(--font-dm-mono), monospace",
              fontSize: 10,
              letterSpacing: ".32em",
              textTransform: "uppercase",
              color: "var(--accent-deep)",
            }}
          >
            {eyebrow}
          </div>
          <h2
            className="relative z-[1] mb-[14px] max-md:text-4xl"
            style={{
              fontFamily: "var(--font-cormorant), serif",
              fontStyle: "italic",
              fontWeight: 300,
              fontSize: 52,
              lineHeight: 1.05,
              letterSpacing: "-.015em",
              color: "var(--ink)",
            }}
          >
            <em style={{ fontWeight: 400 }}>{stop.place_name}</em>
          </h2>
          {stop.one_liner && (
            <p
              className="mb-6"
              style={{
                fontFamily: "var(--font-cormorant), serif",
                fontStyle: "italic",
                fontSize: 18,
                lineHeight: 1.55,
                color: "var(--ink-soft)",
                borderLeft: "2px solid var(--accent)",
                paddingLeft: 14,
              }}
            >
              {stop.one_liner}
            </p>
          )}
          <p
            className="mb-6"
            style={{
              fontSize: 17,
              lineHeight: 1.8,
              color: "var(--ink)",
              fontWeight: 300,
            }}
          >
            {stop.why_fits_today}
          </p>
          {chips.length > 0 && (
            <div className="mb-[14px] flex flex-wrap gap-2">
              {chips.map((c, i) => (
                <span
                  key={i}
                  className="rounded-full border px-[14px] py-[5px]"
                  style={{
                    fontFamily: "var(--font-dm-sans), sans-serif",
                    fontSize: 12,
                    fontWeight: 400,
                    background: "rgba(255,255,255,.55)",
                    backdropFilter: "blur(6px)",
                    borderColor: "rgba(61,46,61,.06)",
                    color: "var(--ink-soft)",
                  }}
                >
                  {c}
                </span>
              ))}
            </div>
          )}
          {stop.tip && (
            <p
              className="my-[14px] border-l-[2px] pl-[14px]"
              style={{
                fontFamily: "var(--font-cormorant), serif",
                fontStyle: "italic",
                fontSize: 16,
                color: "var(--accent-deep)",
                borderColor: "var(--accent)",
                lineHeight: 1.5,
              }}
            >
              {stop.tip}
            </p>
          )}
          {bookingUrl && (
            <a
              href={bookingUrl}
              target="_blank"
              rel="noreferrer"
              className="mt-2 inline-block rounded-full px-[30px] py-[13px] text-white no-underline transition-transform hover:-translate-y-[2px]"
              style={{
                background:
                  "linear-gradient(135deg,var(--accent),var(--blush))",
                fontSize: 13,
                letterSpacing: ".06em",
                fontWeight: 500,
                boxShadow: "0 10px 30px -8px rgba(201,123,140,.5)",
              }}
            >
              reserve
            </a>
          )}
          {orderRecs && <MenuCard rec={orderRecs} />}
        </div>
      </motion.div>
      {transitionText && (
        <div
          className="mb-[100px] text-center"
          style={{
            fontFamily: "var(--font-cormorant), serif",
            fontStyle: "italic",
            fontWeight: 300,
            fontSize: 20,
            color: "var(--ink-soft)",
            letterSpacing: ".02em",
          }}
        >
          <span style={{ color: "var(--accent)" }}>~ </span>
          {transitionText}
          {transitionDriveMin != null && (
            <> · {transitionDriveMin} min drive</>
          )}
          <span style={{ color: "var(--accent)" }}> ~</span>
        </div>
      )}
    </>
  );
}
