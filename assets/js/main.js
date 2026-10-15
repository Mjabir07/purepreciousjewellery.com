// Site-wide behaviour: header, mobile nav, reveal-on-scroll, collection filter,
// product lightbox and the enquiry form (opens WhatsApp / email — no backend needed).

const WHATSAPP = "971501348382";
const EMAIL = "purepreciousjew@gmail.com";

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

// Enquiry form -> WhatsApp or email
const form = document.getElementById("enquiry-form");
if (form) {
  const build = () => {
    const d = Object.fromEntries(new FormData(form));
    return [
      "Custom design enquiry — Pure Precious Jewellery",
      `Name: ${d.name || "-"}`,
      `Phone: ${d.phone || "-"}`,
      `Piece type: ${d.type || "-"}`,
      `Metal / stones: ${d.material || "-"}`,
      `Details: ${d.message || "-"}`,
    ].join("\n");
  };
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const via = e.submitter?.dataset.via || "whatsapp";
    const text = build();
    if (via === "email") {
      location.href = `mailto:${EMAIL}?subject=${encodeURIComponent("Custom design enquiry")}&body=${encodeURIComponent(text)}`;
    } else {
      window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}`, "_blank", "noopener");
    }
  });
}

document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
