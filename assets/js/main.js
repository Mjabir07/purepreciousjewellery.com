// Site-wide behaviour: header, mobile nav, reveal-on-scroll, collection filter,
// product lightbox and the enquiry form (opens WhatsApp / email — no backend needed).

const WHATSAPP = "971501348382";
const EMAIL = "info@purepreciousjewellery.com";

document.documentElement.classList.remove("no-js");

// Header turns solid after scrolling; mobile nav toggle
const header = document.querySelector(".site-header");
const toggle = document.querySelector(".nav-toggle");
const onScroll = () => header.classList.toggle("is-solid", window.scrollY > 40);
onScroll();
window.addEventListener("scroll", onScroll, { passive: true });
toggle?.addEventListener("click", () => {
  const open = header.classList.toggle("is-open");
  toggle.setAttribute("aria-expanded", String(open));
});
document.querySelectorAll(".nav a").forEach((a) =>
  a.addEventListener("click", () => {
    header.classList.remove("is-open");
    toggle?.setAttribute("aria-expanded", "false");
  })
);

// Reveal on scroll
const revealEls = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  revealEls.forEach((el) => io.observe(el));
} else {
  revealEls.forEach((el) => el.classList.add("is-in"));
}

// Collection filter (collections page)
const chips = document.querySelectorAll(".chip[data-filter]");
const blocks = document.querySelectorAll(".cat-block");
function applyFilter(key, updateHash = true) {
  chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.filter === key)));
  blocks.forEach((b) => { b.hidden = key !== "all" && b.id !== key; });
  if (updateHash) history.replaceState(null, "", key === "all" ? location.pathname : "#" + key);
}
if (chips.length) {
  chips.forEach((c) => c.addEventListener("click", () => applyFilter(c.dataset.filter)));
  const fromHash = location.hash.slice(1);
  applyFilter([...blocks].some((b) => b.id === fromHash) ? fromHash : "all", false);
}

// Product lightbox
const lightbox = document.querySelector(".lightbox");
if (lightbox) {
  const media = lightbox.querySelector(".lightbox-media");
  const title = lightbox.querySelector("h3");
  const cat = lightbox.querySelector(".lb-cat");
  const wa = lightbox.querySelector(".lb-wa");
  let lastFocus = null;
  const thumbs = lightbox.querySelector(".lb-thumbs");
  const pic = (base, alt) =>
    `<picture><source srcset="${base}.webp" type="image/webp"><img src="${base}.jpg" alt="${alt.replace(/"/g, "&quot;")}"></picture>`;
  function showGallery(list, alt) {
    const show = (i) => {
      media.innerHTML = pic(list[i], alt);
      thumbs.querySelectorAll("button").forEach((b, j) => b.setAttribute("aria-current", String(i === j)));
    };
    thumbs.innerHTML = list.length > 1
      ? list.map((b, i) => `<button type="button" aria-label="Photo ${i + 1}">${pic(b, "")}</button>`).join("")
      : "";
    thumbs.querySelectorAll("button").forEach((b, i) => b.addEventListener("click", () => show(i)));
    show(0);
  }
  const close = () => { lightbox.classList.remove("is-open"); lastFocus?.focus(); document.body.style.overflow = ""; };
  document.querySelectorAll(".product").forEach((p) =>
    p.addEventListener("click", () => {
      lastFocus = p;
      showGallery(JSON.parse(p.dataset.gallery || "[]"), p.dataset.name);
      title.textContent = p.dataset.name;
      cat.textContent = p.dataset.cat;
      wa.href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(`Hello, I'm interested in "${p.dataset.name}" (${p.dataset.cat}). Could you share more details?`)}`;
      lightbox.classList.add("is-open");
      document.body.style.overflow = "hidden";
      lightbox.querySelector(".lightbox-close").focus();
    })
  );
  lightbox.addEventListener("click", (e) => { if (e.target === lightbox) close(); });
  lightbox.querySelector(".lightbox-close").addEventListener("click", close);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && lightbox.classList.contains("is-open")) close(); });
}

// Enquiry forms: "Send enquiry" emails the client via Web3Forms (falls back to the visitor's
// email app if no access key is set); "Send on WhatsApp" opens WhatsApp with the details.
const LABELS = { name: "Name", phone: "Phone", email: "Email", interest: "Interested in", type: "Piece type", material: "Metal / stones", message: "Message" };
document.querySelectorAll("form.js-enquiry").forEach((form) => {
  const status = form.querySelector(".form-status");
  const say = (msg, kind) => { status.textContent = msg; status.dataset.kind = kind || ""; };
  const summary = () => {
    const d = new FormData(form);
    return [form.dataset.title + " - Pure Precious Jewellery",
      ...Object.keys(LABELS).filter((k) => d.has(k)).map((k) => `${LABELS[k]}: ${d.get(k) || "-"}`)].join("\n");
  };
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    say("");
    if (!form.reportValidity()) return;
    const via = e.submitter?.dataset.via || "send";
    if (via === "whatsapp") {
      window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(summary())}`, "_blank", "noopener");
      return;
    }
    const key = form.querySelector('[name="access_key"]').value;
    if (!key) {
      location.href = `mailto:${EMAIL}?subject=${encodeURIComponent(form.dataset.title)}&body=${encodeURIComponent(summary())}`;
      return;
    }
    const btn = e.submitter;
    btn.disabled = true;
    say("Sending…");
    try {
      const data = Object.fromEntries(new FormData(form));
      if (data.email) data.replyto = data.email;
      const res = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data),
      });
      const out = await res.json().catch(() => ({}));
      if (!res.ok || !out.success) throw new Error(out.message || "failed");
      form.reset();
      say("Thank you — your message has been sent. We'll be in touch soon.", "ok");
    } catch (err) {
      say("Sorry, your message couldn't be sent. Please try again, or message us on WhatsApp.", "error");
    } finally {
      btn.disabled = false;
    }
  });
});

document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

// Reduced motion: keep tile videos still (they show their first frame / poster)
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  document.querySelectorAll("video[autoplay]").forEach((v) => { v.removeAttribute("autoplay"); v.pause(); });
}

// WhatsApp chat popup
const waBtn = document.querySelector(".wa-float[aria-controls]");
const waPanel = document.getElementById("wa-panel");
if (waBtn && waPanel) {
  const setOpen = (open) => {
    waPanel.hidden = !open;
    waBtn.setAttribute("aria-expanded", String(open));
    if (open) waPanel.querySelector(".wa-topics a")?.focus();
  };
  waBtn.addEventListener("click", () => setOpen(waPanel.hidden));
  waPanel.querySelector(".wa-close").addEventListener("click", () => { setOpen(false); waBtn.focus(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !waPanel.hidden) { setOpen(false); waBtn.focus(); } });
  document.addEventListener("click", (e) => { if (!waPanel.hidden && !e.target.closest(".wa-widget")) setOpen(false); });
}
