import Link from "next/link";

export const metadata = {
  title: "For Garry — Day Composer",
};

interface DemoEntry {
  href: string;
  number: string;
  title: string;
  template: string;
  mood: string;
  hero: string; // direct image URL
  blurb: string;
  meta: string;
}

const DEMOS: DemoEntry[] = [
  {
    href: "/demo/family-day",
    number: "I",
    title: "A South Bay decompression",
    template: "Polaroid Keepsake",
    mood: "restorative · sun-warmed · lingering",
    blurb:
      "When the city week leaves you hollow, drive south. Four slow stops — an adobe in afternoon light, a lakeside park, a walk-in Vietnamese spot you can bring the kid to, and a coffee on the way home.",
    meta: "Sat · Jan 10 · 14:30–21:00 · with partner + toddler",
    hero:
      "https://upload.wikimedia.org/wikipedia/commons/4/46/Sandy_Wool_Lake_in_Ed_R._Levin_Country_Park.JPG",
  },
  {
    href: "/demo/cultural-day",
    number: "II",
    title: "A cinematic line through the city",
    template: "Cinematic Editorial",
    mood: "cinematic · vlog-ready · walkable",
    blurb:
      "A Saturday that stays in the frame. Sightglass north light to start, the SFMOMA photography wing for an anchor, Yerba Buena's lawn to let the kid run, and Burma Superstar's tableside tea-leaf salad as the hero shot.",
    meta: "Sat · Jan 17 · 10:00–19:30 · walk + uber",
    hero:
      "https://upload.wikimedia.org/wikipedia/commons/5/57/2017_SFMOMA_from_Yerba_Buena_Gardens.jpg",
  },
  {
    href: "/demo/golden-night",
    number: "III",
    title: "The same line, closing on golden hour",
    template: "Aurora Romance",
    mood: "cinematic · golden-hour · vertical close",
    blurb:
      "The cinematic line, recut for the night. Same opening through SFMOMA and Burma, but the closing lifts vertically — nineteen floors up at Top of the Mark, north window facing the Golden Gate as the city lights itself.",
    meta: "Sat · Jan 24 · 10:00–21:00 · walk + uber",
    hero:
      "https://upload.wikimedia.org/wikipedia/commons/4/4d/Top_of_the_Mark_%2816683414895%29.jpg",
  },
];

export default function DemoIndex() {
  return (
    <main
      style={{
        background: "#F4F1E8",
        minHeight: "100vh",
        padding: "60px 40px 80px",
        fontFamily: "system-ui, sans-serif",
        color: "#1c1814",
      }}
    >
      <header style={{ maxWidth: 1180, margin: "0 auto 56px" }}>
        <div
          style={{
            fontSize: 11,
            letterSpacing: ".3em",
            textTransform: "uppercase",
            color: "#8a8a85",
            marginBottom: 14,
          }}
        >
          Day Composer · for Garry
        </div>
        <h1
          style={{
            fontFamily: "var(--font-fraunces), 'Times New Roman', serif",
            fontWeight: 300,
            fontSize: 72,
            letterSpacing: "-.03em",
            lineHeight: 0.95,
            margin: 0,
            marginBottom: 18,
          }}
        >
          Garry — here are three Saturdays{" "}
          <em style={{ color: "#8b4a4a" }}>I&apos;ve put together for you.</em>
        </h1>
        <p
          style={{
            fontFamily: "var(--font-fraunces), serif",
            fontStyle: "italic",
            fontWeight: 300,
            fontSize: 20,
            color: "#5a554c",
            maxWidth: 780,
            lineHeight: 1.5,
            margin: 0,
          }}
        >
          Three different days, all built around what you said you wanted —
          cinematic frames, kid-friendly windows, walkable density, food with
          opinion. Pick the one that fits the week you&apos;ve had. Open any of
          them to see the whole thing laid out.
        </p>
      </header>

      <ul
        style={{
          listStyle: "none",
          padding: 0,
          margin: "0 auto",
          maxWidth: 1180,
          display: "grid",
          gap: 28,
        }}
      >
        {DEMOS.map((d) => (
          <li key={d.href}>
            <Link
              href={d.href}
              className="demo-link"
              style={{
                display: "grid",
                gridTemplateColumns: "320px 1fr auto",
                gap: 36,
                alignItems: "stretch",
                padding: 0,
                background: "#fff",
                border: "2px solid #1c1814",
                textDecoration: "none",
                color: "#1c1814",
                transition: "transform .2s, box-shadow .2s",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  position: "relative",
                  minHeight: 240,
                  width: "100%",
                  background: `url(${d.hero}) center/cover`,
                  display: "flex",
                  alignItems: "flex-end",
                  padding: 18,
                  color: "#fff",
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    inset: 0,
                    background:
                      "linear-gradient(to bottom,rgba(0,0,0,0) 40%,rgba(0,0,0,.7) 100%)",
                  }}
                />
                <span
                  style={{
                    position: "absolute",
                    top: 14,
                    left: 14,
                    fontFamily: "monospace",
                    fontSize: 11,
                    letterSpacing: ".24em",
                    background: "rgba(0,0,0,.55)",
                    padding: "4px 10px",
                    backdropFilter: "blur(6px)",
                  }}
                >
                  {d.number}
                </span>
                <span
                  style={{
                    position: "relative",
                    zIndex: 2,
                    fontFamily: "var(--font-fraunces), serif",
                    fontStyle: "italic",
                    fontSize: 18,
                    textShadow: "0 2px 12px rgba(0,0,0,.6)",
                  }}
                >
                  {d.template}
                </span>
              </div>
              <div style={{ padding: "28px 4px 28px 0" }}>
                <div
                  style={{
                    fontSize: 10,
                    letterSpacing: ".28em",
                    textTransform: "uppercase",
                    color: "#8b4a4a",
                    marginBottom: 8,
                    fontWeight: 700,
                  }}
                >
                  Day {d.number}
                </div>
                <h2
                  style={{
                    fontFamily: "var(--font-fraunces), serif",
                    fontWeight: 400,
                    fontSize: 34,
                    letterSpacing: "-.015em",
                    margin: 0,
                    marginBottom: 12,
                    lineHeight: 1.05,
                  }}
                >
                  {d.title}
                </h2>
                <p
                  style={{
                    fontSize: 15,
                    lineHeight: 1.7,
                    color: "#2c2820",
                    margin: 0,
                    marginBottom: 14,
                    maxWidth: 620,
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
                    marginBottom: 6,
                  }}
                >
                  {d.meta}
                </div>
                <div
                  style={{
                    fontFamily: "monospace",
                    fontSize: 10,
                    letterSpacing: ".24em",
                    textTransform: "uppercase",
                    color: "#a8a195",
                  }}
                >
                  mood · {d.mood}
                </div>
              </div>
              <div
                style={{
                  alignSelf: "center",
                  paddingRight: 28,
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
          maxWidth: 1180,
          margin: "60px auto 0",
          paddingTop: 24,
          borderTop: "1px solid #d4d2cc",
          fontFamily: "var(--font-fraunces), serif",
          fontStyle: "italic",
          fontWeight: 300,
          fontSize: 18,
          color: "#5a554c",
          lineHeight: 1.6,
          display: "grid",
          gap: 14,
        }}
      >
        <p style={{ margin: 0, maxWidth: 720 }}>
          Each day reads as a single page — no app shell, no controls. The way
          they look is the way you&apos;d send them to someone. Want me to
          re-compose any of them, just say which.
        </p>
        <div
          style={{
            fontFamily: "monospace",
            fontSize: 10,
            letterSpacing: ".24em",
            textTransform: "uppercase",
            color: "#a8a195",
            fontStyle: "normal",
          }}
        >
          — Day Composer ·{" "}
          <Link href="/preview" style={{ color: "#8b4a4a" }}>
            also: /preview switcher
          </Link>
        </div>
      </footer>

      <style>{`
        .demo-link:hover {
          transform: translate(-3px,-3px);
          box-shadow: 6px 6px 0 #1c1814;
        }
        @media (max-width: 860px) {
          .demo-link {
            grid-template-columns: 1fr !important;
          }
          .demo-link > div:nth-child(3) {
            padding: 18px !important;
          }
        }
      `}</style>
    </main>
  );
}
