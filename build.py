"""Build hacs.luukza.com: wraps each page in src/ with the shared layout into site/.

No dependencies beyond Python 3. Run after editing anything in src/:

    python3 build.py

Each file in src/ starts with a metadata comment:

    <!-- title: Page title | description: One sentence | path: hvac-simulators/help | nav: hvac -->

``path`` is where it's served ("" for the home page). ``nav`` marks the active
menu item (home, hvac, archiver).
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"
SITE_URL = "https://hacs.luukza.com"

NAV = [
    ("hvac", "HVAC Simulators", "/hvac-simulators/"),
    ("hvac-help", "HVAC help", "/hvac-simulators/help/"),
    ("archiver", "History Archiver", "/history-archiver/"),
    ("archiver-help", "Archiver help", "/history-archiver/help/"),
]

SUN = (
    '<svg class="theme-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<circle cx="12" cy="12" r="4.5"/><path stroke-linecap="round" d="M12 3v1.5M12 19.5V21M4.5 12H3M21 12h-1.5'
    'M5.6 5.6l1.05 1.05M17.35 17.35l1.05 1.05M18.4 5.6l-1.05 1.05M6.65 17.35l-1.05 1.05"/></svg>'
)
MOON = (
    '<svg class="theme-dark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>'
)
BURGER = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<path stroke-linecap="round" d="M4 6h16M4 12h16M4 18h16"/></svg>'
)

LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#1b6f5f">
<link rel="icon" href="/assets/logo-mark.svg" type="image/svg+xml">
<script>
(function () {{
  try {{
    var s = localStorage.getItem("hacs-luukza-theme");
    var dark = s === "dark" || (s !== "light" && window.matchMedia("(prefers-color-scheme: dark)").matches);
    document.documentElement.classList.toggle("dark", dark);
  }} catch (e) {{}}
}})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
</head>
<body>
<nav class="nav" aria-label="Main">
  <div class="nav-inner">
    <a class="brand" href="/"><img src="/assets/logo-mark.svg" alt=""><span>Luukza <small>HACS</small></span></a>
    <div class="nav-links">{nav_links}</div>
    <div class="nav-actions">
      <button class="icon-btn" data-theme-toggle aria-label="Toggle light/dark theme">{sun}{moon}</button>
      <button class="icon-btn menu-btn" data-menu-toggle aria-label="Menu" aria-expanded="false">{burger}</button>
    </div>
  </div>
  <div class="mobile-menu">{mobile_links}</div>
</nav>
<main>
{content}
</main>
<footer class="footer">
  <div class="footer-inner">
    <div>
      <a class="brand" href="/"><img src="/assets/logo-mark.svg" alt=""><span>Luukza <small>HACS</small></span></a>
      <p style="margin-top:1rem">Home Assistant integrations for understanding your home: installed through HACS, running locally.</p>
    </div>
    <div>
      <h4>HVAC Simulators</h4>
      <ul>
        <li><a href="/hvac-simulators/">Features</a></li>
        <li><a href="/hvac-simulators/help/">Help &amp; setup</a></li>
        <li><a href="https://github.com/meyerjoshua123/ha_hvac_simulators">GitHub</a></li>
        <li><a href="https://github.com/meyerjoshua123/ha_hvac_simulators/releases">Releases</a></li>
      </ul>
    </div>
    <div>
      <h4>History Archiver</h4>
      <ul>
        <li><a href="/history-archiver/">Features</a></li>
        <li><a href="/history-archiver/help/">Help &amp; setup</a></li>
        <li><a href="https://github.com/meyerjoshua123/ha-history-archiver">GitHub</a></li>
      </ul>
    </div>
    <div>
      <h4>More</h4>
      <ul>
        <li><a href="https://luukza.com">luukza.com</a></li>
        <li><a href="https://hacs.xyz">About HACS</a></li>
        <li><a href="https://www.home-assistant.io">Home Assistant</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 Luukza · Hobby projects, provided as-is under the MIT licence.</p>
    <p>HVAC Simulators and this site were built with the help of <a href="https://claude.com/claude-code">Claude Code</a>.</p>
  </div>
</footer>
</body>
</html>
"""

META_RE = re.compile(r"^<!--(.*?)-->\s*", re.S)


def parse_meta(text: str) -> tuple[dict[str, str], str]:
    match = META_RE.match(text)
    if not match:
        raise ValueError("page is missing its metadata comment")
    meta = {}
    for part in match.group(1).split("|"):
        key, _, value = part.partition(":")
        meta[key.strip()] = value.strip()
    return meta, text[match.end():]


def nav_html(active: str) -> tuple[str, str]:
    links = []
    for key, label, href in NAV:
        current = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{href}"{current}>{label}</a>')
    return "".join(links), "".join(links)


def build() -> list[str]:
    written = []
    for page in sorted(SRC.glob("*.html")):
        meta, body = parse_meta(page.read_text())
        path = meta.get("path", "").strip("/")
        out = OUT / path / "index.html" if path else OUT / "index.html"
        if meta.get("path") == "404":
            out = OUT / "404.html"
        nav_links, mobile_links = nav_html(meta.get("nav", ""))
        title = meta["title"]
        full_title = title if title.startswith("Luukza") else f"{title} | Luukza HACS"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            LAYOUT.format(
                title=html.escape(full_title),
                description=html.escape(meta.get("description", "")),
                url=f"{SITE_URL}/{path + '/' if path and path != '404' else ''}",
                nav_links=nav_links,
                mobile_links=mobile_links,
                sun=SUN,
                moon=MOON,
                burger=BURGER,
                content=body.strip(),
            )
        )
        written.append(str(out.relative_to(ROOT)))
    return written


if __name__ == "__main__":
    for path in build():
        print("wrote", path)
