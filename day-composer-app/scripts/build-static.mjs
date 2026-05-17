/**
 * Builds the app as a static export for shareable distribution.
 *
 * Why this exists: `output: "export"` and the /api route at `app/api/plans/route.ts`
 * conflict — Next tries to write both `out/api/plans` (file from the route) and
 * `out/api/plans/family-day/` (directory from the dynamic [id] route). The simplest
 * fix is to skip `/api` entirely for static export — friends don't need it.
 *
 * Approach: temporarily rename `app/api` to `app/.api.bak`, run the export,
 * then restore on exit (even on crash).
 */

import { execSync } from "node:child_process";
import { existsSync, renameSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const apiDir = resolve(root, "app/api");
// Move OUTSIDE app/ so Next.js doesn't try to walk it as a route directory.
const apiBak = resolve(tmpdir(), "day-composer-api-backup");
const outDir = resolve(root, "out");
const nextCache = resolve(root, ".next");

let moved = false;

function restore() {
  if (moved && existsSync(apiBak)) {
    renameSync(apiBak, apiDir);
    moved = false;
    console.log("→ Restored app/api");
  }
}

process.on("exit", restore);
process.on("SIGINT", () => {
  restore();
  process.exit(130);
});

try {
  if (existsSync(apiBak)) {
    console.error(
      "→ Stale app/.api.bak found. Move it back to app/api manually and retry.",
    );
    process.exit(1);
  }

  if (existsSync(apiDir)) {
    console.log("→ Moving app/api aside for static export");
    renameSync(apiDir, apiBak);
    moved = true;
  }

  if (existsSync(outDir)) {
    console.log("→ Clearing previous out/");
    rmSync(outDir, { recursive: true, force: true });
  }

  if (existsSync(nextCache)) {
    console.log("→ Clearing .next/ cache (stale route entries from prior builds)");
    rmSync(nextCache, { recursive: true, force: true });
  }

  console.log("→ Running STATIC_EXPORT=1 next build");
  execSync("next build", {
    cwd: root,
    stdio: "inherit",
    env: { ...process.env, STATIC_EXPORT: "1" },
  });

  console.log("\n✓ Next export complete: out/");
  console.log("→ Downloading & inlining Wikimedia images for offline use");
  execSync("node scripts/fetch-images.mjs", { cwd: root, stdio: "inherit" });
  execSync("node scripts/inline-images.mjs", { cwd: root, stdio: "inherit" });
  console.log("\n✓ Bundle ready: out/");
  console.log("  Demo routes:");
  console.log("    out/demo/index.html");
  console.log("    out/demo/family-day/index.html");
  console.log("    out/demo/cultural-day/index.html");
  console.log("    out/demo/golden-night/index.html");
} catch (err) {
  console.error("✗ Build failed:", err.message);
  process.exitCode = 1;
} finally {
  restore();
}
