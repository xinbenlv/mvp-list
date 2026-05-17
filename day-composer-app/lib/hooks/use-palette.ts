"use client";

import { useMemo } from "react";
import type { TemplateId, TripPlan } from "@/lib/types/trip-plan";

/**
 * Returns CSS-var-style values for the chosen template, lightly nudged based
 * on the plan's mood_tags (now free strings — match via .includes()).
 */

type Palette = Record<string, string>;

const BASE: Record<TemplateId, Palette> = {
  polaroid: {
    "--bone": "#F4ECDF",
    "--paper": "#FAF4EA",
    "--ink": "#2B232B",
    "--ink-soft": "#6A5A60",
    "--rose": "#C28D8A",
    "--rose-deep": "#A86E6B",
    "--sage": "#9DAD93",
    "--wine": "#6B3D49",
    "--champagne": "#E0CBA8",
    "--tape-rose": "rgba(194,141,138,.5)",
    "--tape-sage": "rgba(157,173,147,.5)",
  },
  cinematic: {
    "--ivory": "#F8F6F0",
    "--paper": "#FAF9F4",
    "--jet": "#0A0A0A",
    "--noir": "#15161A",
    "--red": "#DD0F2C",
    "--red-deep": "#A0061C",
    "--ash": "#5A5C60",
    "--silver": "#9D9FA3",
    "--whisper": "rgba(248,246,240,.65)",
    "--hairline": "rgba(10,10,10,.12)",
  },
  aurora: {
    "--peach": "#FFD3B6",
    "--rose": "#FFBCBC",
    "--blush": "#F8C8DC",
    "--lavender-soft": "#E2D4F0",
    "--sage-mist": "#D4E4D4",
    "--cream": "#FFF8F0",
    "--ivory": "#FAEFE4",
    "--ink": "#3D2E3D",
    "--ink-soft": "#7A5C6E",
    "--accent": "#C97B8C",
    "--accent-deep": "#9B5C6E",
    "--gold-whisper": "#E6C9A8",
  },
};

export function usePalette(
  plan: TripPlan | null,
  templateId: TemplateId,
): Palette {
  return useMemo(() => {
    const base = { ...BASE[templateId] };
    const mood = (plan?.mood_tags ?? []).join(" ").toLowerCase();
    const has = (s: string) => mood.includes(s);

    // Lightweight nudges. Each branch tweaks at most one accent var.
    if (has("celebratory") || has("playful") || has("lively")) {
      if (templateId === "polaroid") base["--rose"] = "#D27671";
      if (templateId === "cinematic") base["--red"] = "#EB1132";
      if (templateId === "aurora") base["--accent"] = "#D86B82";
    }
    if (has("restorative") || has("reflective") || has("sun-warmed")) {
      if (templateId === "polaroid") base["--rose"] = "#BD9290";
      if (templateId === "cinematic") base["--red"] = "#C71028";
      if (templateId === "aurora") base["--accent"] = "#B98A98";
    }
    if (has("intimate") || has("romantic")) {
      if (templateId === "polaroid") base["--rose-deep"] = "#9A5E5B";
      if (templateId === "aurora") base["--accent-deep"] = "#8C4D60";
    }
    if (has("energizing") || has("vlog") || has("golden-hour")) {
      if (templateId === "polaroid") base["--sage"] = "#A8BC9D";
      if (templateId === "cinematic") base["--red"] = "#F11432";
      if (templateId === "aurora") base["--peach"] = "#FFC79C";
    }
    return base;
  }, [plan, templateId]);
}
