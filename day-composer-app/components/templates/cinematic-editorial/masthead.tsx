"use client";

import type { TripContext } from "@/lib/types/trip-plan";

interface MastheadProps {
  tripContext?: TripContext;
}

export function Masthead({ tripContext }: MastheadProps) {
  return (
    <div
      className="flex items-center justify-between px-10 py-[14px] max-md:flex-col max-md:items-start max-md:gap-[10px] max-md:px-[18px]"
      style={{
        background: "var(--jet)",
        color: "var(--ivory)",
        fontFamily: "var(--font-jetbrains), monospace",
        fontSize: 10,
        letterSpacing: ".28em",
        textTransform: "uppercase",
      }}
    >
      <div
        className="masthead-brand"
        style={{
          fontFamily: "var(--font-bodoni), serif",
          fontWeight: 900,
          fontSize: 16,
          letterSpacing: 0,
          textTransform: "none",
        }}
      >
        <span
          className="mr-[10px] inline-block h-2 w-2 align-middle"
          style={{ background: "var(--red)" }}
        />
        Day Composer ·{" "}
        <em style={{ fontStyle: "italic", fontWeight: 400, color: "var(--silver)" }}>Issue I</em>
      </div>
      <div
        className="flex flex-wrap gap-x-7 gap-y-[14px]"
        style={{ color: "var(--silver)" }}
      >
        <span>
          {tripContext?.date_label ?? "Jan · MMXXVI"} ·{" "}
          <b style={{ color: "var(--ivory)", fontWeight: 500 }}>{tripContext?.time_window ?? ""}</b>
        </span>
        <span>
          Vol · <b style={{ color: "var(--ivory)", fontWeight: 500 }}>01</b>
        </span>
        <span>
          Edition · <b style={{ color: "var(--ivory)", fontWeight: 500 }}>{tripContext?.origin ?? "Bay Area"}</b>
        </span>
      </div>
    </div>
  );
}
