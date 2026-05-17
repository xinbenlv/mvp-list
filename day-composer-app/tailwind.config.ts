import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Per-template font stacks (next/font assigns CSS variables on body)
        fraunces: ["var(--font-fraunces)", "serif"],
        inter: ["var(--font-inter)", "sans-serif"],
        mono: ["var(--font-jetbrains)", "monospace"],
        // Polaroid Keepsake
        playfair: ["var(--font-playfair)", "serif"],
        crimson: ["var(--font-crimson)", "serif"],
        caveat: ["var(--font-caveat)", "cursive"],
        elite: ["var(--font-elite)", "monospace"],
        // Cinematic Editorial
        bodoni: ["var(--font-bodoni)", "serif"],
        dm: ["var(--font-dm-sans)", "sans-serif"],
        // Aurora Romance
        cormorant: ["var(--font-cormorant)", "serif"],
        dmmono: ["var(--font-dm-mono)", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
