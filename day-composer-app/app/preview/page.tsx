"use client";

import { Suspense, useCallback, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { PolaroidKeepsake } from "@/components/templates/polaroid-keepsake";
import { CinematicEditorial } from "@/components/templates/cinematic-editorial";
import { AuroraRomance } from "@/components/templates/aurora-romance";
import { SAMPLE_TRIP_CONTEXT } from "@/lib/data/sample-plan";
import { SAMPLE_PLAN_MIA_V1_EN } from "@/lib/data/sample-plan-en";
import type {
  TemplateId,
  TripContext,
  TripPlan,
} from "@/lib/types/trip-plan";
import { pickTemplate } from "@/lib/utils/pick-template";

type Mode = "auto" | TemplateId;
const MODES: Mode[] = ["auto", "polaroid", "cinematic", "aurora"];

function isMode(v: string | null): v is Mode {
  return v != null && (MODES as string[]).includes(v);
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

  const [mode, setMode] = useState<Mode>(initialMode);
  const [plan, setPlan] = useState<TripPlan>(SAMPLE_PLAN_MIA_V1_EN);
  const [tripContext] = useState<TripContext | undefined>(SAMPLE_TRIP_CONTEXT);
  const [pasteOpen, setPasteOpen] = useState(false);
  const [pasteValue, setPasteValue] = useState("");
  const [pasteError, setPasteError] = useState<string | null>(null);

  const resolvedTemplate: TemplateId = useMemo(() => {
    if (mode === "auto") return pickTemplate(plan, tripContext);
    return mode;
  }, [mode, plan, tripContext]);

  const setModeAndUrl = useCallback(
    (m: Mode) => {
      setMode(m);
      const next = new URLSearchParams(search.toString());
      next.set("template", m);
      router.replace(`?${next.toString()}`);
    },
    [router, search],
  );

  const applyJson = useCallback(() => {
    try {
      const obj = JSON.parse(pasteValue) as TripPlan;
      if (!obj || typeof obj !== "object" || !Array.isArray(obj.stops)) {
        throw new Error("Missing required field: stops");
      }
      setPlan(obj);
      setPasteError(null);
    } catch (e) {
      setPasteError((e as Error).message);
    }
  }, [pasteValue]);

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
              onClick={() => {
                setPlan(SAMPLE_PLAN_MIA_V1_EN);
                setPasteValue("");
                setPasteError(null);
              }}
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
