// Animated 3D hero: a gold faceted gem (echoing the PPJ emblem) with orbiting
// rings, a wireframe outline and twinkling sparkles. Reacts to pointer and scroll.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const canvas = document.getElementById("hero-canvas");
const hero = document.querySelector(".hero");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const isSmall = window.matchMedia("(max-width: 760px)").matches;

function fail() {
  document.documentElement.classList.add("no-webgl");
}

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
} catch (e) {
  fail();
}

if (renderer) {
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, isSmall ? 1.5 : 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(36, 1, 0.1, 100);
  camera.position.set(0, 0.2, 11);

  // Warm key lights
  const key = new THREE.PointLight(0xffd98a, 60, 30, 2);
  key.position.set(4, 4, 6);
  const rim = new THREE.PointLight(0xffb347, 40, 30, 2);
  rim.position.set(-5, -2, 3);
  const under = new THREE.PointLight(0xffc766, 55, 30, 2);
  under.position.set(0, -5, 4);
  scene.add(key, rim, under, new THREE.AmbientLight(0xffffff, 0.15));

  const goldMat = new THREE.MeshStandardMaterial({
    color: 0xd9ac3c, metalness: 1, roughness: 0.3, envMapIntensity: 1.9, flatShading: true,
  });
  const goldSmooth = new THREE.MeshStandardMaterial({
    color: 0xd9ac3c, metalness: 1, roughness: 0.2, envMapIntensity: 1.6,
  });

  // The whole scene sits in a group so it can be offset right on wide screens
  const stage = new THREE.Group();
  scene.add(stage);

  // --- Brilliant-cut gem: crown + pavilion ---
  const gem = new THREE.Group();
  const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 1.1, 0.5, 8, 1), goldMat);
  crown.position.y = 0.25;
  const pavilion = new THREE.Mesh(new THREE.ConeGeometry(1.1, 1.45, 8, 1), goldMat);
  pavilion.rotation.x = Math.PI;
  pavilion.position.y = -0.725;
  gem.add(crown, pavilion);
  gem.scale.setScalar(1.2);
  stage.add(gem);

  // Outline diamond echoing the logo's double frame
  const edgeGeo = new THREE.EdgesGeometry(new THREE.OctahedronGeometry(1.95, 0));
  const outline = new THREE.LineSegments(
    edgeGeo,
    new THREE.LineBasicMaterial({ color: 0xf3d98b, transparent: true, opacity: 0.55 })
  );
  outline.scale.set(1, 1.1, 1);
  stage.add(outline);

  // --- Orbiting rings ---
  const rings = [];
  function makeRing(radius, tube, orbit, speed, tilt, phase, withStone) {
    const pivot = new THREE.Group();
    const holder = new THREE.Group();
    const band = new THREE.Mesh(new THREE.TorusGeometry(radius, tube, 28, 110), goldSmooth);
    holder.add(band);
    if (withStone) {
      const stone = new THREE.Mesh(new THREE.OctahedronGeometry(tube * 1.9, 0), goldMat);
      stone.position.set(0, radius + tube * 1.2, 0);
      stone.scale.y = 1.3;
      holder.add(stone);
    }
    holder.position.x = orbit;
    holder.rotation.x = Math.PI / 2.4;
    pivot.add(holder);
    pivot.rotation.z = tilt;
    pivot.userData = { speed, phase, holder };
    stage.add(pivot);
    rings.push(pivot);
  }
  makeRing(0.5, 0.08, 2.7, 0.18, 0.35, 0.0, true);
  makeRing(0.38, 0.065, 3.05, -0.14, -0.55, 2.1, false);
  makeRing(0.28, 0.05, 2.35, 0.24, 0.95, 4.0, true);

  // --- Sparkles (custom shader: soft four-point stars that twinkle) ---
  const count = isSmall ? 110 : 240;
  const pos = new Float32Array(count * 3);
  const phase = new Float32Array(count);
  const size = new Float32Array(count);
  for (let i = 0; i < count; i++) {
    const r = 2.4 + Math.random() * 4.6;
    const th = Math.random() * Math.PI * 2;
    const ph = Math.acos(2 * Math.random() - 1);
    pos[i * 3] = r * Math.sin(ph) * Math.cos(th);
    pos[i * 3 + 1] = r * Math.sin(ph) * Math.sin(th) * 0.7;
    pos[i * 3 + 2] = r * Math.cos(ph) - 1.5;
    phase[i] = Math.random() * 6.283;
    size[i] = 0.4 + Math.random() * 1.2;
  }
  const sparkGeo = new THREE.BufferGeometry();
  sparkGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  sparkGeo.setAttribute("aPhase", new THREE.BufferAttribute(phase, 1));
  sparkGeo.setAttribute("aSize", new THREE.BufferAttribute(size, 1));
  const sparkMat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { uTime: { value: 0 }, uScale: { value: renderer.getPixelRatio() * 90 } },
    vertexShader: `
      attribute float aPhase; attribute float aSize; uniform float uTime; uniform float uScale; varying float vA;
      void main() {
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        float tw = 0.5 + 0.5 * sin(uTime * 1.6 + aPhase * 3.0);
        vA = pow(tw, 3.0);
        gl_PointSize = aSize * uScale * (0.4 + vA) / -mv.z;
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      varying float vA;
      void main() {
        vec2 p = gl_PointCoord - 0.5;
        float d = length(p);
        float star = max(0.0, 1.0 - abs(p.x) * 14.0) * max(0.0, 1.0 - abs(p.y) * 2.2)
                   + max(0.0, 1.0 - abs(p.y) * 14.0) * max(0.0, 1.0 - abs(p.x) * 2.2);
        float glow = smoothstep(0.5, 0.0, d);
        float a = (glow * 0.55 + star * 0.9) * vA;
        if (a < 0.01) discard;
        gl_FragColor = vec4(1.0, 0.86, 0.5, a);
      }`,
  });
  const sparkles = new THREE.Points(sparkGeo, sparkMat);
  stage.add(sparkles);

  // --- Layout / interaction ---
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  let scrollP = 0;
  let visible = true;

  function resize() {
    const w = hero.clientWidth;
    const h = hero.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    const narrow = w < 860;
    // Wide: gem sits right of the headline. Narrow: gem sits above the text.
    const halfW = camera.position.z * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * camera.aspect;
    stage.position.set(narrow ? 0 : halfW * 0.44, narrow ? 2.25 : 0, 0);
    stage.scale.setScalar(narrow ? 0.42 : 1);
    camera.updateProjectionMatrix();
    sparkMat.uniforms.uScale.value = renderer.getPixelRatio() * (narrow ? 70 : 90);
  }
  window.addEventListener("resize", resize);
  resize();

  window.addEventListener("pointermove", (e) => {
    pointer.tx = (e.clientX / window.innerWidth) * 2 - 1;
    pointer.ty = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });
  window.addEventListener("scroll", () => {
    scrollP = Math.min(1, Math.max(0, window.scrollY / hero.clientHeight));
  }, { passive: true });
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; }).observe(hero);

  const clock = new THREE.Clock();
  function frame() {
    requestAnimationFrame(frame);
    if (!visible) return;
    const t = clock.getElapsedTime();
    const motion = reduceMotion ? 0.12 : 1;

    pointer.x += (pointer.tx - pointer.x) * 0.05;
    pointer.y += (pointer.ty - pointer.y) * 0.05;

    gem.rotation.y = t * 0.45 * motion + scrollP * 2.2;
    gem.rotation.x = Math.sin(t * 0.6 * motion) * 0.12 + pointer.y * 0.35 + 0.18;
    gem.rotation.z = Math.sin(t * 0.4 * motion) * 0.06 - pointer.x * 0.12;
    gem.position.y = Math.sin(t * 0.9 * motion) * 0.12;

    outline.rotation.y = -t * 0.18 * motion - scrollP;
    outline.rotation.x = Math.sin(t * 0.3 * motion) * 0.1;

    rings.forEach((r) => {
      const d = r.userData;
      r.rotation.y = t * d.speed * motion + d.phase + scrollP * 1.6;
      d.holder.rotation.z = t * 0.5 * motion + d.phase;
      d.holder.position.y = Math.sin(t * 0.8 * motion + d.phase) * 0.25;
    });

    sparkles.rotation.y = t * 0.03 * motion + pointer.x * 0.15;
    sparkMat.uniforms.uTime.value = t;

    stage.rotation.y = pointer.x * 0.18;
    stage.position.z = -scrollP * 2.5;
    canvas.style.opacity = String(1 - scrollP * 0.85);

    key.position.x = 4 + pointer.x * 3;
    key.position.y = 4 - pointer.y * 3;

    renderer.render(scene, camera);
  }
  frame();
  document.documentElement.classList.add("webgl-ready");
}
