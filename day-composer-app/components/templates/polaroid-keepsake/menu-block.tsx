"use client";

import ReactMarkdown from "react-markdown";
import type { OrderRecs } from "@/lib/types/trip-plan";
import { isBoldPick, parseDish } from "@/lib/utils/parse-dish";

interface MenuBlockProps {
  rec: OrderRecs;
}

export function MenuBlock({ rec }: MenuBlockProps) {
  return (
    <div
      className="relative my-6 mb-[10px] p-6"
      style={{
        background: "rgba(250,244,234,.55)",
        border: "1px dashed var(--ink-soft)",
        transform: "rotate(.3deg)",
      }}
    >
      <div
        className="absolute left-[30px] top-[-9px] h-[18px] w-20"
        style={{ transform: "rotate(-2deg)", background: "var(--tape-sage)" }}
      />
      <div
        className="mb-[14px] flex items-baseline justify-between"
        style={{
          fontFamily: "var(--font-playfair), serif",
          fontStyle: "italic",
          fontWeight: 700,
          fontSize: 22,
          color: "var(--ink)",
        }}
      >
        what to order
        <small
          style={{
            fontFamily: "var(--font-elite), monospace",
            fontSize: 10,
            letterSpacing: ".18em",
            textTransform: "uppercase",
            color: "var(--rose-deep)",
            fontStyle: "normal",
            fontWeight: 400,
          }}
        >
          order of fire ↓
        </small>
      </div>
      {rec.menu_listed.map((raw, i) => {
        const { menu_number, name } = parseDish(raw);
        const bold = isBoldPick(raw, rec.bold_picks);
        return (
          <div
            key={i}
            className="grid items-baseline gap-[14px] py-2"
            style={{
              gridTemplateColumns: "42px 1fr auto",
              borderBottom:
                i === rec.menu_listed.length - 1
                  ? "none"
                  : "1px dotted var(--ink-soft)",
              fontSize: 14,
            }}
          >
            <div
              style={{
                fontFamily: "var(--font-elite), monospace",
                color: "var(--wine)",
                fontSize: 13,
              }}
            >
              {menu_number ? `N°${menu_number}` : ""}
            </div>
            <div
              style={{
                fontFamily: "var(--font-crimson), serif",
                fontWeight: bold ? 700 : 500,
                color: "var(--ink)",
              }}
            >
              {name}
            </div>
            <div
              style={{
                fontFamily: "var(--font-elite), monospace",
                fontSize: 9,
                textTransform: "uppercase",
                letterSpacing: ".16em",
                color: bold ? "var(--rose-deep)" : "var(--ink-soft)",
              }}
            >
              {bold ? "pick" : ""}
            </div>
          </div>
        );
      })}
      <div
        className="mt-[14px] border-t pt-3"
        style={{
          borderColor: "var(--ink-soft)",
          borderStyle: "dashed",
          fontFamily: "var(--font-caveat), cursive",
          fontWeight: 500,
          fontSize: 20,
          color: "var(--ink)",
          lineHeight: 1.4,
        }}
      >
        <ReactMarkdown
          components={{
            p: ({ children }) => <p>{children}</p>,
            strong: ({ children }) => (
              <strong style={{ color: "var(--wine)", fontWeight: 700 }}>
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
