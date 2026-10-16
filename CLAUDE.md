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

## Contact details & forms
- Email: info@purepreciousjewellery.com; phone/WhatsApp +971 50 134 8382; landline +971 4 285 9661.
- Contact page and Custom Design page forms (`form.js-enquiry`, handler in `assets/js/main.js`) send email via
  Web3Forms using `WEB3FORMS_KEY` in `tools/build_pages.py` (public key, safe in the repo). Empty key = falls
  back to the visitor's email app. "Send on WhatsApp" always works.

## Deploying — work on `demo`, release to `main`
- **All edits go to the `demo` branch.** GitHub Pages serves `demo` as the client preview link.
- **`main` is the live site** (Cloudflare Pages). Only update it when the user says to release/deploy live:
  `git checkout main && git merge --ff-only demo && git push origin main`, then return to `demo`.
  Batching edits this way keeps Cloudflare deploys (500/month free) low.
- Cloudflare runs `npx wrangler deploy` with `wrangler.jsonc` (assets = repo root). Anything that is not part of
  the public site must be listed in `.assetsignore`.
- Launched (Oct 2026): `DEMO = False` in `tools/build_pages.py`. The generator writes `robots.txt` and
  `sitemap.xml` and a canonical URL on every page pointing to https://purepreciousjewellery.com (so the GitHub
  Pages demo copy is not treated as a separate site). Add new pages to `PATHS` so they get into the sitemap.
- Before pushing, check pages in Playwright at desktop and ~390px width (no horizontal overflow, no console errors).
  Playwright's Chromium can't play H.264, so keep the WebM source first in `<video>`.

## Design tools
- `ui-ux-pro-max` skill (in `.claude/skills/`) for palettes, fonts, UX rules.
- 21st.dev MCP (`.mcp.json`) for component inspiration. The API key comes from the `TWENTY_FIRST_API_KEY`
  environment variable — never write the key into the repo. Free tier: `search` is free, but `get_component`
  code downloads are limited (2/day), so search first and only fetch the one you will use.
  Components are React/Tailwind; adapt them to this site's plain HTML/CSS and existing design tokens.
