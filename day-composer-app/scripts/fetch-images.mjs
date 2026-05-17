/**
 * Download the 9 Wikimedia images used by /demo into out/images/wm/.
 * Idempotent — skips files already present. Resizes large ones with `sips`
 * (Mac built-in) to keep the bundle under ~5MB.
 *
 * Filenames are saved decoded (e.g. `Top_of_the_Mark_(16683414895).jpg`)
 * to match what inline-images.mjs expects after URL-decoding.
 */

import { execSync } from "node:child_process";
import {
  existsSync,
  mkdirSync,
  statSync,
} from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const outDir = resolve(root, "out/images/wm");
mkdirSync(outDir, { recursive: true });

// Each entry: [URL path under /commons/, target filename (decoded)]
const IMAGES = [
  ["8/82/Alviso_Adobe.JPG", "Alviso_Adobe.JPG"],
  [
    "4/46/Sandy_Wool_Lake_in_Ed_R._Levin_Country_Park.JPG",
    "Sandy_Wool_Lake_in_Ed_R._Levin_Country_Park.JPG",
  ],
  [
    "5/59/Banh_Xeo_with_fish_sauce_and_vegetables.jpg",
    "Banh_Xeo_with_fish_sauce_and_vegetables.jpg",
  ],
  [
    "a/ae/Philz_Coffee_-_24th-Folsom_-_SF%2C_CA.jpg",
    "Philz_Coffee_-_24th-Folsom_-_SF,_CA.jpg",
  ],
  [
    "6/65/Sightglass_Coffee_at_Boot_and_Shoe_Service_Cafe_%285991331999%29.jpg",
    "Sightglass_Coffee_at_Boot_and_Shoe_Service_Cafe_(5991331999).jpg",
  ],
  [
    "5/57/2017_SFMOMA_from_Yerba_Buena_Gardens.jpg",
    "2017_SFMOMA_from_Yerba_Buena_Gardens.jpg",
  ],
  ["a/a8/2017_Yerba_Buena_Gardens.jpg", "2017_Yerba_Buena_Gardens.jpg"],
  [
    "1/1c/Fermented_Tea_Leaf_Salad_%289319609945%29.jpg",
    "Fermented_Tea_Leaf_Salad_(9319609945).jpg",
  ],
  [
    "4/4d/Top_of_the_Mark_%2816683414895%29.jpg",
    "Top_of_the_Mark_(16683414895).jpg",
  ],
];

// Filenames to downsize after download (max 1600px). Skips files already small.
const RESIZE_TARGETS = new Set([
  "Sandy_Wool_Lake_in_Ed_R._Levin_Country_Park.JPG",
  "2017_SFMOMA_from_Yerba_Buena_Gardens.jpg",
  "2017_Yerba_Buena_Gardens.jpg",
]);

for (const [path, filename] of IMAGES) {
  const target = resolve(outDir, filename);
  if (existsSync(target)) {
    console.log(`  cached  ${filename}`);
    continue;
  }
  const url = `https://upload.wikimedia.org/wikipedia/commons/${path}`;
  console.log(`  fetch   ${filename}`);
  execSync(
    `curl -sL -A "DayComposerDemoBundle/1.0 (friend handoff)" "${url}" -o "${target}"`,
    { stdio: "inherit" },
  );
  if (RESIZE_TARGETS.has(filename)) {
    try {
      execSync(`sips -Z 1600 "${target}" --out "${target}" > /dev/null 2>&1`);
    } catch {
      console.warn(`    sips resize failed (not on macOS?) — skipping`);
    }
  }
  const bytes = statSync(target).size;
  console.log(`          ${(bytes / 1024).toFixed(0)} KB`);
}

console.log("✓ Images ready in out/images/wm/");
