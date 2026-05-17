import type { Metadata } from "next";
import {
  Fraunces,
  Inter,
  JetBrains_Mono,
  Playfair_Display,
  Crimson_Pro,
  Caveat,
  Special_Elite,
  Bodoni_Moda,
  DM_Sans,
  Cormorant_Garamond,
  DM_Mono,
} from "next/font/google";
import "./globals.css";

// Shared
const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
  display: "swap",
});
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});
const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
  display: "swap",
});

// Polaroid
const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
  style: ["normal", "italic"],
  display: "swap",
});
const crimson = Crimson_Pro({
  subsets: ["latin"],
  variable: "--font-crimson",
  style: ["normal", "italic"],
  display: "swap",
});
const caveat = Caveat({
  subsets: ["latin"],
  variable: "--font-caveat",
  display: "swap",
});
const elite = Special_Elite({
  subsets: ["latin"],
  variable: "--font-elite",
  weight: "400",
  display: "swap",
});

// Cinematic
const bodoni = Bodoni_Moda({
  subsets: ["latin"],
  variable: "--font-bodoni",
  style: ["normal", "italic"],
  display: "swap",
});
const dmSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-dm-sans",
  display: "swap",
});

// Aurora
const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  variable: "--font-cormorant",
  weight: ["300", "400", "500", "700"],
  style: ["normal", "italic"],
  display: "swap",
});
const dmMono = DM_Mono({
  subsets: ["latin"],
  variable: "--font-dm-mono",
  weight: ["400", "500"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Day Composer",
  description: "A composed day, not a checklist.",
};

const fontVars = [
  fraunces.variable,
  inter.variable,
  jetbrains.variable,
  playfair.variable,
  crimson.variable,
  caveat.variable,
  elite.variable,
  bodoni.variable,
  dmSans.variable,
  cormorant.variable,
  dmMono.variable,
].join(" ");

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={fontVars}>
      <body>{children}</body>
    </html>
  );
}
