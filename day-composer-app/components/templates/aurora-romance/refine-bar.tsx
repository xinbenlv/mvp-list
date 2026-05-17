"use client";

import { useState } from "react";

interface RefineBarProps {
  chips?: string[];
  onRefine?: (instruction: string) => void;
}

export function RefineBar({
  chips = ["Quieter", "Add a bar", "Baby is tired"],
  onRefine,
}: RefineBarProps) {
  const [value, setValue] = useState("");
  const submit = () => {
    if (!value.trim()) return;
    onRefine?.(value.trim());
    setValue("");
  };
  return (
    <div
      className="fixed bottom-5 left-1/2 z-[60] flex max-w-[calc(100%-40px)] items-center gap-2 rounded-full px-5 py-2 max-md:flex-wrap max-md:rounded-3xl max-md:p-[10px]"
      style={{
        transform: "translateX(-50%)",
        background: "rgba(61,46,61,.85)",
        backdropFilter: "blur(24px)",
        border: "1px solid rgba(255,255,255,.15)",
        boxShadow: "0 20px 50px -10px rgba(61,46,61,.4)",
      }}
    >
      {chips.map((c) => (
        <button
          key={c}
          type="button"
          onClick={() => setValue(c)}
          className="rounded-full border px-[14px] py-[7px] text-white"
          style={{
            background: "transparent",
            borderColor: "rgba(255,255,255,.2)",
            fontFamily: "var(--font-dm-sans), sans-serif",
            fontSize: 12,
            cursor: "pointer",
            fontWeight: 300,
          }}
        >
          {c}
        </button>
      ))}
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submit()}
        placeholder="adjust this day…"
        className="min-w-[140px] flex-1 px-2 py-[6px] text-white outline-none"
        style={{
          background: "transparent",
          border: "none",
          fontFamily: "var(--font-cormorant), serif",
          fontStyle: "italic",
          fontSize: 15,
        }}
      />
      <button
        type="button"
        onClick={submit}
        className="rounded-full px-5 py-[9px] text-white"
        style={{
          background:
            "linear-gradient(135deg,var(--blush),var(--accent))",
          border: "none",
          fontFamily: "var(--font-dm-sans), sans-serif",
          fontSize: 12,
          cursor: "pointer",
          fontWeight: 500,
          letterSpacing: ".04em",
        }}
      >
        recompose
      </button>
    </div>
  );
}
