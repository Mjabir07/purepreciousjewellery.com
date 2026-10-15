"""Generates the site's HTML pages.

Usage (from the repo root):  python3 tools/build_pages.py
Products live in products.json: add an entry with name, detail and image
(path without extension; provide both .jpg and .webp), then re-run this script.
"""
import html, json, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
with open(os.path.join(ROOT, "products.json"), encoding="utf-8") as f:
    PRODUCTS = json.load(f)

def picture(base, alt, cls="", eager=False, focus=None):
    load = "eager" if eager else "lazy"
    c = f' class="{cls}"' if cls else ""
    st = f' style="object-position:{focus}"' if focus else ""
    return (f'<picture><source srcset="{base}.webp" type="image/webp">'
            f'<img{c} src="{base}.jpg" alt="{html.escape(alt)}" width="1200" height="1200" loading="{load}" decoding="async"{st}></picture>')

def images(item):
    return item.get("images") or [item["image"]]

def tile_media(k, ic):
    items = PRODUCTS.get(k) or []
    vid = next((it for it in items if it.get("video")), None)
    if vid:
        v = vid["video"]
        return (f'<video class="tile-photo" src="{v}.mp4" poster="{v}-poster.jpg" autoplay muted loop playsinline '
                f'preload="metadata" aria-label="{html.escape(vid["name"])}"></video>')
    if items:
        return picture(images(items[0])[0], items[0]["name"], "tile-photo", focus=items[0].get("focus"))
    return f'<div class="tile-art">{ICON[ic]}</div>'

PHONE1, PHONE1_RAW = "+971 50 134 8382", "+971501348382"
PHONE2, PHONE2_RAW = "+971 4 285 9661", "+97142859661"
EMAIL = "purepreciousjew@gmail.com"
WA = "https://wa.me/971501348382"
IG = "https://www.instagram.com/pure_precious_jewellery"
ADDR = ["Office F09, Hana &amp; Maryam Obaid", "Al Helo, Gold Souq, Deira", "Dubai, UAE"]
MAPQ = "https://www.google.com/maps/search/?api=1&query=Pure+Precious+Jewellery+Gold+Souq+Deira+Dubai"
MAPEMBED = "https://www.google.com/maps?q=77CX%2B337%20Al%20Ras%20Dubai&output=embed"

ICON = {
 "ring": '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><circle cx="32" cy="40" r="15"/><circle cx="32" cy="40" r="11" opacity=".5"/><path d="M26 22l6-9 6 9-6 7z"/><path d="M26 22h12M32 13v16" opacity=".6"/></svg>',
 "necklace": '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M10 12c2 20 12 30 22 30s20-10 22-30"/><path d="M32 42v4"/><path d="M32 46l-7 7 7 8 7-8z"/><path d="M25 53h14" opacity=".6"/></svg>',
 "bracelet": '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><ellipse cx="32" cy="34" rx="22" ry="18"/><ellipse cx="32" cy="34" rx="17" ry="13" opacity=".5"/><path d="M28 14l4-7 4 7-4 4z"/></svg>',
 "earring": '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M22 8c-6 0-6 9 0 9s6-9 0-9z" opacity=".0"/><circle cx="22" cy="12" r="3"/><path d="M22 15v8"/><path d="M22 23l-7 9 7 15 7-15z"/><circle cx="46" cy="12" r="3"/><path d="M46 15v8"/><path d="M46 23l-7 9 7 15 7-15z"/></svg>',
}
SVG = {
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.5 3.5A11 11 0 0 0 3.2 17.3L2 22l4.8-1.2A11 11 0 1 0 20.5 3.5zM12 20a9 9 0 0 1-4.6-1.3l-.3-.2-2.8.7.8-2.7-.2-.3A9 9 0 1 1 12 20zm5-6.7c-.3-.1-1.6-.8-1.8-.9s-.4-.1-.6.1-.7.9-.8 1-.3.2-.6.1a7.3 7.3 0 0 1-3.6-3.1c-.3-.5.3-.5.8-1.5.1-.2 0-.3 0-.5l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.800 11.800 0 0 0 4.600 4.100c1.700.7 2.400.8 3.200.7a2.700 2.700 0 0 0 1.800-1.300 2.200 2.200 0 0 0 .2-1.300c-.1-.1-.3-.2-.6-.3z"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.500 1.500a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.500 7-12a7 7 0 0 0-14 0c0 5.500 7 12 7 12z"/><circle cx="12" cy="10" r="2.500"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
}

CATS = [
 ("rings", "Rings", "ring", "Statement, solitaire & bespoke"),
 ("necklaces-pendants", "Necklaces &amp; Pendants", "necklace", "Chains, sets & pendants"),
 ("bracelets", "Bracelets", "bracelet", "Bangles, chains & cuffs"),
 ("earrings", "Earrings", "earring", "Studs, drops & hoops"),
]

NAV = [("index.html", "Home"), ("collections.html", "Collections"), ("custom-design.html", "Custom Design"), ("about.html", "About"), ("contact.html", "Contact")]

# Demo mode keeps search engines away until launch. Set to False when going live
# on purepreciousjewellery.com, re-run this script, and delete robots.txt.
DEMO = True

def head(title, desc, page):
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#fbf7ef">{'<meta name="robots" content="noindex, nofollow">' if DEMO else ''}
<link rel="icon" type="image/svg+xml" href="assets/img/ppj-emblem-gold.svg">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/og-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"JewelryStore","name":"Pure Precious Jewellery L.L.C","description":"Specialist in all kinds of 18K diamond and platinum jewellery, with custom designs made in our own factory.","telephone":"{PHONE1_RAW}","email":"{EMAIL}","sameAs":["{IG}"],"address":{{"@type":"PostalAddress","streetAddress":"Office F09, Hana and Maryam Obaid, Al Helo, Gold Souq, Deira","addressLocality":"Dubai","addressCountry":"AE"}}}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Pure Precious Jewellery — home">
      <img src="assets/img/ppj-emblem-gold.svg" alt="" width="46" height="46">
      <span class="brand-name">Pure Precious<small>Jewellery L.L.C</small></span>
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">
''' + "\n".join(f'      <a href="{h}"' + (' aria-current="page"' if h == page else "") + f'>{t}</a>' for h, t in NAV) + f'''
      <a class="btn btn--gold" href="{WA}" target="_blank" rel="noopener">WhatsApp</a>
    </nav>
  </div>
</header>
<main id="main">
'''

FOOT = f'''</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="assets/img/ppj-logo-light.svg" alt="Pure Precious Jewellery L.L.C" width="140" height="73">
        <p>Specialist in all kinds of 18K diamond &amp; platinum jewellery. Custom pieces crafted in our own factory.</p>
        <div class="socials">
          <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{SVG["ig"]}</a>
          <a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{SVG["wa"]}</a>
          <a href="mailto:{EMAIL}" aria-label="Email">{SVG["mail"]}</a>
        </div>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
''' + "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t in NAV) + f'''
        </ul>
      </div>
      <div>
        <h4>Collections</h4>
        <ul>
''' + "\n".join(f'          <li><a href="collections.html#{k}">{n}</a></li>' for k, n, _, _ in CATS) + f'''
        </ul>
      </div>
      <div>
        <h4>Visit us</h4>
        <address>
          <span>{"<br>".join(ADDR)}</span>
          <a href="tel:{PHONE1_RAW}">{PHONE1}</a>
          <a href="tel:{PHONE2_RAW}">{PHONE2}</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </address>
      </div>
    </div>
    <div class="footer-bottom"><span>&copy; <span data-year>2026</span> Pure Precious Jewellery L.L.C. All rights reserved.</span><span>Gold Souq, Deira, Dubai</span></div>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{SVG["wa"]}</a>
'''

def tail(extra=""):
    return extra + '<script type="module" src="assets/js/main.js"></script>\n</body>\n</html>\n'

def visit_block():
    return f'''
<section class="section section--alt" id="visit">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Visit our workshop</span>
      <h2 class="section-title">Find us in the <span class="gold-text">Gold Souq</span></h2>
      <div class="info-list">
        <div class="info-item"><span class="ico">{SVG["pin"]}</span><div><h4>Address</h4><p>{"<br>".join(ADDR)}</p></div></div>
        <div class="info-item"><span class="ico">{SVG["clock"]}</span><div><h4>Opening hours</h4><p>10:30 am – 1:30 pm<br>4:30 pm – 9:30 pm</p></div></div>
        <div class="info-item"><span class="ico">{SVG["phone"]}</span><div><h4>Call</h4><p><a href="tel:{PHONE1_RAW}">{PHONE1}</a><br><a href="tel:{PHONE2_RAW}">{PHONE2}</a></p></div></div>
        <div class="info-item"><span class="ico">{SVG["mail"]}</span><div><h4>Email</h4><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>
      </div>
      <div class="hero-actions"><a class="btn btn--gold" href="{MAPQ}" target="_blank" rel="noopener">Get directions</a><a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">{SVG["wa"]} WhatsApp</a></div>
    </div>
    <div class="map-box reveal" style="--d:.15s"><iframe title="Pure Precious Jewellery on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{MAPEMBED}"></iframe></div>
  </div>
</section>
'''

def cta_block(title, text, btn_text, btn_href):
    return f'''
<section class="section">
  <div class="container">
    <div class="cta reveal">
      <span class="eyebrow">Made for you</span>
      <h2 style="margin-top:14px">{title}</h2>
      <p>{text}</p>
      <div class="hero-actions"><a class="btn btn--gold" href="{btn_href}">{btn_text}</a><a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">{SVG["wa"]} Chat on WhatsApp</a></div>
    </div>
  </div>
</section>
'''

def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)

# ---------------- HOME ----------------
tiles = "\n".join(f'''      <a class="tile reveal" style="--d:{i*.08:.2f}s" href="collections.html#{k}">
        {tile_media(k, ic)}
        <div class="tile-body"><h3>{n}</h3><p>{sub}</p></div>
      </a>''' for i, (k, n, ic, sub) in enumerate(CATS))

words = ["18K Gold", "Diamond", "Platinum", "Custom Designs", "Made in Our Own Factory", "Gold Souq, Dubai"]
strip = "".join(f"<span>{w}</span>" for w in words * 2)

home = head("Pure Precious Jewellery L.L.C — 18K Diamond & Platinum Jewellery, Gold Souq Dubai",
            "Pure Precious Jewellery L.L.C in the Gold Souq, Deira, Dubai. Specialists in 18K diamond and platinum jewellery with custom designs made in our own factory.", "index.html")
home += f'''
<section class="hero" aria-label="Welcome">
  <canvas id="hero-sparkles" aria-hidden="true"></canvas>
  <div class="container hero-grid">
    <figure class="hero-media">
      <div class="arch">
        <video poster="assets/video/hero-necklace-poster.jpg" autoplay muted loop playsinline preload="auto" aria-label="Model wearing the Pure Precious diamond bib necklace">
          <source src="assets/video/hero-necklace.webm" type="video/webm">
          <source src="assets/video/hero-necklace.mp4" type="video/mp4">
        </video>
      </div>
      <a class="hero-tag" href="collections.html#necklaces-pendants"><span>Featured</span>Diamond Bib Necklace</a>
    </figure>
    <div class="hero-content">
      <span class="eyebrow">Gold Souq &middot; Deira &middot; Dubai</span>
      <h1><span class="gold-text">Pure Precious</span><span>Jewellery</span></h1>
      <p class="hero-sub">Specialist in all kinds of 18K diamond &amp; platinum jewellery</p>
      <p class="hero-text">Fine pieces for every occasion &mdash; and one-of-a-kind designs crafted to your vision in our own factory.</p>
      <div class="hero-actions">
        <a class="btn btn--gold" href="collections.html">Explore collections</a>
        <a class="btn btn--ghost" href="custom-design.html">Design your own</a>
      </div>
    </div>
  </div>
  <div class="scroll-cue" aria-hidden="true"><span>Scroll</span><i></i></div>
</section>

<div class="strip" aria-hidden="true"><div class="strip-track">{strip}</div></div>

<section class="section" id="collections">
  <div class="container">
    <div class="reveal">
      <span class="eyebrow">Collections</span>
      <h2 class="section-title">Crafted to be <span class="gold-text">treasured</span></h2>
      <p class="section-lead">From timeless solitaires to statement necklaces &mdash; browse our pieces by category.</p>
    </div>
    <div class="grid-4">
{tiles}
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container split">
    <figure class="frame frame--emblem reveal" style="margin:0">
      <img src="assets/img/ppj-emblem-gold.svg" alt="PPJ emblem" width="165" height="165">
      <figcaption>Custom made &middot; Our own factory</figcaption>
    </figure>
    <div class="reveal" style="--d:.12s">
      <span class="eyebrow">Custom design</span>
      <h2 class="section-title">Your vision, <span class="gold-text">made real</span></h2>
      <p class="section-lead">With our own factory, we craft unique, personalised pieces with expert design and quality materials &mdash; jewellery built around your story and the memories you want to keep.</p>
      <ul class="checklist">
        <li><span><strong>Personal design.</strong> Bring an idea, a sketch or a photo &mdash; we shape it with you.</span></li>
        <li><span><strong>Quality materials.</strong> 18K gold, diamonds and platinum.</span></li>
        <li><span><strong>Made in-house.</strong> Direct control of craftsmanship from design to finish.</span></li>
      </ul>
      <div class="hero-actions"><a class="btn btn--gold" href="custom-design.html">Start a custom piece</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">About us</span>
      <h2 class="section-title">Trusted in the <span class="gold-text">heart of Deira</span></h2>
      <p class="section-lead">Pure Precious Jewellery L.L.C is a custom jewellery dealer in Dubai&rsquo;s Gold Souq, focused on expert design, quality materials and lasting memories.</p>
      <div class="hero-actions"><a class="btn btn--ghost" href="about.html">Our story</a></div>
    </div>
    <ul class="checklist reveal" style="--d:.12s;margin:0">
      <li><span><strong>18K Diamond &amp; Platinum</strong> &mdash; our speciality.</span></li>
      <li><span><strong>Rings, necklaces &amp; pendants, bracelets, earrings.</strong></span></li>
      <li><span><strong>Bespoke work</strong> from our own factory.</span></li>
      <li><span><strong>Gold Souq workshop</strong> &mdash; visit us in Deira.</span></li>
    </ul>
  </div>
</section>
''' + visit_block() + FOOT + tail('<script src="assets/js/sparkles.js" defer></script>\n')
write("index.html", home)

# ---------------- COLLECTIONS ----------------
chips = '<button class="chip" data-filter="all" aria-pressed="true">All</button>' + "".join(
    f'<button class="chip" data-filter="{k}" aria-pressed="false">{n}</button>' for k, n, _, _ in CATS)

def product(k, n, ic, item):
    plain = html.unescape(n)
    name = html.escape(item["name"])
    detail = html.escape(item.get("detail", ""))
    label = f"{item['name']} — {item['detail']}" if item.get("detail") else item["name"]
    imgs = images(item)
    gallery = html.escape(json.dumps(imgs))
    more = f'<span class="product-count">{len(imgs)} photos</span>' if len(imgs) > 1 else ""
    return f'''        <button class="product reveal" type="button" data-name="{html.escape(label)}" data-cat="{plain}" data-gallery="{gallery}">
          <div class="product-media">{picture(imgs[0], label, focus=item.get("focus"))}{more}</div>
          <h3 class="product-name">{name}</h3>
          <p class="product-meta">{detail or "Enquire for details"}</p>
        </button>'''

def coming_soon(k, n, ic):
    plain = html.unescape(n)
    return f'''        <a class="product product--soon reveal" href="{WA}?text={plain.replace(' ', '%20').replace('&', '%26')}%20-%20please%20share%20your%20latest%20designs" target="_blank" rel="noopener">
          <div class="product-media">{ICON[ic]}</div>
          <h3 class="product-name">New designs coming soon</h3>
          <p class="product-meta">Ask us on WhatsApp</p>
        </a>'''

blocks = "\n".join(f'''  <section class="cat-block" id="{k}" aria-labelledby="h-{k}">
    <div class="container">
      <div class="cat-head"><h2 id="h-{k}">{n}</h2><span>{sub}</span></div>
      <div class="product-grid">
''' + ("\n".join(product(k, n, ic, it) for it in PRODUCTS.get(k, [])) or coming_soon(k, n, ic)) + '''
      </div>
    </div>
  </section>''' for k, n, ic, sub in CATS)

coll = head("Collections — Rings, Necklaces, Bracelets & Earrings | Pure Precious Jewellery",
            "Browse 18K diamond and platinum rings, necklaces & pendants, bracelets and earrings from Pure Precious Jewellery, Gold Souq Dubai.", "collections.html")
coll += f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Collections</span>
    <h1><span class="gold-text">Our</span> Jewellery</h1>
    <p>Rings, necklaces &amp; pendants, bracelets and earrings. Tap any piece to enquire on WhatsApp.</p>
  </div>
</section>
<div class="filter-bar"><div class="container"><div class="filter-list" role="group" aria-label="Filter by category">{chips}</div></div></div>
<div id="catalogue">
{blocks}
</div>
<div class="container"><p class="notice">A selection of our pieces &mdash; many more at our workshop. Prices on request; visit us or message us on WhatsApp.</p></div>
''' + cta_block("Can&rsquo;t find the perfect piece?", "Our factory can make it for you. Tell us what you have in mind.", "Design your own", "custom-design.html") + f'''
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Piece details">
  <button class="lightbox-close" type="button" aria-label="Close">&times;</button>
  <div class="lightbox-card">
    <div class="lightbox-gallery"><div class="lightbox-media"></div><div class="lb-thumbs"></div></div>
    <div class="lightbox-body">
      <span class="eyebrow lb-cat"></span>
      <h3></h3>
      <p>18K gold, diamond &amp; platinum options available. Message us for price, sizes and availability &mdash; or ask for a custom version.</p>
      <div class="hero-actions"><a class="btn btn--gold lb-wa" href="{WA}" target="_blank" rel="noopener">{SVG["wa"]} Enquire on WhatsApp</a></div>
    </div>
  </div>
</div>
''' + FOOT + tail()
write("collections.html", coll)

# ---------------- CUSTOM DESIGN ----------------
steps = [("Brief", "Share your idea, a sketch or a reference photo, plus budget and timeline."),
         ("Design", "Our designers turn the brief into a design for your review."),
         ("Approve", "Refine until it&rsquo;s exactly right and confirm materials and price."),
         ("Craft", "Your piece is made by our craftsmen in our own factory."),
         ("Delivery", "Finished, checked and handed to you &mdash; ready to be treasured.")]
steps_html = "\n".join(f'      <div class="step reveal" style="--d:{i*.08:.2f}s"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(steps))

custom = head("Custom Jewellery Design in Dubai | Pure Precious Jewellery",
              "Have a unique piece made. Pure Precious Jewellery crafts personalised 18K gold, diamond and platinum jewellery in its own factory in Dubai.", "custom-design.html")
custom += f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Custom design</span>
    <h1>Design <span class="gold-text">your own</span></h1>
    <p>Our own factory lets us create unique, personalised jewellery with expert design, quality materials and a focus on your vision &mdash; and the memories it will hold.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="reveal"><span class="eyebrow">How it works</span><h2 class="section-title">From idea to <span class="gold-text">heirloom</span></h2></div>
    <div class="steps">
{steps_html}
    </div>
  </div>
</section>

<section class="section section--alt" id="enquire">
  <div class="container split" style="align-items:start">
    <div class="reveal">
      <span class="eyebrow">Start your piece</span>
      <h2 class="section-title">Tell us <span class="gold-text">what you imagine</span></h2>
      <p class="section-lead">Fill in a few details and send them straight to us on WhatsApp or email. Have a sketch or photo? Attach it in the chat.</p>
      <ul class="checklist">
        <li><span>Rings, necklaces &amp; pendants, bracelets and earrings</span></li>
        <li><span>18K gold, diamonds and platinum</span></li>
        <li><span>Matching sets and personalised engraving</span></li>
      </ul>
    </div>
    <form class="form reveal" id="enquiry-form" style="--d:.12s" novalidate>
      <div class="form-row">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="f-phone">Phone / WhatsApp</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="f-type">Type of piece</label>
          <select id="f-type" name="type" required><option value="">Select…</option><option>Ring</option><option>Necklace / Pendant</option><option>Bracelet</option><option>Earrings</option><option>Full set</option><option>Other</option></select></div>
        <div class="field"><label for="f-mat">Metal / stones</label>
          <select id="f-mat" name="material"><option value="">Not sure yet</option><option>18K gold</option><option>Platinum</option><option>18K gold with diamonds</option><option>Platinum with diamonds</option></select></div>
      </div>
      <div class="field"><label for="f-msg">Your idea</label><textarea id="f-msg" name="message" placeholder="Describe the design, occasion, sizes, budget…" required></textarea></div>
      <div class="hero-actions" style="margin-top:6px">
        <button class="btn btn--gold" type="submit" data-via="whatsapp">{SVG["wa"]} Send on WhatsApp</button>
        <button class="btn btn--ghost" type="submit" data-via="email">Send by email</button>
      </div>
      <p class="form-note">This opens WhatsApp or your email app with your details filled in.</p>
    </form>
  </div>
</section>
''' + FOOT + tail()
write("custom-design.html", custom)

# ---------------- ABOUT ----------------
about = head("About | Pure Precious Jewellery L.L.C — Gold Souq, Dubai",
             "Pure Precious Jewellery L.L.C is a custom jewellery dealer in Dubai's Gold Souq, specialising in 18K diamond and platinum jewellery.", "about.html")
about += f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">About us</span>
    <h1>Pure Precious <span class="gold-text">Jewellery</span></h1>
    <p>A custom jewellery dealer in the Gold Souq, Deira &mdash; Dubai.</p>
  </div>
</section>

<section class="section">
  <div class="container split">
    <figure class="frame frame--emblem reveal" style="margin:0">
      <img src="assets/img/ppj-emblem-gold.svg" alt="PPJ emblem" width="165" height="165">
      <figcaption>Pure Precious Jewellery L.L.C</figcaption>
    </figure>
    <div class="reveal" style="--d:.12s">
      <span class="eyebrow">Our craft</span>
      <h2 class="section-title">Expert design. <span class="gold-text">Lasting memories.</span></h2>
      <p class="section-lead">We are specialists in all kinds of 18K diamond and platinum jewellery. As a custom jewellery dealer with our own factory, we craft unique, personalised pieces &mdash; combining expert design and quality materials with a clear focus on our clients&rsquo; vision.</p>
      <ul class="checklist">
        <li><span><strong>Specialists</strong> in 18K diamond &amp; platinum jewellery.</span></li>
        <li><span><strong>Own factory</strong> for custom and made-to-order designs.</span></li>
        <li><span><strong>Client-first.</strong> Every piece is shaped around your vision.</span></li>
        <li><span><strong>Gold Souq, Deira</strong> &mdash; Dubai&rsquo;s historic gold marketplace.</span></li>
      </ul>
    </div>
  </div>
</section>
''' + cta_block("Visit us or message us", "We&rsquo;d love to help you find or create something special.", "Contact us", "contact.html") + FOOT + tail()
write("about.html", about)

# ---------------- CONTACT ----------------
contact = head("Contact & Visit | Pure Precious Jewellery — Gold Souq, Deira, Dubai",
               "Visit Pure Precious Jewellery in the Gold Souq, Deira, Dubai. Call +971 50 134 8382, WhatsApp or email us.", "contact.html")
contact += f'''
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Contact</span>
    <h1>Visit <span class="gold-text">us</span></h1>
    <p>Visit our workshop, call, or message us on WhatsApp.</p>
  </div>
</section>
''' + visit_block() + FOOT + tail()
write("contact.html", contact)
print("ok")
