/**
 * Post-process the static export to inline Wikimedia images locally,
 * so the bundle works offline.
 *
 * Reads every .html file under out/, replaces every Wikimedia hotlink
 * with the matching local file in out/images/wm/, using a relative path
 * computed from the HTML file's depth.
 *
 * Run AFTER `pnpm build:static` and after the images have been downloaded
 * to out/images/wm/.
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from "node:fs";
import { resolve, relative, dirname } from "node:path";

const root = resolve(import.meta.dirname, "..");
const outDir = resolve(root, "out");
const imagesDir = resolve(outDir, "images/wm");

// Pull list of files we have locally.
const localFiles = new Set(readdirSync(imagesDir));

// Map Wikimedia commons URL (with /thumb/ or full) → local basename.
// We strip the path before /commons/ and take the last segment as filename.
function basenameOfUrl(url) {
  // Strip JSON-escape trailing backslash if present, then decode.
  const cleaned = url.replace(/\\+$/, "");
  const decoded = decodeURIComponent(cleaned);
  const parts = decoded.split("/");
  return parts[parts.length - 1];
}

function findHtmlFiles(dir, acc = []) {
  for (const name of readdirSync(dir)) {
    const full = resolve(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) findHtmlFiles(full, acc);
    else if (name.endsWith(".html")) acc.push(full);
  }
  return acc;
}

let totalReplacements = 0;
let filesTouched = 0;

const wmRegex =
  /https?:\\?\/\\?\/upload\.wikimedia\.org\/wikipedia\/commons\/(?:thumb\/)?[^"'\s)]+/g;

for (const html of findHtmlFiles(outDir)) {
  const original = readFileSync(html, "utf8");
  let replaced = original;
  let count = 0;

  // The URLs appear both raw and JSON-escaped (&, \\/, etc). Catch
  // both forms by re-stringifying matches.
  replaced = replaced.replace(wmRegex, (match) => {
    // Restore backslash escapes so basename works.
    const unesc = match.replace(/\\\//g, "/");
    const base = basenameOfUrl(unesc);
    if (!localFiles.has(base)) {
      console.warn(`  no local copy for ${base}`);
      return match;
    }
    const localAbs = resolve(imagesDir, base);
    const rel = relative(dirname(html), localAbs).replace(/\\/g, "/");
    count++;
    // Re-encode special chars in basename for URL safety.
    return rel.replace(/ /g, "%20");
  });

  if (count > 0) {
    writeFileSync(html, replaced);
    filesTouched++;
    totalReplacements += count;
    console.log(`  ${relative(outDir, html)} · ${count} replacements`);
  }
}

console.log(
  `\n✓ Rewrote ${totalReplacements} Wikimedia URL${
    totalReplacements === 1 ? "" : "s"
  } in ${filesTouched} HTML file${filesTouched === 1 ? "" : "s"}.`,
);
