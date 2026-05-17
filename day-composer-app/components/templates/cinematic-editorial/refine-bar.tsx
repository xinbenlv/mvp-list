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
      className="fixed bottom-0 left-0 right-0 z-[60] flex flex-wrap items-center gap-[10px] px-10 py-[14px] max-md:px-5"
      style={{
        background: "var(--jet)",
        color: "var(--ivory)",
        borderTop: "3px solid var(--red)",
      }}
    >
      <span
        className="mr-[6px]"
        style={{
          fontFamily: "var(--font-jetbrains), monospace",
          fontSize: 10,
          letterSpacing: ".3em",
          textTransform: "uppercase",
          color: "var(--red)",
          fontWeight: 700,
        }}
      >
        ↻ Re-compose
      </span>
      {chips.map((c) => (
        <button
          key={c}
          type="button"
          onClick={() => setValue(c)}
          className="px-[14px] py-[7px]"
          style={{
            background: "transparent",
            border: "1px solid var(--ivory)",
            color: "var(--ivory)",
            fontFamily: "var(--font-dm-sans), sans-serif",
            fontSize: 12,
            cursor: "pointer",
            letterSpacing: ".04em",
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
        className="min-w-[160px] flex-1 px-1 py-[6px] outline-none"
        style={{
          background: "transparent",
          border: "none",
          borderBottom: "1px solid var(--ivory)",
          color: "var(--ivory)",
          fontFamily: "var(--font-bodoni), serif",
          fontStyle: "italic",
          fontSize: 16,
        }}
      />
      <button
        type="button"
        onClick={submit}
        className="px-[22px] py-[10px]"
        style={{
          background: "var(--red)",
          color: "var(--ivory)",
          border: "none",
          fontFamily: "var(--font-jetbrains), monospace",
          fontSize: 11,
          letterSpacing: ".24em",
          textTransform: "uppercase",
          cursor: "pointer",
          fontWeight: 700,
        }}
      >
        Recompose
      </button>
    </div>
  );
}
