// Rainbow Island: Halloween. The island at night under a big moon, jack-o'-lanterns glowing, the spooky friends in their
// own moves (a ghost that floats and glows, a bat that flaps, a spider on its thread, a wolf on a rock), the first film's
// friends trick-or-treating in the toy's hats, and candy. renderAt(t) draws the frame at time t from halloween.mjs alone.
import * as THREE from "three";
import * as S from "./halloween.mjs";
import { PICS, FONT, OUTLINE } from "./pics.js";

const Q = new URLSearchParams(location.search);
const W = +(Q.get("w") || 1920), H = +(Q.get("h") || 1080);
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.autoClear = false;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2("#2b1d4f", 0.011);
const camera = new THREE.PerspectiveCamera(40, W / H, 0.1, 400);

// ------------------------------------------------------------------ helpers
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const smooth = (u) => { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); };
const ease = (a, b, t) => smooth((t - a) / (b - a));
const backOut = (u) => { u = clamp(u, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const bump = (age, len) => (age < 0 || age > len ? 0 : Math.sin(Math.PI * age / len));
function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const NOTE_COL = ["#ec2834", "#f65c28", "#ff8c1a", "#ffb81e", "#ffda24", "#82d638", "#46c46e", "#1eb096", "#4678d2", "#9254e2", "#c454d2", "#f256b0"];
const NOTE_NAME = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const RAINBOW = ["#ec3440", "#ff8c1e", "#ffd82e", "#50c85a", "#3880f4", "#9658e2", "#ff78be"];
const SPOOKCOL = ["#ff8a1e", "#a45cff", "#7be040"];                 // the title's letters: orange, purple, slime green
const CANDYCOL = ["#ff4f7b", "#ffd23e", "#7be040", "#4fb8ff", "#b07cff", "#ff8a1e", "#ffffff"];

// ------------------------------------------------------------------ voxels to a mesh (only the faces that show)
const FACES = [
  [[1, 0, 0], [[1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 0, 1]]], [[-1, 0, 0], [[0, 0, 1], [0, 1, 1], [0, 1, 0], [0, 0, 0]]],
  [[0, 1, 0], [[0, 1, 1], [1, 1, 1], [1, 1, 0], [0, 1, 0]]], [[0, -1, 0], [[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1]]],
  [[0, 0, 1], [[1, 0, 1], [1, 1, 1], [0, 1, 1], [0, 0, 1]]], [[0, 0, -1], [[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]]],
];
function voxGeometry(vox, size, ox = 0, oy = 0, oz = 0) {
  const pos = [], nor = [], col = [], idx = [];
  for (const [k, c] of vox) {
    const [x, y, z] = k.split(",").map(Number);
    for (const [n, q] of FACES) {
      if (vox.has(`${x + n[0]},${y + n[1]},${z + n[2]}`)) continue;
      const b = pos.length / 3;
      const shade = n[1] > 0 ? 1 : n[1] < 0 ? 0.7 : n[0] !== 0 ? 0.86 : 0.94;
      for (const v of q) {
        pos.push((x + v[0]) * size + ox, (y + v[1]) * size + oy, (z + v[2]) * size + oz);
        nor.push(...n);
        col.push(c.r * shade, c.g * shade, c.b * shade);
      }
      idx.push(b, b + 1, b + 2, b, b + 2, b + 3);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("normal", new THREE.Float32BufferAttribute(nor, 3));
  g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
  g.setIndex(idx);
  return g;
}
const colorOf = (() => { const cache = {}; return (h) => cache[h] || (cache[h] = new THREE.Color(h)); })();
function plump(w, h, at, opt = {}) {
  const dist = new Array(w * h).fill(0), q = [];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (!at(x, y)) continue;
    if ([[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => !at(x + dx, y + dy))) { dist[y * w + x] = 1; q.push([x, y]); }
  }
  for (let i = 0; i < q.length; i++) {
    const [x, y] = q[i], d = dist[y * w + x];
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const xx = x + dx, yy = y + dy;
      if (xx < 0 || yy < 0 || xx >= w || yy >= h || !at(xx, yy) || dist[yy * w + xx]) continue;
      dist[yy * w + xx] = d + 1;
      q.push([xx, yy]);
    }
  }
  const max = opt.max ?? 7, k = opt.k ?? 1.9, sets = {};
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const c = at(x, y);
    if (!c) continue;
    const half = Math.min(max, Math.max(1, Math.round(Math.sqrt(dist[y * w + x]) * k)));
    const which = opt.split ? opt.split(x, y) : 0;
    const m = sets[which] || (sets[which] = new Map());
    for (let z = -half; z < half; z++) m.set(`${x},${h - 1 - y},${z}`, colorOf(c));
  }
  return sets;
}

// ------------------------------------------------------------------ materials: plain, glowing (a pumpkin's face, a ghost)
const matVox = new THREE.MeshLambertMaterial({ vertexColors: true });
const glowMat = (k, u) => {
  const m = new THREE.MeshLambertMaterial({ vertexColors: true });
  m.onBeforeCompile = (sh) => {
    sh.uniforms.uGlow = u;
    sh.fragmentShader = sh.fragmentShader.replace("#include <common>", "#include <common>\nuniform float uGlow;")
      .replace("#include <emissivemap_fragment>", `#include <emissivemap_fragment>\ntotalEmissiveRadiance += vColor.rgb * ${k.toFixed(2)} * uGlow;`);
  };
  return m;
};
const faceU = { value: 0 }, lanternU = { value: 1 }, ghostU = { value: 1 }, letterU = { value: 1 };
const matFace = glowMat(1.6, faceU), matLantern = glowMat(1.6, lanternU), matGhost = glowMat(0.35, ghostU), matLetter = glowMat(0.7, letterU);

// ------------------------------------------------------------------ the friends
const VS = 0.062;
const friends = {};
const picOf = (key) => PICS[S.CAST[key].pic || key];
function buildPic(p, glow, matBody, matGlow) {
  const w = p.w || 48, h = p.h || 48, pal = p.pal;
  const at = (x, y) => (x < 0 || y < 0 || x >= w || y >= h ? null : (p.px.charCodeAt(y * w + x) - 48 ? pal[p.px.charCodeAt(y * w + x) - 49] : null));
  const g = new Set(glow || []);
  const sets = plump(w, h, at, { split: g.size ? (x, y) => (g.has(at(x, y)) ? 1 : 0) : null });
  const grp = new THREE.Group();
  for (const [which, m] of Object.entries(sets)) {
    const mesh = new THREE.Mesh(voxGeometry(m, VS, -(w / 2) * VS, 0, 0), which === "1" ? matGlow : matBody);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    grp.add(mesh);
  }
  let y0 = h;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (at(x, y)) y0 = Math.min(y0, y);
  return { grp, height: (h - y0) * VS };
}
for (const [key, c] of Object.entries(S.CAST)) {
  const { grp, height } = buildPic(picOf(key), c.glow, key === "GHOST" ? matGhost : matVox, matFace);
  const root = new THREE.Group(), body = new THREE.Group();
  root.add(body);
  body.add(grp);
  grp.scale.setScalar(c.scale || 1);
  scene.add(root);
  friends[key] = { root, body, c, height: height * (c.scale || 1) };
}
// the spider's thread, from its branch
const thread = new THREE.Mesh(new THREE.BoxGeometry(0.035, 1, 0.035), new THREE.MeshBasicMaterial({ color: "#e8e4ff" }));
scene.add(thread);

// ------------------------------------------------------------------ the island at night
const island = new THREE.Group();
scene.add(island);
const HILL = (x, z) => 1.6 * Math.exp(-((x) ** 2 / 30 + (z + 7.6) ** 2 / 10));
{
  const R = rng(11), CELL = 0.8, RAD = 17, m = new Map();
  const n = Math.ceil(RAD / CELL);
  for (let i = -n; i <= n; i++) for (let j = -n; j <= n; j++) {
    const x = i * CELL, z = j * CELL, r = Math.hypot(x, z * 1.08);
    if (r > RAD) continue;
    const wob = Math.sin(x * 0.7) * Math.cos(z * 0.6) * 0.5 + R() * 0.25;
    let top = 0;
    if (z < -4.5) top = Math.round((HILL(x, z) + (r > 11 ? wob * 0.8 : 0)) / 0.4);
    if (r > 14) top = Math.max(top, Math.round(wob));
    const bottom = -Math.round(3 + 9 * Math.pow(1 - r / RAD, 1.4) + R() * 2);
    for (let y = bottom; y <= top; y++) {
      const grass = y === top, dirt = y >= top - 2;
      const c = grass ? ["#5fb84a", "#56ad44", "#68c254", "#4fa23f"][(i * 7 + j * 3 + y) & 3] : dirt ? ((i + j + y) & 1 ? "#9a6a3e" : "#8a5e36") : ((i + y) & 1 ? "#7d6f92" : "#6d6082");
      m.set(`${i},${y},${j}`, colorOf(c));
    }
  }
  const g = voxGeometry(m, 0.4);
  g.scale(CELL / 0.4, 1, CELL / 0.4);
  g.translate(-CELL / 2, -0.4, -CELL / 2);
  const mesh = new THREE.Mesh(g, matVox);
  mesh.receiveShadow = mesh.castShadow = true;
  island.add(mesh);
}
const groundY = (x, z) => (z < -4.5 ? Math.round(HILL(x, z) / 0.4) * 0.4 : 0);
{
  // flowers in night colours, and mushrooms
  const R = rng(5), m = new Map(), S2 = 0.18, spots = Object.values(S.CAST).map((c) => c.pos);
  let n = 0;
  while (n < 120) {
    const a = R() * Math.PI * 2, r = 2 + R() * 13.5, x = Math.cos(a) * r, z = Math.sin(a) * r * 0.92;
    if (spots.some((p) => Math.hypot(p[0] - x, p[2] - z) < 1.7) || Math.hypot(x - 9.5, z + 7) < 1.5 || Math.hypot(x + 10.2, z + 3.2) < 1.8) continue;
    n++;
    const gx = Math.round(x / S2), gz = Math.round(z / S2), gy = Math.round(groundY(x, z) / S2);
    if (R() < 0.35) {                                                  // a mushroom
      const cap = R() < 0.5 ? "#e0405a" : "#b07cff";
      for (let y = 0; y < 2; y++) m.set(`${gx},${gy + y},${gz}`, colorOf("#f4ecd8"));
      for (let dx = -1; dx <= 1; dx++) for (let dz = -1; dz <= 1; dz++) m.set(`${gx + dx},${gy + 2},${gz + dz}`, colorOf((dx + dz) & 1 ? cap : "#ffffff"));
      m.set(`${gx},${gy + 3},${gz}`, colorOf(cap));
      continue;
    }
    const hgt = 2 + Math.floor(R() * 2), col = ["#b07cff", "#ff8a1e", "#ffffff", "#7be040"][Math.floor(R() * 4)];
    for (let y = 0; y < hgt; y++) m.set(`${gx},${gy + y},${gz}`, colorOf("#3e9e48"));
    for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) m.set(`${gx + dx},${gy + hgt},${gz + dz}`, colorOf(col));
    m.set(`${gx},${gy + hgt},${gz}`, colorOf("#ffe066"));
  }
  const fl = new THREE.Mesh(voxGeometry(m, S2), matVox);
  fl.castShadow = true;
  island.add(fl);
  const bush = (x, z, r, seed) => {
    const Rb = rng(seed), bm = new Map(), s = 0.3;
    for (let i = -r; i <= r; i++) for (let j = 0; j <= r * 1.4; j++) for (let k = -r; k <= r; k++)
      if (i * i + (j - r * 0.5) ** 2 * 1.6 + k * k < r * r + Rb() * 2) bm.set(`${i},${j},${k}`, colorOf(Rb() < 0.08 ? "#b07cff" : (i + j + k) & 1 ? "#2f8e45" : "#3b9e50"));
    const b = new THREE.Mesh(voxGeometry(bm, s), matVox);
    b.position.set(x, groundY(x, z), z);
    b.castShadow = b.receiveShadow = true;
    island.add(b);
  };
  bush(-11, -6, 4, 2);
  bush(13, 3, 3, 3);
  bush(-13, 5, 3, 4);
  // the wolf's rock
  const rm = new Map(), Rr = rng(31);
  for (let i = -5; i <= 5; i++) for (let j = 0; j <= 4; j++) for (let k = -4; k <= 4; k++)
    if (i * i * 0.8 + (j * 1.6) ** 2 + k * k * 1.1 < 26 + Rr() * 5) rm.set(`${i},${j},${k}`, colorOf((i + j * 2 + k) % 3 ? "#8a86a0" : "#77728e"));
  const rock = new THREE.Mesh(voxGeometry(rm, 0.3, 0, -0.3, 0), matVox);
  rock.position.set(-10.2, 0, -3.2);
  rock.castShadow = rock.receiveShadow = true;
  island.add(rock);
  // the tree in autumn, with a branch for the owl and the spider's thread
  const tm = new Map(), s = 0.3, tx = 9.5, tz = -7;
  for (let y = 0; y < 26; y++) for (let i = -1; i <= 1; i++) for (let k = -1; k <= 1; k++) if (Math.abs(i) + Math.abs(k) < 2 || y < 2) tm.set(`${i},${y},${k}`, colorOf((y + i) & 1 ? "#6e4a2e" : "#5e3e26"));
  for (let u = 0; u <= 8; u++) { const bx = Math.round(-u * 0.8), bz = Math.round(u * 0.36); tm.set(`${bx},16,${bz}`, colorOf("#6e4a2e")); tm.set(`${bx},15,${bz}`, colorOf("#5e3e26")); }
  const Rt = rng(9);
  for (let i = -9; i <= 9; i++) for (let j = 24; j <= 40; j++) for (let k = -9; k <= 9; k++) {
    const d = i * i + ((j - 32) * 1.15) ** 2 + k * k;
    if (d < 70 + Rt() * 14 && Rt() > 0.12) tm.set(`${i},${j},${k}`, colorOf(["#ff8a1e", "#e85a24", "#ffc23a", "#c9462a"][Math.floor(Rt() * 4)]));
  }
  const tree = new THREE.Mesh(voxGeometry(tm, s), matVox);
  tree.position.set(tx, groundY(tx, tz), tz);
  tree.castShadow = tree.receiveShadow = true;
  island.add(tree);
}
// jack-o'-lanterns round the island: the Pumpkin's own picture, small, their faces lit
const lanterns = [];
{
  const R = rng(17), p = PICS.PUMPKIN;
  const spots = [[-12.5, 2], [-9, 8.5], [-3, 11], [4, 10.5], [10.5, 7], [14, -1], [12, -9], [-6, -10.5], [-14, -2], [6, -11.5], [-1, 13.5], [15.5, 4]];
  for (const [x, z] of spots) {
    const { grp } = buildPic(p, ["#ffd82e"], matVox, matLantern);
    grp.scale.setScalar(0.42 + R() * 0.2);
    grp.position.set(x, groundY(x, z), z);
    grp.rotation.y = Math.atan2(-x, 14 - z) * 0.8;
    scene.add(grp);
    lanterns.push(grp);
  }
}

// ------------------------------------------------------------------ the rainbow arch, dim at night, bright at the party
const bands = [];
for (let b = 0; b < 7; b++) {
  const m = new Map(), r0 = 23 - b;
  for (let x = -24; x <= 24; x++) for (let y = 0; y <= 24; y++) {
    const r = Math.hypot(x, y);
    if (r >= r0 - 1 && r < r0) for (let z = 0; z < 2; z++) m.set(`${x},${y},${z}`, colorOf(RAINBOW[b]));
  }
  const mat = new THREE.MeshLambertMaterial({ vertexColors: true, emissive: new THREE.Color(RAINBOW[b]), emissiveIntensity: 0.2 });
  scene.add(new THREE.Mesh(voxGeometry(m, 1, -0.5, -3, -19), mat));
  bands.push(mat);
}

// ------------------------------------------------------------------ the Halloween sky: a big moon, stars, bats against it
const sky = new THREE.Mesh(new THREE.SphereGeometry(300, 32, 16), new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false, fog: false,
  vertexShader: "varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
  fragmentShader: `varying vec3 vP;
    void main(){
      float h = clamp(vP.y * 1.5 + 0.12, 0.0, 1.0);
      vec3 hor = vec3(0.98, 0.6, 0.36), mid = vec3(0.46, 0.25, 0.64), top = vec3(0.08, 0.05, 0.22);
      vec3 c = h < 0.25 ? mix(hor, mid, h / 0.25) : mix(mid, top, (h - 0.25) / 0.75);
      gl_FragColor = vec4(pow(c, vec3(2.2)), 1.0);
    }`,
}));
scene.add(sky);
const moon = new THREE.Mesh(new THREE.SphereGeometry(13, 24, 16), new THREE.MeshBasicMaterial({ color: "#fff0c4", fog: false }));
moon.position.set(26, 36, -150);
scene.add(moon);
{
  const cv = document.createElement("canvas");
  cv.width = cv.height = 256;
  const c = cv.getContext("2d"), gr = c.createRadialGradient(128, 128, 30, 128, 128, 128);
  gr.addColorStop(0, "rgba(255,236,190,0.55)"); gr.addColorStop(1, "rgba(255,200,140,0)");
  c.fillStyle = gr; c.fillRect(0, 0, 256, 256);
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cv), transparent: true, depthWrite: false, fog: false, blending: THREE.AdditiveBlending }));
  halo.position.copy(moon.position).add(new THREE.Vector3(0, 0, 2));
  halo.scale.setScalar(62);
  scene.add(halo);
}
{
  const R = rng(3), p = [];
  for (let i = 0; i < 800; i++) {
    const a = R() * Math.PI * 2, e = 0.12 + R() * 1.3, r = 250;
    p.push(Math.cos(a) * Math.cos(e) * r, Math.sin(e) * r, Math.sin(a) * Math.cos(e) * r);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3));
  scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: "#ffffff", size: 2.4, sizeAttenuation: false, fog: false })));
}
// little dark bats that cross the moon now and then
const flock = [];
{
  const { grp } = buildPic(PICS.BAT, null, new THREE.MeshBasicMaterial({ color: "#1c1030", fog: false }), null);
  for (let i = 0; i < 9; i++) {
    const b = grp.clone();
    scene.add(b);
    flock.push(b);
  }
}

// ------------------------------------------------------------------ lights: the moon, a purple sky, the big pumpkin's glow
const hemi = new THREE.HemisphereLight("#c6b2ff", "#2a1f44", 1.15);
scene.add(hemi);
const moonL = new THREE.DirectionalLight("#dfe4ff", 1.7);
moonL.position.set(12, 30, 20);
moonL.castShadow = true;
moonL.shadow.mapSize.set(2048, 2048);
Object.assign(moonL.shadow.camera, { left: -24, right: 24, top: 24, bottom: -24, near: 1, far: 120 });
moonL.shadow.bias = -0.0006;
moonL.shadow.normalBias = 0.02;
scene.add(moonL, moonL.target);
const pumpL = new THREE.PointLight("#ff9a3a", 0, 22, 1.4);
pumpL.position.set(0, 3.4, -5.4);
scene.add(pumpL);
const fillL = new THREE.AmbientLight("#ffffff", 0.32);
scene.add(fillL);

// ------------------------------------------------------------------ pixel-font voxel text
function textPixels(text) {
  const w = text.length * 6 + 1, h = 9, px = new Array(w * h).fill(0);
  [...text].forEach((ch, i) => {
    const g = FONT[ch];
    if (!g) return;
    for (let y = 0; y < 7; y++) for (let x = 0; x < 5; x++) if ((g[y] >> (4 - x)) & 1) px[(y + 1) * w + i * 6 + x + 1] = 1;
  });
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (px[y * w + x]) continue;
    for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++)
      if (y + dy >= 0 && y + dy < h && x + dx >= 0 && x + dx < w && px[(y + dy) * w + x + dx] === 1) px[y * w + x] = 2;
  }
  return { w, h, px };
}
function voxLetter(ch, color, s, mat) {
  const { w, h, px } = textPixels(ch);
  const sets = plump(w, h, (x, y) => (x < 0 || y < 0 || x >= w || y >= h ? null : px[y * w + x] === 1 ? color : px[y * w + x] === 2 ? OUTLINE : null), { max: 2, k: 1.4 });
  const m = new THREE.Mesh(voxGeometry(sets[0], s, -w * s / 2, 0, 0), mat || matVox);
  m.castShadow = true;
  return m;
}
const letters = (text) => [...text].map((ch, i) => {
  if (ch === " ") return null;
  const m = voxLetter(ch, SPOOKCOL[i % 3], 0.36, matLetter);
  scene.add(m);
  return m;
});
const title = letters(S.TITLE.text), happy = letters(S.HAPPY.text);

// ------------------------------------------------------------------ the notes they sing
const NOTES = [];
for (const l of S.LINES) if (l.tag !== "bed") for (const [d, n, len] of l.notes) NOTES.push({ t: l.t + d, len, who: l.who, m: S.midi(n), n, line: l });
NOTES.sort((a, b) => a.t - b.t);
const lineEnd = (l) => l.t + Math.max(...l.notes.map(([d, , len]) => d + len));
const NOTE_GLYPH = ["...11", "...111", "...1.1", "...1..", "...1..", ".111..", "1111..", ".11..."];
const noteGeo = {};
const noteMesh = (pc) => {
  if (!noteGeo[pc]) {
    const w = 6, h = 8;
    const sets = plump(w + 2, h + 2, (x, y) => {
      const g = (xx, yy) => xx >= 0 && yy >= 0 && xx < w && yy < h && NOTE_GLYPH[yy][xx] === "1";
      if (g(x - 1, y - 1)) return NOTE_COL[pc];
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) if (g(x - 1 + dx, y - 1 + dy)) return OUTLINE;
      return null;
    }, { max: 1 });
    noteGeo[pc] = voxGeometry(sets[0], 0.09, -0.36, 0, 0);
  }
  return noteGeo[pc];
};
const notePool = [];
for (let i = 0; i < 48; i++) {
  const m = new THREE.Mesh(noteMesh(0), new THREE.MeshLambertMaterial({ vertexColors: true, transparent: true, emissive: "#ffffff", emissiveIntensity: 0.25 }));
  m.visible = false;
  scene.add(m);
  notePool.push(m);
}

// ------------------------------------------------------------------ candy: wrapped sweets, a colour each
const CANDY_N = 480;
const candyGeo = (() => {
  const m = new Map();
  for (let x = 0; x < 4; x++) for (let y = 0; y < 2; y++) for (let z = 0; z < 2; z++) m.set(`${x},${y},${z}`, colorOf("#ffffff"));
  for (const x of [-1, 4]) for (const y of [-1, 0, 1, 2]) m.set(`${x},${y},0`, colorOf("#ffffff")), m.set(`${x},${y},1`, colorOf("#ffffff"));
  return voxGeometry(m, 0.07, -0.14, -0.07, -0.07);
})();
const candy = new THREE.InstancedMesh(candyGeo, new THREE.MeshLambertMaterial({ emissive: "#ffffff", emissiveIntensity: 0.12 }), CANDY_N);
candy.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
for (let i = 0; i < CANDY_N; i++) candy.setColorAt(i, colorOf(CANDYCOL[i % CANDYCOL.length]));
scene.add(candy);
const BURSTS = [
  { t: S.CANDY, at: [0, 3.6, -6.6], n: 180, seed: 1, fwd: 5 },
  { t: S.BIGEND, at: [0, 3, 0], n: 150, seed: 2, fwd: 0 },
  { t: S.FINALE, at: [0, 3, 0], n: 150, seed: 3, fwd: 0 },
];
// green bubbles from the scientist's flask, sparks round the ghost
const bubbleFx = (() => {
  const g = new THREE.BufferGeometry(), n = 90;
  g.setAttribute("position", new THREE.Float32BufferAttribute(new Float32Array(n * 3), 3));
  const m = new THREE.PointsMaterial({ color: "#9cff6a", size: 8, sizeAttenuation: false, transparent: true, opacity: 0.9, depthWrite: false, blending: THREE.AdditiveBlending });
  const p = new THREE.Points(g, m);
  scene.add(p);
  return { g, m, n };
})();

// ------------------------------------------------------------------ speech bubbles: the notes, coloured, with their letters
const BUB_W = 600, BUB_H = 320;
function drawLetters(ctx, text, x, y, s, fill) {
  for (const pass of [0, 1]) {
    [...text].forEach((ch, i) => {
      const g = FONT[ch];
      if (!g) return;
      for (let yy = 0; yy < 7; yy++) for (let xx = 0; xx < 5; xx++) if ((g[yy] >> (4 - xx)) & 1) {
        const px = Math.round(x) + (i * 6 + xx) * s, py = Math.round(y) + yy * s;
        if (pass === 0) { ctx.fillStyle = OUTLINE; ctx.fillRect(px - s * 0.45, py - s * 0.45, s * 1.9, s * 1.9); }
        else { ctx.fillStyle = fill; ctx.fillRect(px - 0.25, py - 0.25, s + 0.5, s + 0.5); }
      }
    });
  }
}
const bubbles = [];
for (let i = 0; i < 6; i++) {
  const cv = document.createElement("canvas");
  cv.width = BUB_W; cv.height = BUB_H;
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.minFilter = THREE.LinearFilter;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false, fog: false }));
  sp.renderOrder = 10;
  sp.visible = false;
  scene.add(sp);
  bubbles.push({ cv, ctx: cv.getContext("2d"), tex, sp });
}
function drawBubble(b, line, t) {
  const ctx = b.ctx, sung = line.notes.filter(([d]) => line.t + d <= t + 0.02);
  ctx.clearRect(0, 0, BUB_W, BUB_H);
  const slots = Math.min(6, line.notes.length), slot = 86;
  const bw = slots * slot + 64, x0 = (BUB_W - bw) / 2, x1 = x0 + bw, y0 = 10, y1 = BUB_H - 62, r = 50, tx = BUB_W / 2 - 20;
  ctx.beginPath();
  ctx.moveTo(x0 + r, y0); ctx.arcTo(x1, y0, x1, y1, r); ctx.arcTo(x1, y1, x0, y1, r);
  ctx.lineTo(tx + 34, y1); ctx.lineTo(tx - 10, BUB_H - 8); ctx.lineTo(tx - 4, y1);
  ctx.arcTo(x0, y1, x0, y0, r); ctx.arcTo(x0, y0, x1, y0, r); ctx.closePath();
  ctx.fillStyle = "#ffffff"; ctx.fill();
  ctx.lineWidth = 10; ctx.strokeStyle = OUTLINE; ctx.stroke();
  const show = sung.slice(-6);
  const all = line.notes.map(([, nn]) => S.midi(nn)), lo = Math.min(...all), hi = Math.max(...all);
  const left = x0 + 32 + slot / 2 - 8;
  show.forEach(([d, nn, len], i) => {
    const m = S.midi(nn), pc = m % 12, age = t - (line.t + d), pop = 1 + 0.5 * Math.exp(-age * 10);
    const cx = left + i * slot, cy = 146 - (hi > lo ? ((m - lo) / (hi - lo)) * 62 : 31);
    ctx.save();
    ctx.translate(cx, cy); ctx.scale(pop, pop); ctx.rotate(-0.35);
    ctx.beginPath(); ctx.ellipse(0, 0, 23, 16, 0, 0, Math.PI * 2);
    ctx.fillStyle = NOTE_COL[pc]; ctx.fill(); ctx.lineWidth = 5; ctx.strokeStyle = OUTLINE; ctx.stroke();
    ctx.restore();
    ctx.fillStyle = OUTLINE;
    ctx.fillRect(cx + 17 * pop, cy - 62 * pop, 6, 60 * pop);
    if (len < 0.3) { ctx.beginPath(); ctx.moveTo(cx + 23 * pop, cy - 62 * pop); ctx.quadraticCurveTo(cx + 46 * pop, cy - 42 * pop, cx + 40 * pop, cy - 22 * pop); ctx.lineWidth = 6; ctx.stroke(); }
    const name = NOTE_NAME[pc], ls = name.length > 1 ? 6 : 8;
    drawLetters(ctx, name, cx - ((name.length * 6 - 1) * ls) / 2, 196, ls, NOTE_COL[pc]);
  });
  b.tex.needsUpdate = true;
}

// ------------------------------------------------------------------ the toy's band
const hud = new THREE.Scene(), hudCam = new THREE.OrthographicCamera(0, W, H, 0, -1, 1);
const fadeMat = new THREE.MeshBasicMaterial({ color: "#000000", transparent: true, opacity: 0 });
const fader = new THREE.Mesh(new THREE.PlaneGeometry(W, H), fadeMat);
fader.position.set(W / 2, H / 2, 0.5);
fader.renderOrder = 20;
hud.add(fader);
const bandCv = document.createElement("canvas");
bandCv.width = W; bandCv.height = Math.round(H * 0.13);
const bandTex = new THREE.CanvasTexture(bandCv);
bandTex.colorSpace = THREE.SRGBColorSpace;
const band = new THREE.Mesh(new THREE.PlaneGeometry(W, bandCv.height), new THREE.MeshBasicMaterial({ map: bandTex, transparent: true }));
hud.add(band);
const NIGHTC = ["#286e46", "#185032"], PURPLE = ["#966ee6", "#7854c8"], ORANGE = ["#f0782a", "#c0561a"], YESC = ["#38aa50", "#257a38"];
const BANDS = [
  ...Object.entries(S.ENTER).filter(([k, e]) => e.kind !== "there" && !S.GUESTS.includes(k)).map(([k, e]) => ({ t: e.t + 0.2, len: 2.2, text: S.CAST[k].name, col: NIGHTC })),
  { t: 32.6, len: 1.6, text: "OWL", col: NIGHTC },
  { t: S.KNOCK - 0.2, len: 1.9, text: "TRICK OR TREAT!", col: PURPLE },
  { t: S.BOO, len: 1.0, text: "BOO!", col: ORANGE },
  { t: S.CANDY, len: 1.8, text: "CANDY!", col: YESC },
  { t: S.PARTY.t0 - 0.2, len: 2.2, text: "SPOOKY", col: PURPLE },
].sort((a, b) => a.t - b.t);
let bandDrawn = "";
function drawBand(t) {
  const cur = BANDS.filter((b) => t >= b.t && t < b.t + b.len).pop();
  if (!cur) { band.visible = false; return; }
  const age = t - cur.t, rest = cur.t + cur.len - t, h = bandCv.height;
  const slide = Math.min(backOut(age / 0.35), smooth(rest / 0.3));
  band.visible = true;
  band.position.set(W / 2, h / 2 - h * (1 - slide), 0);
  const key = cur.text + cur.col[0];
  if (bandDrawn !== key) {
    const ctx = bandCv.getContext("2d");
    ctx.fillStyle = cur.col[0]; ctx.fillRect(0, 0, W, h);
    ctx.fillStyle = cur.col[1]; ctx.fillRect(0, h - h * 0.16, W, h * 0.16);
    ctx.fillStyle = OUTLINE; ctx.fillRect(0, 0, W, Math.max(4, h * 0.04));
    const s = Math.floor(h * 0.1), tw = (cur.text.length * 6 - 1) * s;
    drawLetters(ctx, cur.text, (W - tw) / 2, (h * 0.84 - 7 * s) / 2 + h * 0.03, s, "#ffffff");
    bandTex.needsUpdate = true;
    bandDrawn = key;
  }
}

// ------------------------------------------------------------------ where each friend is, and how it moves
function singingLines(t) { return S.LINES.filter((l) => l.tag !== "bed" && t >= l.t - 0.15 && t <= lineEnd(l) + 0.15); }
function noteKick(who, t) {
  let k = 0;
  for (const e of NOTES) {
    if (e.t > t) break;
    if (e.who === who) k = Math.max(k, bump(t - e.t, 0.26));
  }
  return k;
}
function friendPose(key, t) {
  const f = friends[key], c = f.c, e = S.ENTER[key];
  const pos = new THREE.Vector3(...c.pos);
  let rotY = 0, rotZ = 0, sx = 1, sy = 1, mid = false;
  const age = t - e.t;
  if (age < 0) return { vis: false };
  const from = new THREE.Vector3(...(e.from || c.pos));
  const ph = (key.charCodeAt(0) * 0.37 + key.length) % 6;
  switch (e.kind) {
    case "rise": { const u = clamp(age / 1.4, 0, 1); pos.y = lerp(from.y, c.pos[1], backOut(u)); break; }
    case "fly": {
      const u = clamp(age / 1.8, 0, 1);
      pos.lerpVectors(from, pos, smooth(u));
      pos.y += Math.sin(u * Math.PI) * 2;
      break;
    }
    case "drop": { const u = clamp(age / 1.0, 0, 1); pos.y = lerp(from.y, c.pos[1], backOut(u)); break; }
    case "leap": {
      const u = clamp(age / 1.1, 0, 1);
      pos.lerpVectors(from, pos, smooth(u));
      pos.y += Math.sin(u * Math.PI) * 3.2;
      break;
    }
    case "walk": case "hop": case "run": {
      const len = e.kind === "hop" ? 2.0 : e.kind === "run" ? 1.6 : 2.2, u = clamp(age / len, 0, 1);
      pos.lerpVectors(from, pos, smooth(u));
      const steps = e.kind === "hop" ? 4 : e.kind === "run" ? 8 : 6, p2 = u * steps;
      if (u < 1) {
        pos.y += Math.abs(Math.sin(p2 * Math.PI)) * (e.kind === "hop" ? 0.9 : e.kind === "run" ? 0.3 : 0.14);
        rotZ = e.kind === "walk" ? Math.sin(p2 * Math.PI) * 0.1 : 0;
        rotY = (from.x > c.pos[0] ? 1 : -1) * 0.35 * (1 - smooth((u - 0.8) / 0.2));
      }
      break;
    }
    case "loop": {                                     // Slimy: a loop-de-loop in the air, then a splat
      const u = clamp(age / 1.5, 0, 1);
      if (u < 1) {
        pos.lerpVectors(from, pos, smooth(u));
        const a = u * Math.PI * 2;
        pos.x += Math.sin(a) * 2.2; pos.y += (1 - Math.cos(a)) * 1.6;
        rotZ = -a; mid = true;
      }
      const k = bump(age - 1.5, 0.35); sy *= 1 - 0.35 * k; sx *= 1 + 0.3 * k;
      break;
    }
    case "peek": { const u = clamp(age / 0.55, 0, 1); pos.y = lerp(from.y, 0, backOut(u)); break; }
    case "pop": {
      const u = clamp(age / 0.8, 0, 1);
      pos.y = lerp(from.y, 0, u) + Math.sin(u * Math.PI) * 1.8;
      break;
    }
  }
  const land = { walk: 2.2, hop: 2.0, run: 1.6, leap: 1.1, pop: 0.8, peek: 0.55 }[e.kind];
  if (land) { const k = bump(age - land, 0.3); sy *= 1 - 0.18 * k; sx *= 1 + 0.12 * k; }
  sy *= 1 + Math.sin(t * 2.2 + ph) * 0.018;
  // floaters bob; the bat flaps and hovers; the spider bobs on its thread
  if (c.float) pos.y += Math.sin(t * 1.6 + ph) * 0.22;
  if (c.fly) { pos.y += Math.sin(t * 2.4) * 0.25; sx *= 1 + Math.sin(t * 22) * 0.12; }
  if (c.hang && age > 1.0) pos.y += Math.sin(t * 1.3) * 0.12;
  // singing: a hop and a stretch on each note (the floaters and the spider: a little bob instead)
  const kick = noteKick(key, t);
  pos.y += kick * (c.hang ? 0.1 : 0.3);
  sy *= 1 + kick * 0.1; sx *= 1 - kick * 0.05;
  // the flytrap chomps: a squash on each note, and now and then by itself
  if (key === "FLYTRAP") { const k = Math.max(kick, bump(((t + 1.1) % 3.4) - 3.0, 0.25)); sy *= 1 - 0.22 * k; sx *= 1 + 0.1 * k; }
  // the wolf lifts its head to howl
  if (key === "WOLF") for (const l of S.LINES) if (l.who === "WOLF" && l.tag === "howl" || l.who === "WOLF" && l.tag === "end") {
    const k = ease(l.t, l.t + 0.4, t) * (1 - ease(lineEnd(l), lineEnd(l) + 0.4, t));
    rotZ -= 0.32 * k; pos.y += 0.25 * k;
  }
  // the others turn a little toward whoever is singing
  const sing = singingLines(t), singers = sing.filter((l) => l.who !== key);
  if (singers.length && !sing.some((l) => l.who === key) && age > 2.5 && !c.hang) {
    const sp = S.CAST[singers[singers.length - 1].who].pos;
    rotY += clamp(Math.atan2(sp[0] - pos.x, 6) * 0.6, -0.5, 0.5);
  }
  // trick or treat: the guests bounce at the door; BOO!: the spooky friends lunge and grow, the guests leap and shake
  if (S.GUESTS.includes(key)) {
    const jump = bump(t - S.BOO - 0.25, 0.75);
    pos.y += jump * 2.4;
    pos.x += ease(S.BOO + 0.25, S.BOO + 0.8, t) * (1 - ease(S.BOO + 1.6, S.BOO + 2.6, t)) * 0.8;
    const shake = ease(S.BOO + 0.3, S.BOO + 0.45, t) * (1 - ease(S.EEK + 0.9, S.EEK + 1.3, t));
    rotZ += Math.sin(t * 40 + ph) * 0.12 * shake;
    sy *= 1 + jump * 0.2; sx *= 1 - jump * 0.1;
    pos.y += (bump(t - S.CANDY - 0.4, 0.45) + bump(t - S.CANDY - 1.0, 0.45)) * 0.7;
  } else if (key !== "OWL") {
    const lunge = ease(S.BOO - 0.15, S.BOO + 0.05, t) * (1 - ease(S.BOO + 1.0, S.BOO + 1.6, t));
    sx *= 1 + 0.18 * lunge; sy *= 1 + 0.18 * lunge;
    pos.x += lunge * 0.6;
  }
  // the party: a bounce on every beat
  if (t >= S.PARTY.t0 && t < S.PARTY.t1 + 0.4) {
    const b = (t - S.PARTY.t0) / S.SPB, fb = b - Math.floor(b);
    const amp = c.hang ? 0.1 : key === "OWL" ? 0.12 : key === "PUMPKIN" ? 0.18 : 0.28;
    const intro = ease(S.PARTY.t0, S.PARTY.t0 + 0.4, t) * (1 - ease(S.PARTY.t1, S.PARTY.t1 + 0.4, t));
    pos.y += Math.pow(Math.sin(fb * Math.PI), 1.5) * amp * intro;
    rotZ += Math.sin(b * Math.PI / 2 + ph) * (key === "SKELETON" ? 0.22 : 0.12) * intro;
    rotY += Math.sin(b * Math.PI / 4 + ph) * 0.25 * intro;
    const k = Math.exp(-fb * 10) * intro;
    sy *= 1 - 0.07 * k; sx *= 1 + 0.05 * k;
  }
  // the big jumps: the party's last chord, and the last letter of HAPPY HALLOWEEN
  if (key !== "OWL" && !c.hang) pos.y += (bump(t - S.BIGEND, 0.6) + bump(t - S.FINALE, 0.6)) * 1.3;
  // waving goodbye
  if (t > 79 && t < 83.4) rotZ += Math.sin(t * 6 + ph) * 0.1 * ease(79, 79.5, t) * (1 - ease(82.8, 83.4, t));
  return { vis: true, pos, rotY, rotZ, sx, sy, mid };
}

// ------------------------------------------------------------------ the camera
function camAt(t) {
  const K = S.CAM, P0 = S.PARTY.t0, P1 = S.PARTY.t1 + 0.8;
  if (t > P0 && t < P1) {
    const u = smooth((t - P0) / (P1 - P0)), a = u * Math.PI * 2;
    const r = 18 + 2 * u + Math.sin(u * Math.PI) * 1.5, y = 6.5 + u + Math.sin(u * Math.PI * 2) * 1.2;
    return { p: new THREE.Vector3(Math.sin(a) * r, y, Math.cos(a) * r), l: new THREE.Vector3(0, 1.6 + 0.2 * u, 0) };
  }
  let i = 0;
  while (i < K.length - 2 && t >= K[i + 1][0]) i++;
  const u = smooth((t - K[i][0]) / (K[i + 1][0] - K[i][0])), a = K[i], b = K[i + 1];
  return {
    p: new THREE.Vector3(lerp(a[1][0], b[1][0], u), lerp(a[1][1], b[1][1], u), lerp(a[1][2], b[1][2], u)),
    l: new THREE.Vector3(lerp(a[2][0], b[2][0], u), lerp(a[2][1], b[2][1], u), lerp(a[2][2], b[2][2], u)),
  };
}

// ------------------------------------------------------------------ one frame
const tmpM = new THREE.Matrix4(), tmpQ = new THREE.Quaternion(), tmpE = new THREE.Euler(), tmpV = new THREE.Vector3(), tmpS = new THREE.Vector3();
window.renderAt = (t) => {
  const c = camAt(t);
  camera.position.copy(c.p);
  camera.lookAt(c.l);
  camera.updateMatrixWorld();
  // the pumpkin's face lights at its turn and flickers; the lanterns flicker too
  faceU.value = ease(S.ENTER.PUMPKIN.t, S.ENTER.PUMPKIN.t + 0.6, t) * (0.85 + 0.15 * Math.sin(t * 13) * Math.sin(t * 7.3));
  lanternU.value = 0.8 + 0.2 * Math.sin(t * 11.1) * Math.sin(t * 5.7);
  ghostU.value = 0.8 + 0.2 * Math.sin(t * 2);
  pumpL.intensity = 55 * faceU.value;
  const boo = bump(t - S.BOO, 0.5);                          // BOO!: the moonlight flickers
  moonL.intensity = 1.7 - 1.1 * boo * (Math.sin(t * 60) > 0 ? 1 : 0.3);
  // the rainbow: a band lights on each beat of the party
  const pb = (t - S.PARTY.t0) / S.SPB;
  bands.forEach((m, i) => {
    let e = 0.22;
    if (pb >= 0 && t < S.PARTY.t1) e += 0.9 * Math.exp(-((pb - Math.floor(pb)) * 6)) * (Math.floor(pb) % 7 === i ? 1 : 0.15);
    e += 1.2 * (bump(t - S.BIGEND, 1.5) + bump(t - S.FINALE, 1.5));
    m.emissiveIntensity = e;
  });
  // bats across the moon now and then
  flock.forEach((b, i) => {
    const period = 17, ph = ((t + i * 0.45 + (i % 3) * 0.3) % period) / 6;
    b.visible = ph < 1;
    if (!b.visible) return;
    b.position.set(lerp(-60, 90, ph) + (i % 3) * 4, 30 + Math.sin(ph * 9 + i) * 3 + (i % 4) * 3, -120 + (i % 2) * 6);
    b.scale.set(1.4 * (1 + Math.sin(t * 25 + i) * 0.3), 1.4, 1.4);
  });
  // the titles: HALLOWEEN at the start, HAPPY HALLOWEEN at the end
  title.forEach((m, i) => {
    if (!m) return;
    const age = t - S.TITLE.t0 - i * S.TITLE.step, n = title.length, x = (i - (n - 1) / 2) * 2.35;
    const away = smooth((t - S.TITLE.out - i * 0.04) / 1.3);
    m.visible = age > 0 && away < 1;
    if (!m.visible) return;
    m.position.set(x, 12.2 - Math.pow((i - (n - 1) / 2) / ((n - 1) / 2), 2) * 1.4 + Math.sin(t * 2 + i) * 0.15 + away * 14, -3 - away * 4);
    m.rotation.set(0, Math.sin(t * 1.3 + i * 0.6) * 0.18, Math.sin(t * 2 + i) * 0.06);
    m.scale.setScalar(backOut(age / 0.45) * (1 + bump(age, 0.3) * 0.3));
  });
  happy.forEach((m, i) => {
    if (!m) return;
    const age = t - S.HAPPY.t0 - i * S.HAPPY.step, row = i < 5 ? 0 : 1, j = row ? i - 6 : i, n = row ? 9 : 5;
    m.visible = age > 0;
    if (!m.visible) return;
    m.position.set((j - (n - 1) / 2) * 2.35, (row ? 10.4 : 13.6) + Math.sin(t * 1.5 + i) * 0.15, -3);
    m.rotation.set(0, Math.sin(t + i) * 0.15, Math.sin(t * 2 + i) * 0.05);
    m.scale.setScalar(backOut(age / 0.5) * (1 + bump(age, 0.3) * 0.3));
  });
  // the friends
  for (const key of Object.keys(friends)) {
    const f = friends[key], p = friendPose(key, t);
    f.root.visible = p.vis;
    if (!p.vis) continue;
    f.root.position.copy(p.pos);
    f.root.rotation.set(0, p.rotY, 0);
    f.body.rotation.set(0, 0, p.rotZ);
    f.body.scale.set(p.sx, p.sy, (p.sx + p.sy) / 2);
    const hcy = p.mid ? f.height / 2 : 0;
    f.body.position.set(Math.sin(p.rotZ) * hcy, hcy - Math.cos(p.rotZ) * hcy, 0);
  }
  // the spider's thread, from the branch down to its back
  {
    const sp = friends.SPIDER;
    thread.visible = sp.root.visible;
    if (thread.visible) {
      const top = S.CAST.SPIDER.hang, bot = sp.root.position.y + sp.height * 0.75;
      thread.position.set(sp.root.position.x, (top + bot) / 2, sp.root.position.z);
      thread.scale.set(1, Math.max(0.01, top - bot), 1);
    }
  }
  // the notes floating up from whoever sings them
  let pi = 0;
  for (const e of NOTES) {
    if (e.t > t) break;
    const age = t - e.t;
    if (age > 2.0 || pi >= notePool.length) continue;
    const m = notePool[pi++], f = friends[e.who], p = f.root.position;
    m.geometry = noteMesh(e.m % 12);
    const R = rng(Math.round(e.t * 1000)), side = (R() - 0.5) * 1.6;
    m.visible = true;
    m.position.set(p.x + side + Math.sin(age * 3 + side) * 0.3, p.y + f.height * 0.9 + age * 1.5, p.z + 0.4);
    m.rotation.set(0, Math.sin(age * 2) * 0.6, Math.sin(age * 4) * 0.2);
    m.scale.setScalar(backOut(age / 0.25) * 1.1);
    m.material.opacity = 1 - smooth((age - 1.3) / 0.7);
  }
  for (; pi < notePool.length; pi++) notePool[pi].visible = false;
  // candy
  let ci = 0;
  for (const bst of BURSTS) {
    const age = t - bst.t;
    if (age < 0 || age > 4.5) continue;
    const R = rng(bst.seed);
    for (let i = 0; i < bst.n && ci < CANDY_N; i++, ci++) {
      const a = R() * Math.PI * 2, up = 6 + R() * 7, out = 2 + R() * 7, spin = 2 + R() * 8;
      const drag = (1 - Math.exp(-age * 1.2)) / 1.2, fall = Math.max(0, age - 0.3);
      let y = bst.at[1] + up * drag - 4.5 * fall * fall * 0.5;
      const x = bst.at[0] + Math.cos(a) * out * drag, z = bst.at[2] + Math.sin(a) * out * drag * 0.8 + bst.fwd * drag;
      const gy = Math.abs(x) < 16 && Math.abs(z) < 16 ? groundY(x, z) + 0.08 : -30;
      if (y < gy) y = gy;                               // (it lands on the grass and stays)
      tmpV.set(x, y, z);
      tmpE.set(y > gy ? spin * age : 0, spin * age * 0.7, y > gy ? age * 3 + i : 0);
      tmpQ.setFromEuler(tmpE);
      tmpS.setScalar(age > 3.8 ? 1 - (age - 3.8) / 0.7 : 1);
      tmpM.compose(tmpV, tmpQ, tmpS);
      candy.setMatrixAt(ci, tmpM);
    }
  }
  candy.count = ci;
  candy.instanceMatrix.needsUpdate = true;
  // the scientist's bubbles
  {
    const pos = bubbleFx.g.attributes.position, R = rng(8), sc = friends.SCIENTIST.root;
    const on = sc.visible ? 1 : 0;
    for (let i = 0; i < bubbleFx.n; i++) {
      const sp = 0.5 + R(), off = R() * 3, age = ((t * sp + off) % 2.2);
      pos.setXYZ(i, sc.position.x + 0.95 + Math.sin(age * 4 + i) * 0.15, sc.position.y + 0.9 + age * 0.9, sc.position.z + 0.5);
    }
    pos.needsUpdate = true;
    bubbleFx.m.opacity = 0.85 * on;
  }
  // speech bubbles
  const active = S.LINES.filter((l) => l.bubble && t >= l.t - 0.1 && t < lineEnd(l) + 1.0);
  bubbles.forEach((b, i) => {
    const l = active[i];
    b.sp.visible = !!l;
    if (!l) return;
    const f = friends[l.who], p = f.root.position, n = active.length;
    const age = t - (l.t - 0.1), out = lineEnd(l) + 1.0 - t;
    const far = clamp(camera.position.distanceTo(p) / 13, 1, 2.1);
    const s = Math.min(backOut(age / 0.3), smooth(out / 0.25)) * (n > 2 ? 0.8 : 1) * far;
    drawBubble(b, l, t);
    b.sp.position.set(p.x + 0.6, p.y + f.height + 1.25 * s + 0.35 + (n > 2 ? (i % 2) * 0.9 * far : 0), p.z + 0.5);
    b.sp.scale.set(3.9 * s, 3.9 * s * (BUB_H / BUB_W), 1);
  });
  renderer.clear();
  renderer.render(scene, camera);
  drawBand(t);
  fadeMat.opacity = Math.max(1 - smooth(t / 0.8), smooth((t - (S.DUR - 1.6)) / 1.4));
  fader.visible = fadeMat.opacity > 0.001;
  renderer.clearDepth();
  renderer.render(hud, hudCam);
};
window.ready = true;
