"use client";

import ReactMarkdown from "react-markdown";
import type { OrderRecs } from "@/lib/types/trip-plan";
import { isBoldPick, parseDish } from "@/lib/utils/parse-dish";

interface MenuCardProps {
  rec: OrderRecs;
}

export function MenuCard({ rec }: MenuCardProps) {
  return (
    <div
      className="relative mt-[30px] rounded-3xl border p-8"
      style={{
        background: "rgba(255,255,255,.6)",
        backdropFilter: "blur(16px)",
        borderColor: "rgba(255,255,255,.7)",
        boxShadow: "0 14px 40px -15px rgba(201,123,140,.25)",
      }}
    >
      <div
        className="absolute left-[30px] top-[-12px] h-6 w-6"
        style={{
          background:
            "radial-gradient(circle,var(--peach) 0%,transparent 70%)",
          opacity: 0.7,
        }}
      />
      <div
        className="mb-[18px] flex items-baseline justify-between"
        style={{
          fontFamily: "var(--font-cormorant), serif",
          fontStyle: "italic",
          fontWeight: 400,
          fontSize: 26,
          color: "var(--ink)",
        }}
      >
        what to order
        <small
          style={{
            fontFamily: "var(--font-dm-mono), monospace",
            fontSize: 10,
            letterSpacing: ".2em",
            color: "var(--accent-deep)",
            textTransform: "uppercase",
            fontStyle: "normal",
          }}
        >
          {rec.menu_listed.length} dishes · order of fire
        </small>
      </div>
      {rec.menu_listed.map((raw, i) => {
        const { menu_number, name } = parseDish(raw);
        const bold = isBoldPick(raw, rec.bold_picks);
        return (
          <div
            key={i}
            className="grid items-baseline gap-[14px] py-[11px]"
            style={{
              gridTemplateColumns: "50px 1fr auto",
              borderBottom:
                i === rec.menu_listed.length - 1
                  ? "none"
                  : "1px solid rgba(61,46,61,.06)",
              fontSize: 14,
            }}
          >
            <div
              style={{
                fontFamily: "var(--font-dm-mono), monospace",
                color: "var(--accent-deep)",
                fontWeight: 500,
              }}
            >
              {menu_number ?? ""}
            </div>
            <div
              style={{
                fontWeight: bold ? 600 : 400,
                color: "var(--ink)",
              }}
            >
              {name}
            </div>
            <div
              className="text-right"
              style={{
                fontFamily: "var(--font-dm-mono), monospace",
                fontSize: 10,
                textTransform: "uppercase",
                letterSpacing: ".14em",
                color: bold ? "var(--accent-deep)" : "var(--ink-soft)",
              }}
            >
              {bold ? "pick" : ""}
            </div>
          </div>
        );
      })}
      <div
        className="mt-[18px] pt-[18px]"
        style={{
          borderTop: "1px solid rgba(61,46,61,.06)",
          fontFamily: "var(--font-cormorant), serif",
          fontStyle: "italic",
          fontSize: 17,
          color: "var(--ink)",
          lineHeight: 1.6,
        }}
      >
        <ReactMarkdown
          components={{
            p: ({ children }) => <p>{children}</p>,
            strong: ({ children }) => (
              <strong
                style={{ color: "var(--accent-deep)", fontWeight: 600 }}
              >
                {children}
              </strong>
            ),
          }}
        >
          {rec.logic_text}
        </ReactMarkdown>
      </div>
    </div>
  );
}
