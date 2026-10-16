# Pure Precious Jewellery — project notes

Informational website (no online store) for Pure Precious Jewellery L.L.C, Gold Souq, Deira, Dubai.
The client has a **workshop / factory**, not a showroom — never call it a shop or showroom.

## How the site is built
- Static HTML/CSS/JS, no framework, no build step for hosting.
- **Do not hand-edit the `.html` files.** Edit `tools/build_pages.py` (layout, copy) and `products.json`
  (catalogue), then run `python3 tools/build_pages.py` to regenerate all pages.
- Styles: `assets/css/styles.css` (light ivory + gold + deep emerald; Cormorant / Montserrat).
- Home hero: necklace video in an arch (`assets/video/hero-necklace.{webm,mp4}`), sparkles in `assets/js/sparkles.js`.
- Product photos: `assets/img/products/<category>/<name>.{jpg,webp}` (about 1200px). Categories:
  `rings`, `necklaces-pendants`, `bracelets`, `earrings`. See README.md for the `products.json` format.
- When the user uploads raw photos (e.g. `WhatsApp Image ...jpeg`): check what each shows, move it to the right
  category with a descriptive dashed name, make jpg + webp, delete the original, add it to `products.json`, rebuild.

## Deploying
- Pushing to `main` deploys automatically: Cloudflare Pages (live) and GitHub Pages (demo link).
- `DEMO = True` in `tools/build_pages.py` plus `robots.txt` keep search engines out. At launch: set
  `DEMO = False`, rebuild, delete `robots.txt`, add a sitemap.
- Before pushing, check pages in Playwright at desktop and ~390px width (no horizontal overflow, no console errors).
  Playwright's Chromium can't play H.264, so keep the WebM source first in `<video>`.

## Design tools
- `ui-ux-pro-max` skill (in `.claude/skills/`) for palettes, fonts, UX rules.
- 21st.dev MCP (`.mcp.json`) for component inspiration. The API key comes from the `TWENTY_FIRST_API_KEY`
  environment variable — never write the key into the repo. Free tier: `search` is free, but `get_component`
  code downloads are limited (2/day), so search first and only fetch the one you will use.
  Components are React/Tailwind; adapt them to this site's plain HTML/CSS and existing design tokens.
