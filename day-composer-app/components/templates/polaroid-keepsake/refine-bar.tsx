"use client";

import { useState } from "react";

interface RefineBarProps {
  chips?: string[];
  onRefine?: (instruction: string) => void;
}

export function RefineBar({ chips = ["Quieter", "Add a bar", "Baby is tired"], onRefine }: RefineBarProps) {
  const [value, setValue] = useState("");
  const submit = () => {
    if (!value.trim()) return;
    onRefine?.(value.trim());
    setValue("");
  };
  return (
    <div
      className="fixed bottom-[18px] left-1/2 z-[60] flex max-w-[calc(100%-36px)] items-center gap-2 px-[16px] py-2 max-md:flex-wrap"
      style={{
        transform: "translateX(-50%)",
        background: "var(--ink)",
        color: "var(--bone)",
        border: "2px solid var(--ink)",
        boxShadow: "0 8px 24px -6px rgba(0,0,0,.3)",
      }}
    >
      <div
        className="absolute left-[30px] top-[-8px] h-[14px] w-20"
        style={{ transform: "rotate(-4deg)", background: "var(--tape-rose)" }}
      />
      <span
        className="mr-1"
        style={{
          fontFamily: "var(--font-caveat), cursive",
          fontWeight: 700,
          fontSize: 18,
          color: "var(--bone)",
        }}
      >
        tweak →
      </span>
      {chips.map((c) => (
        <button
          key={c}
          type="button"
          onClick={() => setValue(c)}
          className="px-3 py-[6px]"
          style={{
            background: "transparent",
            border: "1px dashed rgba(244,236,223,.5)",
            color: "var(--bone)",
            fontFamily: "var(--font-elite), monospace",
            fontSize: 11,
            letterSpacing: ".05em",
            cursor: "pointer",
          }}
        >
          {c}
        </button>
      ))}
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submit()}
        placeholder="adjust this day..."
        className="min-w-[160px] flex-1 px-1 py-1 outline-none"
        style={{
          background: "transparent",
          border: "none",
          borderBottom: "1px dashed var(--bone)",
          color: "var(--bone)",
          fontFamily: "var(--font-caveat), cursive",
          fontWeight: 500,
          fontSize: 18,
        }}
      />
      <button
        type="button"
        onClick={submit}
        className="px-4 py-2"
        style={{
          background: "var(--rose)",
          color: "var(--ink)",
          border: "none",
          fontFamily: "var(--font-caveat), cursive",
          fontWeight: 700,
          fontSize: 18,
          cursor: "pointer",
        }}
      >
        recompose
      </button>
    </div>
  );
}
