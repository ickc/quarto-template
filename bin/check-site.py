#!/usr/bin/env python
"""Spot-check a rendered Quarto site in a headless browser, light and dark.

    python bin/check-site.py OUTPUT_DIR [PAGE ...]

PAGE is a path inside OUTPUT_DIR (default: index.html). Checks a few pages, not
the whole site: each page is loaded with the OS colour scheme emulated as light
and then dark, and fails if

- the dark theme is not applied when the OS asks for it;
- any visible inline `code` painted with a background of its own has a
  text/background contrast below 4.5:1 (WCAG AA), e.g. light text on a light
  chip in a dark-theme heading;
- the page has maths but MathJax 4 did not typeset it, or reports an error;
- TeX Gyre Schola did not load from font.kolen.dev;
- the page logs a JavaScript error.

Prints one line per page and theme, and exits non-zero if any check failed.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import re
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

# Runs in the page. Returns a list of problems with inline code contrast.
CONTRAST_JS = r"""
() => {
  const parse = (s) => {
    const m = s.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);
    return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  };
  // Effective background: composite translucent backgrounds up the tree.
  const background = (el) => {
    const layers = [];
    for (let e = el; e; e = e.parentElement) {
      const c = parse(getComputedStyle(e).backgroundColor);
      if (c && c[3] > 0) { layers.push(c); if (c[3] >= 1) break; }
    }
    let rgb = [255, 255, 255];
    for (const [r, g, b, a] of layers.reverse()) {
      rgb = [r * a + rgb[0] * (1 - a), g * a + rgb[1] * (1 - a), b * a + rgb[2] * (1 - a)];
    }
    return rgb;
  };
  const lum = ([r, g, b]) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const problems = [];
  for (const el of document.querySelectorAll("code")) {
    if (el.closest("pre") || !el.getClientRects().length) continue;
    // Only code painted as a chip of its own: unpainted code (as in the TOC and
    // navbar) is just text in the colour around it, which is the theme's call.
    const own = parse(getComputedStyle(el).backgroundColor);
    if (!own || own[3] === 0) continue;
    const fg = parse(getComputedStyle(el).color);
    const bg = background(el);
    const [l1, l2] = [lum(fg), lum(bg)].sort((a, b) => b - a);
    const ratio = (l1 + 0.05) / (l2 + 0.05);
    if (ratio < 4.5) {
      const where = el.parentElement.tagName.toLowerCase();
      problems.push(`${ratio.toFixed(2)}:1 in <${where}>: ${el.textContent.slice(0, 40)}`);
    }
  }
  return problems;
}
"""


def serve(root: Path) -> tuple[http.server.ThreadingHTTPServer, str]:
    handler = functools.partial(_QuietHandler, directory=str(root))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args) -> None:
        pass


def check(page, url: str, scheme: str, ignore: re.Pattern | None) -> list[str]:
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(f"JS error: {e}"))
    page.on(
        "console",
        lambda m: m.type == "error" and errors.append(f"console: {m.text[:200]}"),
    )
    page.goto(url, wait_until="networkidle")
    problems: list[str] = []

    dark = page.evaluate("document.body.classList.contains('quarto-dark')")
    if dark != (scheme == "dark"):
        problems.append(f"body is {'dark' if dark else 'light'}, OS asked for {scheme}")

    problems += [f"inline code contrast {p}" for p in page.evaluate(CONTRAST_JS)]

    if page.locator(".math").count():
        try:
            # "attached": the first one may be hidden, e.g. in a footnote.
            page.wait_for_selector("mjx-container", state="attached", timeout=20_000)
        except Exception:
            problems.append("maths present but MathJax did not typeset it")
        else:
            version = page.evaluate("window.MathJax && MathJax.version")
            if not str(version).startswith("4"):
                problems.append(f"MathJax {version}, expected 4")
            if page.locator("mjx-merror").count():
                problems.append("MathJax reports an error (mjx-merror)")

    page.evaluate("document.fonts.ready")
    if not page.evaluate("document.fonts.check('16px \"TeX Gyre Schola\"')"):
        problems.append("TeX Gyre Schola not loaded")

    problems += [e for e in errors if not (ignore and ignore.search(e))]
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("root", type=Path, help="the rendered site (Quarto's output-dir)")
    parser.add_argument("pages", nargs="*", default=["index.html"])
    parser.add_argument("--ignore-console", help="regex of console/JS errors to ignore")
    args = parser.parse_args()
    ignore = re.compile(args.ignore_console) if args.ignore_console else None

    server, base = serve(args.root)
    failed = False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for scheme in ("light", "dark"):
            context = browser.new_context(color_scheme=scheme)
            for path in args.pages:
                page = context.new_page()
                problems = check(page, base + path, scheme, ignore)
                page.close()
                status = "FAIL" if problems else "ok"
                print(f"{status:4} {scheme:5} {path}")
                for problem in problems:
                    print(f"       - {problem}")
                failed |= bool(problems)
            context.close()
        browser.close()
    server.shutdown()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
