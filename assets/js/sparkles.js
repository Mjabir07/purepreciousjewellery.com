// Soft gold sparkles drifting around the hero video. Plain 2D canvas, no libraries.
const canvas = document.getElementById("hero-sparkles");
const hero = document.querySelector(".hero");

if (canvas && hero) {
  const ctx = canvas.getContext("2d");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let w = 0, h = 0, dpr = 1, stars = [], visible = true;
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = hero.clientWidth;
    h = hero.clientHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    // Sparkles cluster around the video frame (right side on desktop, top on mobile)
    const media = hero.querySelector(".hero-media").getBoundingClientRect();
    const hr = hero.getBoundingClientRect();
    const cx = media.left - hr.left + media.width / 2;
    const cy = media.top - hr.top + media.height / 2;
    const n = w < 760 ? 34 : 70;
    stars = Array.from({ length: n }, () => {
      const a = Math.random() * Math.PI * 2;
      const r = (0.45 + Math.random() * 0.75) * Math.max(media.width, media.height) * 0.75;
      return {
        x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r * 0.8,
        s: 1.5 + Math.random() * 4.5, p: Math.random() * Math.PI * 2,
        sp: 0.6 + Math.random() * 1.2, dx: (Math.random() - 0.5) * 6, dy: -2 - Math.random() * 6,
        depth: 0.3 + Math.random() * 0.9,
      };
    });
  }

  function star(x, y, size, alpha) {
    ctx.globalAlpha = alpha;
    const g = ctx.createRadialGradient(x, y, 0, x, y, size * 2.2);
    g.addColorStop(0, "rgba(255, 236, 170, 0.9)");
    g.addColorStop(1, "rgba(207, 162, 58, 0)");
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(x, y, size * 2.2, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = "#c9962c";
    ctx.beginPath();
    ctx.moveTo(x, y - size * 2); ctx.quadraticCurveTo(x, y, x + size * 2, y);
    ctx.quadraticCurveTo(x, y, x, y + size * 2); ctx.quadraticCurveTo(x, y, x - size * 2, y);
    ctx.quadraticCurveTo(x, y, x, y - size * 2); ctx.fill();
  }

  let t0 = performance.now();
  function frame(now) {
    requestAnimationFrame(frame);
    if (!visible) return;
    const t = (now - t0) / 1000;
    pointer.x += (pointer.tx - pointer.x) * 0.05;
    pointer.y += (pointer.ty - pointer.y) * 0.05;
    ctx.clearRect(0, 0, w, h);
    for (const s of stars) {
      const m = reduce ? 0 : 1;
      const x = s.x + s.dx * t * m * 0.3 + pointer.x * 18 * s.depth;
      let y = s.y + s.dy * t * m * 0.3 + pointer.y * 12 * s.depth;
      y = ((y % h) + h) % h;
      const tw = reduce ? 0.6 : Math.pow(0.5 + 0.5 * Math.sin(t * s.sp + s.p), 3);
      if (tw > 0.03) star(x, y, s.s * (0.5 + tw * 0.6), tw);
    }
    ctx.globalAlpha = 1;
  }

  window.addEventListener("resize", resize);
  window.addEventListener("pointermove", (e) => {
    pointer.tx = (e.clientX / window.innerWidth) * 2 - 1;
    pointer.ty = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; }).observe(hero);
  resize();
  requestAnimationFrame(frame);
}
