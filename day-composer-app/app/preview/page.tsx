"use client";

import { Suspense, useCallback, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { PolaroidKeepsake } from "@/components/templates/polaroid-keepsake";
import { CinematicEditorial } from "@/components/templates/cinematic-editorial";
import { AuroraRomance } from "@/components/templates/aurora-romance";
import {
  SAMPLE_TRIP_CONTEXT,
  SAMPLE_PLAN_MIA_V1,
  SAMPLE_PLAN_MIA_V2,
  SAMPLE_PLAN_GARRY_V1,
  SAMPLE_PLAN_GARRY_V2,
} from "@/lib/data/sample-plan";
import {
  SAMPLE_PLAN_MIA_V1_EN,
  SAMPLE_PLAN_GARRY_FAMILY_DAY_EN,
  SAMPLE_PLAN_GARRY_CULTURAL_DAY_EN,
  SAMPLE_PLAN_GARRY_GOLDEN_NIGHT_EN,
  TRIP_CONTEXT_GARRY_FAMILY_DAY,
  TRIP_CONTEXT_GARRY_CULTURAL_DAY,
  TRIP_CONTEXT_GARRY_GOLDEN_NIGHT,
} from "@/lib/data/sample-plan-en";
import type {
  TemplateId,
  TripContext,
  TripPlan,
} from "@/lib/types/trip-plan";
import { pickTemplate } from "@/lib/utils/pick-template";

type Mode = "auto" | TemplateId;
const MODES: Mode[] = ["auto", "polaroid", "cinematic", "aurora"];

interface PlanOption {
  id: string;
  label: string;
  plan: TripPlan;
  context?: TripContext;
  /** Plans without a hand-translated EN version render the raw Chinese JSON. */
  language: "en" | "zh";
}

const PLAN_OPTIONS: PlanOption[] = [
  // Garry demo set — all English
  {
    id: "garry_family_day",
    label: "Garry · Family Day",
    plan: SAMPLE_PLAN_GARRY_FAMILY_DAY_EN,
    context: TRIP_CONTEXT_GARRY_FAMILY_DAY,
    language: "en",
  },
  {
    id: "garry_cultural_day",
    label: "Garry · Cultural Day",
    plan: SAMPLE_PLAN_GARRY_CULTURAL_DAY_EN,
    context: TRIP_CONTEXT_GARRY_CULTURAL_DAY,
    language: "en",
  },
  {
    id: "garry_golden_night",
    label: "Garry · Golden Night",
    plan: SAMPLE_PLAN_GARRY_GOLDEN_NIGHT_EN,
    context: TRIP_CONTEXT_GARRY_GOLDEN_NIGHT,
    language: "en",
  },
  // Legacy / raw JSON fixtures
  { id: "mia_v1_en", label: "Mia · v1 (EN)", plan: SAMPLE_PLAN_MIA_V1_EN, language: "en" },
  { id: "mia_v1", label: "Mia · v1 (raw)", plan: SAMPLE_PLAN_MIA_V1, language: "zh" },
  { id: "mia_v2", label: "Mia · v2 (raw)", plan: SAMPLE_PLAN_MIA_V2, language: "zh" },
  { id: "garry_v1", label: "Garry · v1 (raw)", plan: SAMPLE_PLAN_GARRY_V1, language: "zh" },
  { id: "garry_v2", label: "Garry · v2 (raw)", plan: SAMPLE_PLAN_GARRY_V2, language: "zh" },
];

const DEFAULT_PLAN_ID = "garry_family_day";

function isMode(v: string | null): v is Mode {
  return v != null && (MODES as string[]).includes(v);
}

function findPlanOption(id: string | null): PlanOption {
  return PLAN_OPTIONS.find((p) => p.id === id) ?? PLAN_OPTIONS[0];
}

export default function PreviewPage() {
  return (
    <Suspense fallback={null}>
      <PreviewInner />
    </Suspense>
  );
}

function PreviewInner() {
  const router = useRouter();
  const search = useSearchParams();

  const initialMode: Mode = (() => {
    const t = search.get("template");
    return isMode(t) ? t : "auto";
  })();
  const initialPlanOption = findPlanOption(search.get("plan") ?? DEFAULT_PLAN_ID);

  const [mode, setMode] = useState<Mode>(initialMode);
  const [planOption, setPlanOption] = useState<PlanOption>(initialPlanOption);
  const [pastedPlan, setPastedPlan] = useState<TripPlan | null>(null);
  // Each Garry plan carries its own context; legacy fixtures fall back to Mia's.
  const tripContext: TripContext | undefined =
    planOption.context ?? SAMPLE_TRIP_CONTEXT;
  const [pasteOpen, setPasteOpen] = useState(false);
  const [pasteValue, setPasteValue] = useState("");
  const [pasteError, setPasteError] = useState<string | null>(null);

  const plan: TripPlan = pastedPlan ?? planOption.plan;

  const resolvedTemplate: TemplateId = useMemo(() => {
    if (mode === "auto") return pickTemplate(plan, tripContext);
    return mode;
  }, [mode, plan, tripContext]);

  const updateUrl = useCallback(
    (next: { mode?: Mode; planId?: string }) => {
      const params = new URLSearchParams(search.toString());
      if (next.mode) params.set("template", next.mode);
      if (next.planId) params.set("plan", next.planId);
      router.replace(`?${params.toString()}`);
    },
    [router, search],
  );

  const setModeAndUrl = useCallback(
    (m: Mode) => {
      setMode(m);
      updateUrl({ mode: m });
    },
    [updateUrl],
  );

  const setPlanAndUrl = useCallback(
    (id: string) => {
      const next = findPlanOption(id);
      setPlanOption(next);
      setPastedPlan(null);
      updateUrl({ planId: next.id });
    },
    [updateUrl],
  );

  const applyJson = useCallback(() => {
    try {
      const obj = JSON.parse(pasteValue) as TripPlan;
      if (!obj || typeof obj !== "object" || !Array.isArray(obj.stops)) {
        throw new Error("Missing required field: stops");
      }
      setPastedPlan(obj);
      setPasteError(null);
    } catch (e) {
      setPasteError((e as Error).message);
    }
  }, [pasteValue]);

  const resetPaste = useCallback(() => {
    setPastedPlan(null);
    setPasteValue("");
    setPasteError(null);
  }, []);

  const handleRefine = useCallback((instruction: string) => {
    // Frontend-only stub. In real use the backend would re-compose.
    // eslint-disable-next-line no-console
    console.info("[refine]", instruction);
  }, []);

  return (
    <>
      {/* Top control bar */}
      <div
        className="fixed left-1/2 top-3 z-[100] flex max-w-[calc(100%-24px)] flex-wrap items-center gap-1 rounded-full border border-black/20 bg-white/85 p-1 shadow-lg backdrop-blur"
        style={{ transform: "translateX(-50%)", fontFamily: "system-ui, sans-serif" }}
      >
        <select
          value={pastedPlan ? "" : planOption.id}
          onChange={(e) => setPlanAndUrl(e.target.value)}
          className="rounded-full bg-transparent px-3 py-1 text-[11px] uppercase tracking-[0.16em] text-black/80 outline-none"
          aria-label="Select demo plan"
        >
          {pastedPlan && <option value="">— Pasted JSON —</option>}
          {PLAN_OPTIONS.map((p) => (
            <option key={p.id} value={p.id}>
              {p.label}
            </option>
          ))}
        </select>
        <span className="mx-1 h-4 w-px bg-black/15" />
        {MODES.map((m) => {
          const active = mode === m;
          return (
            <button
              key={m}
              type="button"
              onClick={() => setModeAndUrl(m)}
              className={`rounded-full px-3 py-1 text-[11px] uppercase tracking-[0.18em] transition ${
                active
                  ? "bg-black text-white"
                  : "bg-transparent text-black/60 hover:text-black"
              }`}
            >
              {m}
            </button>
          );
        })}
        <span className="mx-1 h-4 w-px bg-black/15" />
        <button
          type="button"
          onClick={() => setPasteOpen((v) => !v)}
          className={`rounded-full px-3 py-1 text-[11px] uppercase tracking-[0.18em] ${
            pasteOpen ? "bg-black text-white" : "bg-transparent text-black/60"
          }`}
        >
          Paste JSON
        </button>
        {planOption.language === "zh" && !pastedPlan && (
          <span className="ml-1 mr-2 rounded-full bg-amber-100 px-2 py-[2px] text-[9px] uppercase tracking-[0.18em] text-amber-900">
            zh content
          </span>
        )}
      </div>

      {/* JSON paste panel */}
      {pasteOpen && (
        <div className="fixed right-3 top-14 z-[100] w-[420px] max-w-[calc(100%-24px)] rounded-xl border border-black/20 bg-white/95 p-3 shadow-2xl backdrop-blur">
          <div className="mb-2 flex items-center justify-between">
            <span className="text-[10px] uppercase tracking-[.22em] text-black/60">
              TripPlan JSON
            </span>
            <button
              type="button"
              className="text-[12px] text-black/60 hover:text-black"
              onClick={() => setPasteOpen(false)}
            >
              ✕
            </button>
          </div>
          <textarea
            value={pasteValue}
            onChange={(e) => setPasteValue(e.target.value)}
            placeholder="Paste a TripPlan JSON here…"
            className="h-[260px] w-full resize-y rounded border border-black/20 bg-white p-2 font-mono text-[12px] outline-none"
          />
          {pasteError && (
            <div className="mt-1 text-[11px] text-red-600">{pasteError}</div>
          )}
          <div className="mt-2 flex items-center justify-between gap-2">
            <button
              type="button"
              onClick={resetPaste}
              className="rounded border border-black/20 px-3 py-1 text-[11px] uppercase tracking-[.18em] text-black/70 hover:bg-black/5"
            >
              Reset
            </button>
            <button
              type="button"
              onClick={applyJson}
              className="rounded bg-black px-3 py-1 text-[11px] uppercase tracking-[.18em] text-white hover:bg-black/85"
            >
              Apply
            </button>
          </div>
        </div>
      )}

      {/* Template body */}
      <main>
        {resolvedTemplate === "polaroid" && (
          <PolaroidKeepsake plan={plan} tripContext={tripContext} onRefine={handleRefine} />
        )}
        {resolvedTemplate === "cinematic" && (
          <CinematicEditorial plan={plan} tripContext={tripContext} onRefine={handleRefine} />
        )}
        {resolvedTemplate === "aurora" && (
          <AuroraRomance plan={plan} tripContext={tripContext} onRefine={handleRefine} />
        )}
      </main>
    </>
  );
}
