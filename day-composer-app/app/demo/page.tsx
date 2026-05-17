import Link from "next/link";

export const metadata = {
  title: "Demo — Day Composer",
};

interface DemoEntry {
  href: string;
  number: string;
  persona: string;
  title: string;
  template: string;
  mood: string;
  blurb: string;
  swatch: string;
}

const DEMOS: DemoEntry[] = [
  {
    href: "/demo/family-day",
    number: "01",
    persona: "Garry",
    title: "A South Bay decompression",
    template: "Polaroid Keepsake",
    mood: "restorative · sun-warmed · lingering",
    blurb:
      "After a high-stim week in SF, four slow stops south of the city — adobe, lakeside, Vietnamese walk-in, coffee on the way home.",
    swatch:
      "linear-gradient(135deg,#F4ECDF 0%,#C28D8A 50%,#6B3D49 100%)",
  },
  {
    href: "/demo/cultural-day",
    number: "02",
    persona: "Garry",
    title: "A cinematic line through the city",
    template: "Cinematic Editorial",
    mood: "cinematic · vlog-ready · walkable",
    blurb:
      "Sightglass north light, SFMOMA's third floor, the Yerba Buena lawn, and Burma Superstar's tableside salad mix — one continuous frame.",
    swatch:
      "linear-gradient(155deg,#F8F6F0 0%,#0A0A0A 70%,#DD0F2C 100%)",
  },
  {
    href: "/demo/golden-night",
    number: "03",
    persona: "Garry",
    title: "A line closing on golden hour",
    template: "Aurora Romance",
    mood: "cinematic · golden-hour · vertical close",
    blurb:
      "The cinematic line, recut for night — drops the park, lifts the closing up to Top of the Mark's 19th-floor lights.",
    swatch:
      "radial-gradient(circle at 30% 30%,#FFD3B6 0%,transparent 55%),radial-gradient(circle at 70% 70%,#C97B8C 0%,transparent 60%),#FFF8F0",
  },
];

export default function DemoIndex() {
  return (
    <main
      style={{
        background: "#F4F1E8",
        minHeight: "100vh",
        padding: "60px 40px",
        fontFamily: "system-ui, sans-serif",
        color: "#1c1814",
      }}
    >
      <header style={{ maxWidth: 1100, margin: "0 auto 50px" }}>
        <div
          style={{
            fontSize: 11,
            letterSpacing: ".3em",
            textTransform: "uppercase",
            color: "#8a8a85",
            marginBottom: 14,
          }}
        >
          Day Composer · Demo Set
        </div>
        <h1
          style={{
            fontFamily:
              "var(--font-fraunces), 'Times New Roman', serif",
            fontWeight: 300,
            fontSize: 64,
            letterSpacing: "-.03em",
            lineHeight: 1,
            margin: 0,
            marginBottom: 16,
          }}
        >
          One persona,{" "}
          <em style={{ color: "#8b4a4a" }}>three Saturdays.</em>
        </h1>
        <p
          style={{
            fontFamily: "var(--font-fraunces), serif",
            fontStyle: "italic",
            fontWeight: 300,
            fontSize: 19,
            color: "#8a8a85",
            maxWidth: 720,
            lineHeight: 1.5,
            margin: 0,
          }}
        >
          Three different plans for the same person — Garry — each rendered in
          the template that best fits its mood. Click any to open the full page.
        </p>
      </header>

      <ul
        style={{
          listStyle: "none",
          padding: 0,
          margin: "0 auto",
          maxWidth: 1100,
          display: "grid",
          gap: 24,
        }}
      >
        {DEMOS.map((d) => (
          <li key={d.href}>
            <Link
              href={d.href}
              style={{
                display: "grid",
                gridTemplateColumns: "180px 1fr auto",
                gap: 32,
                alignItems: "center",
                padding: 28,
                background: "#fff",
                border: "2px solid #1c1814",
                textDecoration: "none",
                color: "#1c1814",
                transition: "transform .2s, box-shadow .2s",
              }}
              className="demo-link"
            >
              <div
                style={{
                  height: 180,
                  width: "100%",
                  background: d.swatch,
                  position: "relative",
                  display: "flex",
                  alignItems: "flex-end",
                  padding: 14,
                  color: "#fff",
                  fontFamily: "var(--font-fraunces), serif",
                  fontStyle: "italic",
                  fontSize: 18,
                  textShadow: "0 2px 12px rgba(0,0,0,.4)",
                  lineHeight: 1.1,
                }}
              >
                <span
                  style={{
                    position: "absolute",
                    top: 14,
                    left: 14,
                    fontFamily: "monospace",
                    fontSize: 11,
                    letterSpacing: ".24em",
                    background: "rgba(0,0,0,.55)",
                    padding: "4px 8px",
                  }}
                >
                  {d.number}
                </span>
                <span style={{ position: "relative", zIndex: 2 }}>
                  {d.template}
                </span>
              </div>
              <div>
                <div
                  style={{
                    fontSize: 10,
                    letterSpacing: ".28em",
                    textTransform: "uppercase",
                    color: "#8b4a4a",
                    marginBottom: 6,
                    fontWeight: 700,
                  }}
                >
                  Plan {d.number} · for {d.persona}
                </div>
                <h2
                  style={{
                    fontFamily: "var(--font-fraunces), serif",
                    fontWeight: 400,
                    fontSize: 32,
                    letterSpacing: "-.015em",
                    margin: 0,
                    marginBottom: 10,
                    lineHeight: 1.1,
                  }}
                >
                  {d.title}
                </h2>
                <p
                  style={{
                    fontSize: 14.5,
                    lineHeight: 1.65,
                    color: "#333",
                    margin: 0,
                    marginBottom: 10,
                  }}
                >
                  {d.blurb}
                </p>
                <div
                  style={{
                    fontFamily: "monospace",
                    fontSize: 11,
                    letterSpacing: ".14em",
                    textTransform: "uppercase",
                    color: "#8a8a85",
                  }}
                >
                  {d.mood}
                </div>
              </div>
              <div
                style={{
                  fontFamily: "monospace",
                  fontSize: 12,
                  letterSpacing: ".24em",
                  textTransform: "uppercase",
                  color: "#1c1814",
                  fontWeight: 700,
                }}
              >
                OPEN →
              </div>
            </Link>
          </li>
        ))}
      </ul>

      <footer
        style={{
          maxWidth: 1100,
          margin: "50px auto 0",
          paddingTop: 24,
          borderTop: "1px solid #d4d2cc",
          display: "flex",
          justifyContent: "space-between",
          fontFamily: "monospace",
          fontSize: 11,
          letterSpacing: ".16em",
          textTransform: "uppercase",
          color: "#8a8a85",
          flexWrap: "wrap",
          gap: 14,
        }}
      >
        <span>day-composer-app · demo set</span>
        <Link href="/preview" style={{ color: "#1c1814" }}>
          → also see /preview
        </Link>
      </footer>

      <style>{`
        .demo-link:hover {
          transform: translate(-3px,-3px);
          box-shadow: 6px 6px 0 #1c1814;
        }
      `}</style>
    </main>
  );
}
