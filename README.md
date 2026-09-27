# hacs.luukza.com

The website for Luukza's Home Assistant integrations: [HVAC Simulators](https://github.com/meyerjoshua123/ha_hvac_simulators) and [History Archiver](https://github.com/meyerjoshua123/ha-history-archiver). It has a features page and a detailed help page for each.

It's a plain static site styled after [luukza.com](https://luukza.com), using the same colour tokens, fonts and components but no framework, so there is nothing to install.

## Layout

| Path | What |
| :--- | :--- |
| `src/*.html` | Page content, each starting with a `<!-- title: … \| description: … \| path: … \| nav: … -->` comment |
| `build.py` | Wraps every page in the shared layout (head, nav, footer, theme) and writes `site/` |
| `site/` | The built site that gets published, including `site/assets/` (CSS, JS, logo) |

## Editing

1. Edit a page in `src/` (or `site/assets/site.css` for styling).
2. Run `python3 build.py`.
3. Commit both `src/` and `site/`.

## Cloudflare Pages

Connect this repository in **Cloudflare → Workers & Pages → Create → Pages → Connect to Git**:

| Setting | Value |
| :--- | :--- |
| Framework preset | None |
| Build command | *(leave empty)* |
| Build output directory | `site` |

Then add the custom domain under **Custom domains → `hacs.luukza.com`**. Because luukza.com is already on Cloudflare, the DNS record is created for you. Every push to `main` redeploys.

---

HVAC Simulators and this site were built with the help of [Claude Code](https://claude.com/claude-code).
