#!/usr/bin/env python3
"""Render the fractalyze.io diagrams into this directory.

The org profile shows three drawings that also exist on the website. They are
React components there, not files, so the only way to keep the two in step is to
photograph the real thing: start the site, point a headless Chrome at it, and
clip each component out of the rendered page.

    cd website && npm run build && npm run start &
    python3 render-diagrams.py

Every drawing is rendered twice. GitHub serves a README in the viewer's theme
and the site is drawn on white, so the dark pass swaps the site's ink and paper
before capturing; the README picks between them with prefers-color-scheme.

The site has no dark mode of its own — DARK_CSS below is this script's
invention, and is the one thing here that can look wrong without the website
being wrong. Check the output.
"""

import base64
import json
import os
import subprocess
import sys
import time
import urllib.request

import websocket

CHROME = "/home/a41/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"
ORIGIN = os.environ.get("SITE_ORIGIN", "http://localhost:3000")
PORT = 9250
OUT = os.path.dirname(os.path.abspath(__file__))

# 1920 is the width the design was drawn at, and the width at which the root font
# size is 16px — below it the desktop layout scales down and the drawings come
# out smaller than they were designed. 2x for a display that is not 1x.
WIDTH, SCALE = 1920, 2

# Each drawing is found by the heading of the section it sits in, then narrowed
# to the element that is the drawing itself, so that the README can supply its
# own headings and prose.
TARGETS = [
    ("computing-layer", "/", "From Complexity to Production", "div.grid"),
    ("pipeline", "/compiler", "From Python to the Hardware", "ol"),
    ("benchmark", "/compiler", "The Verifiable Difference a Compiler Makes", "div.rounded-2xl"),
]

# Tailwind compiles the palette to hex rather than custom properties, so the dark
# pass overrides the classes themselves. The accent stays: it is the brand, it
# carries the bars and the chips, and it reads on either background — which is
# why the text on top of it has to be forced back to ink after the sweep.
DARK_CSS = """
  .bg-paper   { background-color: #0d1117 !important; }
  .bg-surface { background-color: #161b22 !important; }
  /* The computing-layer pair argues by contrast: a light card beside a black
     one. Darkening the light card to #161b22 puts it a hair off the black panel
     opposite and the argument disappears, so the Today side is lifted instead,
     and everything nested in it lifts with it to stay legible. `.grid >` picks
     out that panel alone — the benchmark card is also .bg-surface and should
     stay where it is. */
  .grid > .bg-surface                { background-color: #21262d !important; }
  .grid > .bg-surface .bg-paper      { background-color: #161b22 !important; }
  .grid > .bg-surface .bg-surface    { background-color: #21262d !important; }
  .text-ink   { color: #e6edf3 !important; }
  .text-muted { color: #9198a1 !important; }
  .border-line, .border-line\\/60 { border-color: #30363d !important; }
  /* Anything sitting on the accent keeps dark text — the chips, the layer rows,
     the hardware bar. Same element carries both classes. */
  .bg-accent.text-ink, .bg-accent-blue.text-ink,
  .bg-accent .text-ink, .bg-accent-blue .text-ink { color: #0d1117 !important; }
  /* The one accent that is not opaque. Every other accent block keeps its own
     colour through the sweep, but this one is 40% over whatever is behind it,
     and behind it here is near-black, which desaturates it to a grey. It ends up
     duller than the eleven chips it is supposed to answer, inverting the
     emphasis the pair is drawn to make. Deep rather than pale, since the text on
     it goes light in this pass where the chips' text goes dark. */
  .bg-accent\\/40 { background-color: #2f2b4d !important; }
  /* The pipeline's connector is a black hairline and would vanish. The black
     panel opposite the Today one is a div and must stay black. */
  span.bg-ink { background-color: #6e7681 !important; }
  .bg-line-strong { background-color: #6e7681 !important; }
"""

PAD = 24


def main() -> int:
    chrome = subprocess.Popen(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
         f"--force-device-scale-factor={SCALE}",
         f"--remote-debugging-port={PORT}", "--remote-allow-origins=*", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    try:
        tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
        ws = websocket.create_connection(
            [t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"], timeout=60)
    except Exception as exc:  # noqa: BLE001 - the message is the whole point
        chrome.kill()
        print(f"could not attach to Chrome: {exc}", file=sys.stderr)
        return 1

    counter = [0]

    def send(method, **params):
        counter[0] += 1
        ws.send(json.dumps({"id": counter[0], "method": method, "params": params}))
        while True:
            reply = json.loads(ws.recv())
            if reply.get("id") == counter[0]:
                if "error" in reply:
                    raise RuntimeError(f"{method}: {reply['error']}")
                return reply

    def evaluate(expression):
        r = send("Runtime.evaluate", returnByValue=True, expression=expression)
        return r["result"]["result"].get("value")

    send("Page.enable")
    send("Emulation.setDeviceMetricsOverride",
         width=WIDTH, height=1200, deviceScaleFactor=SCALE, mobile=False)
    # Reveal fades blocks in on scroll and bails out entirely under reduced
    # motion, which is the difference between capturing the drawing and
    # capturing it mid-fade.
    send("Emulation.setEmulatedMedia",
         features=[{"name": "prefers-reduced-motion", "value": "reduce"}])

    written = []
    for name, path, heading, selector in TARGETS:
        send("Page.navigate", url=ORIGIN + path)
        time.sleep(4)

        for theme in ("light", "dark"):
            if theme == "dark":
                evaluate(
                    "(() => { const s = document.createElement('style');"
                    f" s.id = 'dark-pass'; s.textContent = {json.dumps(DARK_CSS)};"
                    " document.head.appendChild(s); })()")
                time.sleep(0.6)

            box = evaluate(f"""
              (() => {{
                const h = [...document.querySelectorAll('h2')]
                  .find(x => x.textContent.includes({json.dumps(heading)}));
                if (!h) return null;
                const el = h.closest('section').querySelector({json.dumps(selector)});
                if (!el) return null;
                const r = el.getBoundingClientRect();
                return JSON.stringify({{x: r.x + scrollX, y: r.y + scrollY,
                                       w: r.width, h: r.height}});
              }})()""")
            if not box:
                raise SystemExit(f"{name}: no element for {heading!r} / {selector!r}")
            b = json.loads(box)

            shot = send("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                        clip={"x": b["x"] - PAD, "y": b["y"] - PAD,
                              "width": b["w"] + PAD * 2, "height": b["h"] + PAD * 2,
                              "scale": SCALE})["result"]["data"]
            raw = base64.b64decode(shot)
            out = os.path.join(OUT, f"{name}-{theme}.png")
            with open(out, "wb") as fh:
                fh.write(raw)
            written.append((os.path.basename(out), b["w"], b["h"], len(raw)))

            if theme == "dark":
                evaluate("document.getElementById('dark-pass')?.remove()")

    ws.close()
    chrome.kill()
    for filename, w, h, size in written:
        print(f"{filename:26s} {w:.0f}x{h:.0f} css  {size // 1024:>5d}K")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
