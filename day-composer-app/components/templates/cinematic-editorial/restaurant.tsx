"use client";

import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import type { OrderRecs, Stop } from "@/lib/types/trip-plan";
import { formatLogisticsChips } from "@/lib/utils/format-logistics";
import { isBoldPick, parseDish } from "@/lib/utils/parse-dish";

interface RestaurantProps {
  stop: Stop;
  index: number;
  rec: OrderRecs;
}

const ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"];

export function Restaurant({ stop, index, rec }: RestaurantProps) {
  const chips = formatLogisticsChips(stop.logistics);
  return (
    <motion.section
      id={`s${index + 1}`}
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 1, ease: [0.25, 0.46, 0.45, 0.94] }}
      className="relative overflow-hidden px-[50px] py-[100px] max-md:px-6 max-md:py-[50px]"
      style={{
        minHeight: "100vh",
        background: "linear-gradient(155deg,#7a0a1c 0%,#3a0510 50%,#0a0203 100%)",
        color: "var(--ivory)",
      }}
    >
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse at 65% 35%,rgba(221,15,44,.22) 0%,transparent 55%)",
        }}
      />
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse at center,transparent 20%,rgba(0,0,0,.55) 100%)",
        }}
      />
      <div
        className="mb-6"
        style={{
          fontFamily: "var(--font-jetbrains), monospace",
          fontSize: 10,
          letterSpacing: ".36em",
          textTransform: "uppercase",
          color: "var(--silver)",
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
        Movement {ROMAN[index]?.toUpperCase()} ·{" "}
        <em style={{ color: "var(--ivory)" }}>The Peak</em>
      </div>
      <div className="relative z-[2] mx-auto grid max-w-[1300px] grid-cols-2 items-center gap-[80px] max-md:grid-cols-1 max-md:gap-[30px]">
        <div>
          <div
            className="mb-[14px]"
            style={{
              fontFamily: "var(--font-jetbrains), monospace",
              fontSize: 10,
              letterSpacing: ".4em",
              textTransform: "uppercase",
              color: "var(--ivory)",
              opacity: 0.85,
              fontWeight: 700,
            }}
          >
            Peak
          </div>
          <div
            className="mb-[18px] inline-block"
            style={{
              fontFamily: "var(--font-bodoni), serif",
              fontWeight: 900,
              fontSize: 80,
              color: "var(--ivory)",
              lineHeight: 0.85,
              letterSpacing: "-.04em",
            }}
          >
            {stop.time}
            <span
              className="mt-[14px] block h-1 w-[60px]"
              style={{ background: "var(--ivory)" }}
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
              color: "var(--ivory)",
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
                fontSize: 17,
                lineHeight: 1.55,
                color: "var(--whisper)",
                borderLeft: "3px solid var(--ivory)",
              }}
            >
              {stop.one_liner}
            </div>
          )}
          <p
            className="mb-6"
            style={{ fontSize: 16, lineHeight: 1.85, color: "var(--whisper)" }}
          >
            {stop.why_fits_today}
          </p>
          {chips.length > 0 && (
            <div
              className="mb-5 flex flex-wrap max-w-fit"
              style={{ border: "1px solid var(--ivory)" }}
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
                    background: "transparent",
                    color: "var(--ivory)",
                    borderRight: i === chips.length - 1 ? "none" : "1px solid var(--ivory)",
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
                color: "var(--ivory)",
                borderLeft: "2px solid var(--ivory)",
                lineHeight: 1.5,
              }}
            >
              {stop.tip}
            </p>
          )}
        </div>
        {/* Menu card */}
        <div
          className="relative p-[42px] max-md:p-7"
          style={{
            background: "var(--ivory)",
            color: "var(--jet)",
            boxShadow: "0 40px 100px -20px rgba(0,0,0,.7)",
            borderTop: "8px solid var(--red)",
          }}
        >
          <div
            className="absolute left-0 top-[-30px]"
            style={{
              fontFamily: "var(--font-jetbrains), monospace",
              fontSize: 10,
              letterSpacing: ".36em",
              color: "var(--ivory)",
              fontWeight: 700,
            }}
          >
            WHAT TO ORDER · BY THE COMPOSER
          </div>
          <h3
            className="mb-[6px] max-md:text-3xl"
            style={{
              fontFamily: "var(--font-bodoni), serif",
              fontWeight: 900,
              fontSize: 42,
              lineHeight: 0.95,
              letterSpacing: "-.03em",
            }}
          >
            What <em style={{ fontStyle: "italic", fontWeight: 400 }}>to order</em>
          </h3>
          <div
            className="mb-6 pb-4"
            style={{
              fontFamily: "var(--font-jetbrains), monospace",
              fontSize: 10,
              letterSpacing: ".3em",
              textTransform: "uppercase",
              color: "var(--ash)",
              borderBottom: "2px solid var(--jet)",
              fontWeight: 700,
            }}
          >
            {rec.menu_listed.length} plates · in order of fire
          </div>
          {rec.menu_listed.map((raw, i) => {
            const { menu_number, name } = parseDish(raw);
            const bold = isBoldPick(raw, rec.bold_picks);
            return (
              <div
                key={i}
                className="grid items-baseline gap-[14px] py-[11px]"
                style={{
                  gridTemplateColumns: "48px 1fr auto",
                  borderBottom:
                    i === rec.menu_listed.length - 1
                      ? "none"
                      : "1px solid var(--hairline)",
                }}
              >
                <div
                  style={{
                    fontFamily: "var(--font-bodoni), serif",
                    fontWeight: 900,
                    fontSize: 20,
                    color: "var(--red)",
                    lineHeight: 1,
                  }}
                >
                  {menu_number ?? ""}
                </div>
                <div
                  style={{
                    fontFamily: "var(--font-dm-sans), sans-serif",
                    fontWeight: bold ? 700 : 500,
                    fontSize: 14,
                    color: "var(--jet)",
                  }}
                >
                  {name}
                </div>
                <div
                  className="text-right"
                  style={{
                    fontFamily: "var(--font-jetbrains), monospace",
                    fontSize: 9,
                    textTransform: "uppercase",
                    letterSpacing: ".2em",
                    color: bold ? "var(--red)" : "var(--ash)",
                    fontWeight: bold ? 700 : 500,
                  }}
                >
                  {bold ? "pick" : ""}
                </div>
              </div>
            );
          })}
          <div
            className="mt-5 pt-4"
            style={{
              borderTop: "2px solid var(--jet)",
              fontFamily: "var(--font-bodoni), serif",
              fontStyle: "italic",
              fontSize: 16,
              lineHeight: 1.55,
              color: "var(--jet)",
            }}
          >
            <ReactMarkdown
              components={{
                p: ({ children }) => <p>{children}</p>,
                strong: ({ children }) => (
                  <strong style={{ color: "var(--red)", fontWeight: 700 }}>
                    {children}
                  </strong>
                ),
              }}
            >
              {rec.logic_text}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    </motion.section>
  );
}
