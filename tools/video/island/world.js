// Rainbow Island: Rainbow mode's friends as plump voxel figures (each pixel of their 48 x 48 art a little cube, thicker
// toward the middle), on a floating island under a voxel rainbow. renderAt(t) draws the frame at time t, from script.mjs
// alone (no state carried between frames), so frames can be drawn in any order, by several browsers at once.
import * as THREE from "three";
import * as S from "./script.mjs";
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
const camera = new THREE.PerspectiveCamera(40, W / H, 0.1, 400);

// ------------------------------------------------------------------ helpers
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const smooth = (u) => { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); };
const ease = (a, b, t) => smooth((t - a) / (b - a));
const backOut = (u) => { u = clamp(u, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
const bump = (age, len) => (age < 0 || age > len ? 0 : Math.sin(Math.PI * age / len));
function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const keyframes = (kf, t) => {                      // [[t, v], ..] eased between keys
  if (t <= kf[0][0]) return kf[0][1];
  for (let i = 0; i < kf.length - 1; i++)
    if (t < kf[i + 1][0]) return lerp(kf[i][1], kf[i + 1][1], ease(kf[i][0], kf[i + 1][0], t));
  return kf[kf.length - 1][1];
};
// the toy's note colours (kid.c KID_NOTE_COL), C red .. B pink
const NOTE_COL = ["#ec2834", "#f65c28", "#ff8c1a", "#ffb81e", "#ffda24", "#82d638", "#46c46e", "#1eb096", "#4678d2", "#9254e2", "#c454d2", "#f256b0"];
const NOTE_NAME = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const RAINBOW = ["#ec3440", "#ff8c1e", "#ffd82e", "#50c85a", "#3880f4", "#9658e2", "#ff78be"];

// ------------------------------------------------------------------ voxels to a mesh (only the faces that show)
const FACES = [
  [[1, 0, 0], [[1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 0, 1]]], [[-1, 0, 0], [[0, 0, 1], [0, 1, 1], [0, 1, 0], [0, 0, 0]]],
  [[0, 1, 0], [[0, 1, 1], [1, 1, 1], [1, 1, 0], [0, 1, 0]]], [[0, -1, 0], [[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1]]],
  [[0, 0, 1], [[1, 0, 1], [1, 1, 1], [0, 1, 1], [0, 0, 1]]], [[0, 0, -1], [[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]]],
];
function voxGeometry(vox, size, ox = 0, oy = 0, oz = 0) {   // vox: Map "x,y,z" -> THREE.Color
  const pos = [], nor = [], col = [], idx = [];
  for (const [k, c] of vox) {
    const [x, y, z] = k.split(",").map(Number);
    for (const [n, q] of FACES) {
      if (vox.has(`${x + n[0]},${y + n[1]},${z + n[2]}`)) continue;
      const b = pos.length / 3;
      const shade = n[1] > 0 ? 1 : n[1] < 0 ? 0.7 : n[0] !== 0 ? 0.86 : 0.94;   // a touch of baked shade per face
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

// a pixel picture to plump voxels: each pixel a column through the figure, thicker the farther it is from the edge
function plump(w, h, at, opt = {}) {               // at(x, y): colour or null (y down)
  const dist = new Array(w * h).fill(0), q = [];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (!at(x, y)) continue;
    const edge = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => !at(x + dx, y + dy));
    if (edge) { dist[y * w + x] = 1; q.push([x, y]); }
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
  const max = opt.max ?? 7, k = opt.k ?? 1.9;
  const sets = {};
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

// ------------------------------------------------------------------ materials
const matVox = new THREE.MeshLambertMaterial({ vertexColors: true });
const shimU = { uT: { value: 0 }, uGain: { value: 0 } };
const matShim = new THREE.MeshLambertMaterial({ vertexColors: true });
matShim.onBeforeCompile = (sh) => {
  Object.assign(sh.uniforms, shimU);
  sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nvarying vec3 vLp;")
    .replace("#include <begin_vertex>", "#include <begin_vertex>\nvLp = position;");
  sh.fragmentShader = sh.fragmentShader.replace("#include <common>", "#include <common>\nvarying vec3 vLp;\nuniform float uT;\nuniform float uGain;")
    .replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\nfloat band = exp(-pow(vLp.x * 0.7 + vLp.y * 0.5 - uT, 2.0) * 5.0);\ntotalEmissiveRadiance += vColor.rgb * (0.25 + 1.6 * band) * uGain;");
};

// ------------------------------------------------------------------ the friends
const VS = 0.062;                                    // a pixel of the art, in the world
const friends = {};
for (const [key, c] of Object.entries(S.CAST)) {
  const p = PICS[key], pal = p.pal;
  const at = (x, y) => (x < 0 || y < 0 || x >= 48 || y >= 48 ? null : (p.px.charCodeAt(y * 48 + x) - 48 ? pal[p.px.charCodeAt(y * 48 + x) - 49] : null));
  const shim = new Set(p.shim || []);
  const sets = plump(48, 48, at, { split: shim.size ? (x, y) => (shim.has(p.px.charCodeAt(y * 48 + x) - 48) ? 1 : 0) : null });
  const root = new THREE.Group(), body = new THREE.Group();
  root.add(body);
  for (const [which, m] of Object.entries(sets)) {
    const mesh = new THREE.Mesh(voxGeometry(m, VS, -24 * VS, 0, 0), which === "1" ? matShim : matVox);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    body.add(mesh);
  }
  // the picture's real width and height (it sits on its bottom row, centred)
  let x0 = 48, x1 = 0, y0 = 48;
  for (let y = 0; y < 48; y++) for (let x = 0; x < 48; x++) if (at(x, y)) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); }
  scene.add(root);
  friends[key] = { root, body, c, height: (48 - y0) * VS, width: (x1 - x0 + 1) * VS };
}
// the sheep rides a cloud
const cloudVox = (r, seed, s) => {
  const R = rng(seed), m = new Map(), balls = [];
  for (let i = 0; i < 5; i++) balls.push([(R() - 0.5) * r * 2.2, (R() - 0.3) * r * 0.5, (R() - 0.5) * r * 0.8, r * (0.55 + R() * 0.45)]);
  for (let x = -r * 3; x <= r * 3; x++) for (let y = -r; y <= r * 1.5; y++) for (let z = -r * 1.5; z <= r * 1.5; z++)
    if (balls.some(([bx, by, bz, br]) => (x - bx) ** 2 + ((y - by) * 1.3) ** 2 + (z - bz) ** 2 < br * br))
      m.set(`${x},${y},${z}`, colorOf(y < -r * 0.2 ? "#e6ecff" : "#ffffff"));
  return voxGeometry(m, s);
};
{
  const cl = new THREE.Mesh(cloudVox(5, 7, 0.32), matVox);
  cl.position.set(0, -0.95, -0.2);
  cl.castShadow = true;
  friends.SHEEP.root.add(cl);
}

// ------------------------------------------------------------------ the island
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
      const c = grass ? ["#7ed957", "#74d04e", "#8ae262", "#6cc84a"][(i * 7 + j * 3 + y) & 3] : dirt ? ((i + j + y) & 1 ? "#b07a4a" : "#a06c40") : ((i + y) & 1 ? "#8d7fa0" : "#7d708f");
      m.set(`${i},${y},${j}`, colorOf(c));
    }
  }
  const g = voxGeometry(m, 0.4, 0, 0, 0);
  // (cells are 0.8 wide and 0.4 tall: stretch x and z)
  g.scale(CELL / 0.4, 1, CELL / 0.4);
  g.translate(-CELL / 2, -0.4, -CELL / 2);
  const mesh = new THREE.Mesh(g, matVox);
  mesh.receiveShadow = true;
  mesh.castShadow = true;
  island.add(mesh);
}
const groundY = (x, z) => (z < -4.5 ? Math.round(HILL(x, z) / 0.4) * 0.4 : 0);
// flowers, bushes, trees
{
  const R = rng(5), m = new Map(), S2 = 0.18;
  const spots = Object.values(S.CAST).map((c) => c.pos);
  let n = 0;
  while (n < 170) {
    const a = R() * Math.PI * 2, r = 2 + R() * 13.5, x = Math.cos(a) * r, z = Math.sin(a) * r * 0.92;
    if (spots.some((p) => Math.hypot(p[0] - x, p[2] - z) < 1.6)) continue;
    if (Math.hypot(x - 9.5, z + 7) < 1.5) continue;
    n++;
    const gx = Math.round(x / S2), gz = Math.round(z / S2), gy = Math.round(groundY(x, z) / S2);
    const hgt = 2 + Math.floor(R() * 2), col = ["#ff5c8a", "#ffd23e", "#ffffff", "#b07cff", "#ff8c3a", "#6fb8ff"][Math.floor(R() * 6)];
    for (let y = 0; y < hgt; y++) m.set(`${gx},${gy + y},${gz}`, colorOf("#3e9e48"));
    for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) m.set(`${gx + dx},${gy + hgt},${gz + dz}`, colorOf(col));
    m.set(`${gx},${gy + hgt},${gz}`, colorOf("#ffe066"));
  }
  const fl = new THREE.Mesh(voxGeometry(m, S2), matVox);
  fl.castShadow = true;
  island.add(fl);
  // bushes: the duck's (it hides behind it), and a few more
  const bush = (x, z, r, seed) => {
    const Rb = rng(seed), bm = new Map(), s = 0.3;
    for (let i = -r; i <= r; i++) for (let j = 0; j <= r * 1.4; j++) for (let k = -r; k <= r; k++)
      if (i * i + (j - r * 0.5) ** 2 * 1.6 + k * k < r * r + Rb() * 2) bm.set(`${i},${j},${k}`, colorOf(Rb() < 0.08 ? "#ff6f9a" : (i + j + k) & 1 ? "#3fae4f" : "#4cbf5a"));
    const b = new THREE.Mesh(voxGeometry(bm, s), matVox);
    b.position.set(x, groundY(x, z), z);
    b.castShadow = b.receiveShadow = true;
    island.add(b);
  };
  bush(-6.0, -2.6, 5, 1);
  bush(-11, -6, 4, 2);
  bush(12.5, 2, 3, 3);
  bush(-13, 3, 3, 4);
  // the owl's tree, with a branch for its perch
  const tm = new Map(), s = 0.3, tx = 9.5, tz = -7;
  for (let y = 0; y < 26; y++) for (let i = -1; i <= 1; i++) for (let k = -1; k <= 1; k++) if (Math.abs(i) + Math.abs(k) < 2 || y < 2) tm.set(`${i},${y},${k}`, colorOf((y + i) & 1 ? "#8a5a32" : "#7a4e2a"));
  for (let u = 0; u <= 8; u++) { const bx = Math.round(-u * 0.8), bz = Math.round(u * 0.36); tm.set(`${bx},16,${bz}`, colorOf("#8a5a32")); tm.set(`${bx},15,${bz}`, colorOf("#7a4e2a")); }
  const Rt = rng(9);
  for (let i = -9; i <= 9; i++) for (let j = 24; j <= 40; j++) for (let k = -9; k <= 9; k++) {
    const d = i * i + ((j - 32) * 1.15) ** 2 + k * k;
    if (d < 70 + Rt() * 14) tm.set(`${i},${j},${k}`, colorOf(Rt() < 0.05 ? "#ff8fb0" : (i + j + k) & 1 ? "#4cbf5a" : "#5ccf68"));
  }
  const tree = new THREE.Mesh(voxGeometry(tm, s), matVox);
  tree.position.set(tx, groundY(tx, tz), tz);
  tree.castShadow = tree.receiveShadow = true;
  island.add(tree);
}

// ------------------------------------------------------------------ the rainbow arch, a band a colour
const bands = [];
{
  for (let b = 0; b < 7; b++) {
    const m = new Map(), r0 = 23 - b, s = 1;
    for (let x = -24; x <= 24; x++) for (let y = 0; y <= 24; y++) {
      const r = Math.hypot(x, y);
      if (r >= r0 - 1 && r < r0) for (let z = 0; z < 2; z++) m.set(`${x},${y},${z}`, colorOf(RAINBOW[b]));
    }
    const mat = new THREE.MeshLambertMaterial({ vertexColors: true, emissive: new THREE.Color(RAINBOW[b]), emissiveIntensity: 0.15 });
    const mesh = new THREE.Mesh(voxGeometry(m, s, -0.5, -3, -19), mat);
    scene.add(mesh);
    bands.push(mat);
  }
}

// ------------------------------------------------------------------ sky, sun, moon, stars, clouds
const skyU = { uDay: { value: 1 }, uGlow: { value: 0 } };
const sky = new THREE.Mesh(new THREE.SphereGeometry(300, 32, 16), new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false, uniforms: skyU,
  vertexShader: "varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
  fragmentShader: `varying vec3 vP; uniform float uDay; uniform float uGlow;
    vec3 pick(vec3 n, vec3 d, vec3 y, float t){ return t < 0.5 ? mix(n, d, t * 2.0) : mix(d, y, t * 2.0 - 1.0); }
    void main(){
      float h = clamp(vP.y * 1.6 + 0.15, 0.0, 1.0);
      vec3 top = pick(vec3(0.04,0.06,0.2), vec3(0.42,0.36,0.78), vec3(0.36,0.66,1.0), uDay);
      vec3 hor = pick(vec3(0.16,0.17,0.42), vec3(1.0,0.68,0.55), vec3(0.82,0.93,1.0), uDay);
      vec3 c = mix(hor, top, pow(h, 0.8));
      c = mix(c, vec3(1.0,0.86,0.45), uGlow * 0.35 * (1.0 - h));
      gl_FragColor = vec4(pow(c, vec3(2.2)), 1.0);
    }`,
}));
scene.add(sky);
const sun = new THREE.Mesh(new THREE.SphereGeometry(7, 16, 12), new THREE.MeshBasicMaterial({ color: "#fff1a8" }));
scene.add(sun);
const moon = new THREE.Mesh(new THREE.SphereGeometry(4.5, 16, 12), new THREE.MeshBasicMaterial({ color: "#fff6dc" }));
scene.add(moon);
const starPts = (() => {
  const R = rng(3), p = [];
  for (let i = 0; i < 700; i++) {
    const a = R() * Math.PI * 2, e = 0.08 + R() * 1.3, r = 250;
    p.push(Math.cos(a) * Math.cos(e) * r, Math.sin(e) * r, Math.sin(a) * Math.cos(e) * r);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3));
  const m = new THREE.PointsMaterial({ color: "#ffffff", size: 2.4, sizeAttenuation: false, transparent: true, opacity: 0, depthWrite: false });
  const pts = new THREE.Points(g, m);
  scene.add(pts);
  return m;
})();
const clouds = [];
for (let i = 0; i < 9; i++) {
  const c = new THREE.Mesh(cloudVox(4 + (i % 3), 20 + i, 0.6), matVox);
  scene.add(c);
  clouds.push({ m: c, a: (i / 9) * Math.PI * 2 + 0.3, r: 34 + (i % 4) * 6, y: 11 + (i % 3) * 4 });
}

// ------------------------------------------------------------------ lights
const hemi = new THREE.HemisphereLight("#ffffff", "#5a7a4a", 1.2);
scene.add(hemi);
const sunL = new THREE.DirectionalLight("#fff4e0", 2.2);
sunL.castShadow = true;
sunL.shadow.mapSize.set(2048, 2048);
Object.assign(sunL.shadow.camera, { left: -24, right: 24, top: 24, bottom: -24, near: 1, far: 120 });
sunL.shadow.bias = -0.0006;
sunL.shadow.normalBias = 0.02;
scene.add(sunL, sunL.target);
const glowL = new THREE.PointLight("#ffd36b", 0, 30, 1.5);
glowL.position.set(0, 6, -5);
scene.add(glowL);

// ------------------------------------------------------------------ pixel-font voxel text (the toy's 5 x 7 letters)
function glyphAt(ch) { return FONT[ch] || null; }
function textPixels(text) {                          // 1 = letter, 2 = outline (a pixel round each letter)
  const w = text.length * 6 + 1, h = 9, px = new Array(w * h).fill(0);
  [...text].forEach((ch, i) => {
    const g = glyphAt(ch);
    if (!g) return;
    for (let y = 0; y < 7; y++) for (let x = 0; x < 5; x++) if ((g[y] >> (4 - x)) & 1) px[(y + 1) * w + i * 6 + x + 1] = 1;
  });
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (px[y * w + x]) continue;
    for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++)
      if (px[(y + dy) * w + x + dx] === 1 && y + dy >= 0 && y + dy < h && x + dx >= 0 && x + dx < w) px[y * w + x] = 2;
  }
  return { w, h, px };
}
function voxLetter(ch, color, s) {                    // one letter, outlined, standing on its baseline, centred
  const { w, h, px } = textPixels(ch);
  const sets = plump(w, h, (x, y) => (x < 0 || y < 0 || x >= w || y >= h ? null : px[y * w + x] === 1 ? color : px[y * w + x] === 2 ? OUTLINE : null), { max: 2, k: 1.4 });
  const m = new THREE.Mesh(voxGeometry(sets[0], s, -w * s / 2, 0, 0), matVox);
  m.castShadow = true;
  return m;
}
const title = [...S.TITLE.text].map((ch, i) => {
  if (ch === " ") return null;
  const n = S.TITLE.text.slice(0, i).replace(/ /g, "").length;
  const m = voxLetter(ch, RAINBOW[n % 7], 0.36);
  scene.add(m);
  return m;
});
const matGlow = new THREE.MeshLambertMaterial({ vertexColors: true, emissive: "#ffffff", emissiveIntensity: 0.0 });
matGlow.onBeforeCompile = (sh) => {
  sh.fragmentShader = sh.fragmentShader.replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\ntotalEmissiveRadiance += vColor.rgb * 0.75;");
};
const night = [...S.GOODNIGHT.text].map((ch, i) => {
  const m = voxLetter(ch, RAINBOW[i % 7], 0.36);
  m.material = matGlow;
  scene.add(m);
  return m;
});

// ------------------------------------------------------------------ the notes they sing: events
const NOTES = [];
for (const l of S.LINES) for (const [d, n, len] of l.notes) NOTES.push({ t: l.t + d, len, who: l.who, m: S.midi(n), n, line: l });
NOTES.sort((a, b) => a.t - b.t);
const lineEnd = (l) => l.t + Math.max(...l.notes.map(([d, , len]) => d + len));

// voxel eighth notes that float up from a singer, a colour per note
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
for (let i = 0; i < 40; i++) {
  const m = new THREE.Mesh(noteMesh(0), new THREE.MeshLambertMaterial({ vertexColors: true, transparent: true }));
  m.visible = false;
  scene.add(m);
  notePool.push(m);
}
const zPool = [];
for (let i = 0; i < 16; i++) {
  const m = voxLetter("Z", "#cfd8ff", 0.09);
  m.material = new THREE.MeshLambertMaterial({ vertexColors: true, transparent: true });
  m.visible = false;
  scene.add(m);
  zPool.push(m);
}

// ------------------------------------------------------------------ confetti and sparkles
const CONF_N = 420;
const confetti = new THREE.InstancedMesh(new THREE.BoxGeometry(0.16, 0.16, 0.03), new THREE.MeshLambertMaterial(), CONF_N);
confetti.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
{
  const R = rng(21);
  for (let i = 0; i < CONF_N; i++) confetti.setColorAt(i, colorOf(RAINBOW[i % 7]));
}
scene.add(confetti);
const BURSTS = [{ t: S.YES, at: [0, 2.5, 3], n: 200, seed: 1 }, { t: S.BIGEND, at: [0, 3, 0], n: 220, seed: 2 }];
const sparkles = (() => {                              // golden sparkles round the peacock, then fireflies at night
  const g = new THREE.BufferGeometry(), n = 120;
  g.setAttribute("position", new THREE.Float32BufferAttribute(new Float32Array(n * 3), 3));
  const m = new THREE.PointsMaterial({ color: "#ffe27a", size: 9, sizeAttenuation: false, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
  const p = new THREE.Points(g, m);
  scene.add(p);
  return { g, m, n };
})();

// ------------------------------------------------------------------ speech bubbles: the notes, coloured, with their letters
const BUB_W = 600, BUB_H = 320;
function drawLetters(ctx, text, x, y, s, fill) {     // the toy's font, with a dark outline
  for (const pass of [0, 1]) {
    [...text].forEach((ch, i) => {
      const g = glyphAt(ch);
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
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false }));
  sp.renderOrder = 10;
  sp.visible = false;
  scene.add(sp);
  bubbles.push({ cv, ctx: cv.getContext("2d"), tex, sp });
}
function drawBubble(b, line, t) {
  const ctx = b.ctx, sung = line.notes.filter(([d]) => line.t + d <= t + 0.02);
  ctx.clearRect(0, 0, BUB_W, BUB_H);
  // the bubble, as wide as its notes, with its tail down to the friend
  const slots = Math.min(6, line.notes.length) + (line.tag === "oops" ? 1 : 0), slot = 86;
  const bw = slots * slot + 64, x0 = (BUB_W - bw) / 2, x1 = x0 + bw, y0 = 10, y1 = BUB_H - 62, r = 50;
  const tx = BUB_W / 2 - 20;
  ctx.beginPath();
  ctx.moveTo(x0 + r, y0); ctx.arcTo(x1, y0, x1, y1, r); ctx.arcTo(x1, y1, x0, y1, r);
  ctx.lineTo(tx + 34, y1); ctx.lineTo(tx - 10, BUB_H - 8); ctx.lineTo(tx - 4, y1);
  ctx.arcTo(x0, y1, x0, y0, r); ctx.arcTo(x0, y0, x1, y0, r); ctx.closePath();
  ctx.fillStyle = "#ffffff"; ctx.fill();
  ctx.lineWidth = 10; ctx.strokeStyle = OUTLINE; ctx.stroke();
  // the last six notes: a coloured head (higher for a higher note) with a stem, and its letter under it
  const show = sung.slice(-6), n = show.length;
  const all = line.notes.map(([, nn]) => S.midi(nn)), lo = Math.min(...all), hi = Math.max(...all);
  const left = x0 + 32 + slot / 2 - 8;
  show.forEach(([d, nn, len], i) => {
    const m = S.midi(nn), pc = m % 12, age = t - (line.t + d);
    const pop = 1 + 0.5 * Math.exp(-age * 10);
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
  // a wrong note gets a question mark; a right answer a !
  if (line.tag === "oops" && n === line.notes.length && t > lineEnd(line) - 0.1) drawLetters(ctx, "?", left + 4 * slot - 12, 92, 9, "#ff5470");
  b.tex.needsUpdate = true;
}

// ------------------------------------------------------------------ the toy's band at the bottom: a word, sliding up
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
const NAME = { STAR: "STAR", DUCKY: "DUCKY", KITTY: "KITTY", BUNNY: "BUNNY", ELEPHANT: "ELEPHANT", BEAR: "BEAR", FROG: "FROG", APRIL: "APRIL", OWL: "OWL", PEACOCK: "PEACOCK", BEATBOT: "BEAT BOT", SHEEP: "SHEEP" };
const GREEN = ["#60c85a", "#389c42"], PURPLE = ["#966ee6", "#7854c8"], YESC = ["#38aa50", "#257a38"], NIGHTC = ["#286e46", "#185032"];
const BANDS = [
  ...Object.entries(S.ENTER).filter(([k]) => k !== "STAR").map(([k, e]) => ({ t: e.t + 0.2, len: 2.3, text: NAME[k], col: e.t > 88 ? NIGHTC : GREEN })),
  { t: 5.8, len: 2.0, text: "STAR", col: GREEN },
  { t: 31.9, len: 2.2, text: "COPY ME", col: PURPLE },
  { t: S.YES, len: 1.6, text: "YES!", col: YESC },
  { t: S.PARTY.t0 - 0.2, len: 2.2, text: "DANCE", col: PURPLE },
  { t: 88.5, len: 2.2, text: "NIGHT", col: PURPLE },
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
function singingLines(t) { return S.LINES.filter((l) => t >= l.t - 0.15 && t <= lineEnd(l) + 0.15); }
function noteKick(who, t) {                           // a hop on each note the friend starts
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
  let rotY = 0, rotZ = 0, rotX = 0, sx = 1, sy = 1, vis = true, scale = 1;
  const age = t - e.t;
  if (age < 0) return { vis: false };
  const from = new THREE.Vector3(...(e.from || c.pos));
  switch (e.kind) {
    case "twinkle": scale = backOut(age / 0.8); rotY = (1 - smooth(age / 1.2)) * Math.PI * 2; break;
    case "pop": {
      const u = clamp(age / 0.9, 0, 1);
      pos.lerpVectors(from, pos, u);
      pos.y += Math.sin(u * Math.PI) * 2.2 + (u < 1 ? 0 : 0);
      if (u < 0.15) pos.y = lerp(from.y, from.y + 1.4, u / 0.15);
      break;
    }
    case "peek": {
      const u = clamp(age / 0.55, 0, 1);
      pos.y = lerp(from.y, 0, backOut(u));
      break;
    }
    case "hop": case "run": case "walk": {
      const len = e.kind === "hop" ? 1.5 : e.kind === "run" ? 1.2 : 2.0, u = clamp(age / len, 0, 1);
      pos.lerpVectors(from, pos, smooth(u));
      const steps = e.kind === "hop" ? 3 : e.kind === "run" ? 6 : 5;
      const ph = u * steps;
      if (u < 1) {
        pos.y += Math.abs(Math.sin(ph * Math.PI)) * (e.kind === "hop" ? 1.1 : e.kind === "run" ? 0.35 : 0.12);
        rotZ = e.kind === "walk" ? Math.sin(ph * Math.PI) * 0.09 : 0;
        rotY = (from.x > c.pos[0] ? 1 : -1) * 0.35 * (1 - smooth((u - 0.8) / 0.2));
      }
      break;
    }
    case "leap": {
      const u = clamp(age / 1.0, 0, 1);
      pos.lerpVectors(from, pos, u);
      pos.y += Math.sin(u * Math.PI) * 4;
      rotZ = -u * Math.PI * 2 * (u < 1 ? 1 : 0);
      if (u >= 1) rotZ = 0;
      break;
    }
    case "fly": {
      const u = clamp(age / 1.8, 0, 1), su = smooth(u);
      pos.lerpVectors(from, pos, su);
      pos.y += Math.sin(u * Math.PI) * 2;
      if (u < 1) { sx = 1 + Math.sin(age * 30) * 0.12; rotY = 0.4 * (1 - su); }
      break;
    }
    case "rise": { const u = clamp(age / 1.6, 0, 1); pos.y = lerp(from.y, c.pos[1], backOut(u)); break; }
    case "drop": {
      const u = clamp(age / 0.6, 0, 1);
      pos.y = lerp(from.y, c.pos[1], u * u);
      if (age > 0.6) { const k = bump(age - 0.6, 0.35); sy = 1 - 0.3 * k; sx = 1 + 0.25 * k; }
      break;
    }
    case "float": { const u = clamp(age / 2.6, 0, 1); pos.lerpVectors(from, pos, smooth(u)); break; }
  }
  // landing squash, after arriving
  const land = { pop: 0.9, hop: 1.5, leap: 1.0, run: 1.2, walk: 2.0, peek: 0.55 }[e.kind];
  if (land) { const k = bump(age - land, 0.3); sy *= 1 - 0.18 * k; sx *= 1 + 0.12 * k; }
  // breathing, and a little look about
  const ph = (key.charCodeAt(0) * 0.37 + key.length) % 6;
  sy *= 1 + Math.sin(t * 2.2 + ph) * 0.018;
  // singing: a hop and a stretch on each note
  const kick = noteKick(key, t);
  pos.y += kick * 0.32;
  sy *= 1 + kick * 0.1; sx *= 1 - kick * 0.05;
  // the others turn a little toward whoever is singing
  const singers = singingLines(t).filter((l) => l.who !== key && l.who !== "STAR");
  if (singers.length && !singingLines(t).some((l) => l.who === key) && key !== "STAR" && age > 2) {
    const sp = S.CAST[singers[singers.length - 1].who].pos;
    rotY += clamp(Math.atan2(sp[0] - pos.x, 6) * 0.6, -0.5, 0.5);
  }
  // the frog's wrong note: dizzy; its right answer: a backflip
  if (key === "FROG") {
    const wob = ease(35.85, 36.1, t) * (1 - ease(37.4, 37.9, t));
    rotZ += Math.sin(t * 9) * 0.3 * wob; rotY += Math.sin(t * 5) * 0.4 * wob;
    const flip = clamp((t - S.YES) / 0.8, 0, 1);
    if (flip > 0 && flip < 1) { rotZ += flip * Math.PI * 2; pos.y += Math.sin(flip * Math.PI) * 2.6; }
  }
  // YES!: everyone jumps twice
  if (key !== "STAR" && key !== "OWL") pos.y += (bump(t - S.YES - 0.1, 0.45) + bump(t - S.YES - 0.6, 0.45)) * 0.8;
  // the peacock turns once, slowly, as its harp plays
  if (key === "PEACOCK") rotY += smooth((t - 47) / 2.4) * Math.PI * 2;
  // the party: a bounce on every beat, a sway every two
  const inParty = t >= S.PARTY.t0 && t < S.PARTY.t1 + 0.4 && !["STAR", "SHEEP"].includes(key);
  if (inParty) {
    const b = (t - S.PARTY.t0) / S.SPB, fb = b - Math.floor(b);
    const amp = key === "BEATBOT" ? 0.45 : key === "OWL" ? 0.12 : 0.28;
    const intro = ease(S.PARTY.t0, S.PARTY.t0 + 0.4, t) * (1 - ease(S.PARTY.t1, S.PARTY.t1 + 0.4, t));
    pos.y += Math.pow(Math.sin(fb * Math.PI), 1.5) * amp * intro;
    rotZ += Math.sin(b * Math.PI / 2 + ph) * 0.12 * intro;
    rotY += Math.sin(b * Math.PI / 4 + ph) * 0.25 * intro;
    const k = Math.exp(-fb * 10) * intro;
    sy *= 1 - 0.07 * k; sx *= 1 + 0.05 * k;
  }
  // the end of the party: a big jump on the last chord
  if (key !== "STAR" && key !== "OWL" && key !== "SHEEP") pos.y += bump(t - S.BIGEND, 0.6) * 1.4;
  // the yawn and sleep
  if (key === "DUCKY") { const y = bump(t - 85.0, 2.1); sy *= 1 + 0.12 * y; sx *= 1 - 0.05 * y; }
  const z = S.SLEEP[key];
  if (z !== undefined) {
    const s = smooth((t - z) / 1.4);
    rotZ += s * (key === "PEACOCK" ? 0.12 : 0.28) * (ph > 3 ? 1 : -1);
    sy *= 1 - 0.08 * s + Math.sin(t * 1.3 + ph) * 0.02 * s;
    pos.y -= 0.06 * s;
  }
  if (key === "STAR") { pos.y += Math.sin(t * 1.4) * 0.25; rotZ += Math.sin(t * 0.9) * 0.12; sx *= 1.7; sy *= 1.7; }
  if (key === "SHEEP") pos.y += Math.sin(t * 0.8) * 0.2;
  const mid = (key === "FROG" && (t - S.YES > 0 && t - S.YES < 0.8 || age < 1.0));
  return { vis, pos, rotY, rotZ, rotX, sx: sx * scale, sy: sy * scale, scale, mid };
}

// ------------------------------------------------------------------ the camera
function camAt(t) {
  const K = S.CAM, P0 = S.PARTY.t0, P1 = 84.2;
  if (t > P0 && t < P1) {                             // the party: once round the island
    const u = smooth((t - P0) / (P1 - P0)), a = u * Math.PI * 2;
    const r = 17 + 2 * u + Math.sin(u * Math.PI) * 1.5, y = 6.5 + u + Math.sin(u * Math.PI * 2) * 1.2;
    return { p: new THREE.Vector3(Math.sin(a) * r, y, Math.cos(a) * r), l: new THREE.Vector3(0, 1.6 + 0.2 * u, 0) };
  }
  let i = 0;
  while (i < K.length - 2 && t >= K[i + 1][0]) i++;
  const u = smooth((t - K[i][0]) / (K[i + 1][0] - K[i][0]));
  const a = K[i], b = K[i + 1];
  return {
    p: new THREE.Vector3(lerp(a[1][0], b[1][0], u), lerp(a[1][1], b[1][1], u), lerp(a[1][2], b[1][2], u)),
    l: new THREE.Vector3(lerp(a[2][0], b[2][0], u), lerp(a[2][1], b[2][1], u), lerp(a[2][2], b[2][2], u)),
  };
}

// ------------------------------------------------------------------ one frame
const tmpM = new THREE.Matrix4(), tmpQ = new THREE.Quaternion(), tmpE = new THREE.Euler(), tmpV = new THREE.Vector3(), one = new THREE.Vector3(1, 1, 1);
window.renderAt = (t) => {
  const c = camAt(t);                                // the camera first: the bubbles size themselves by it
  camera.position.copy(c.p);
  camera.lookAt(c.l);
  camera.updateMatrixWorld();
  // sky and light
  const day = keyframes(S.SKY, t), glow = keyframes(S.GLOW, t);
  skyU.uDay.value = day; skyU.uGlow.value = glow;
  const sunUp = smooth((day - 0.35) / 0.65);
  sun.position.set(-40, lerp(-20, 60, sunUp), -150);
  moon.position.set(30, lerp(-20, 48, 1 - smooth(day / 0.6)), -150);
  starPts.opacity = 1 - smooth(day / 0.45);
  hemi.intensity = lerp(0.55, 1.25, day);
  hemi.color.set(day < 0.5 ? "#8fa0ff" : "#ffffff");
  hemi.groundColor.set(day < 0.5 ? "#2a3060" : "#5a7a4a");
  sunL.intensity = lerp(0.6, 2.2, day);
  sunL.color.set(day > 0.75 ? "#fff4e0" : day > 0.35 ? "#ffb07a" : "#9fb4ff");
  sunL.position.set(day > 0.4 ? -14 : 14, 30, 18);
  sunL.target.position.set(0, 0, -2);
  scene.fog = null;
  glowL.intensity = glow * 60;
  for (const c of clouds) {
    const a = c.a + t * 0.008;
    c.m.position.set(Math.cos(a) * c.r, c.y, Math.sin(a) * c.r - 10);
  }
  // the rainbow: a band lights on each beat of the party, all together on the last chord
  const pb = (t - S.PARTY.t0) / S.SPB;
  bands.forEach((m, i) => {
    let e = 0.12 + (1 - day) * 0.35;
    if (pb >= 0 && t < S.PARTY.t1) e += 0.9 * Math.exp(-((pb - Math.floor(pb)) * 6)) * (Math.floor(pb) % 7 === i ? 1 : 0.15);
    e += 1.2 * bump(t - S.BIGEND, 1.5) + glow * 0.4;
    m.emissiveIntensity = e;
  });
  // the title, letter by letter as the star rings it, then away up into the sky
  title.forEach((m, i) => {
    if (!m) return;
    const t0 = S.TITLE.t0 + i * S.TITLE.step, age = t - t0;
    const n = title.length, x = (i - (n - 1) / 2) * 2.35, arc = -Math.pow((i - (n - 1) / 2) / ((n - 1) / 2), 2) * 1.6;
    const away = smooth((t - S.TITLE.out - i * 0.04) / 1.3);
    m.visible = age > 0 && away < 1;
    if (!m.visible) return;
    const s = backOut(age / 0.45);
    m.position.set(x, 12.2 + arc + Math.sin(t * 2 + i) * 0.12 + away * 14, -3 - away * 4);
    m.rotation.set(0, Math.sin(t * 1.3 + i * 0.6) * 0.18, Math.sin(t * 2 + i) * 0.05);
    m.scale.setScalar(s * (1 + bump(age, 0.3) * 0.3));
  });
  night.forEach((m, i) => {
    const age = t - S.GOODNIGHT.t0 - i * 0.18, n = night.length;
    m.visible = age > 0;
    if (!m.visible) return;
    m.position.set((i - (n - 1) / 2) * 2.35, 12.4 - Math.pow((i - (n - 1) / 2) / ((n - 1) / 2), 2) * 1.2 + Math.sin(t * 1.5 + i) * 0.15, -3);
    m.rotation.set(0, Math.sin(t + i) * 0.15, 0);
    m.scale.setScalar(backOut(age / 0.6));
  });
  // the friends
  for (const key of Object.keys(friends)) {
    const f = friends[key], p = friendPose(key, t);
    f.root.visible = p.vis;
    if (!p.vis) continue;
    f.root.position.copy(p.pos);
    f.root.rotation.set(p.rotX, p.rotY, 0);
    f.body.rotation.set(0, 0, p.rotZ);
    f.body.scale.set(p.sx, p.sy, (p.sx + p.sy) / 2);
    const hcy = p.mid ? f.height / 2 : 0;               // (a flip turns round the middle of the friend, a sway round its feet)
    f.body.position.set(Math.sin(p.rotZ) * hcy, hcy - Math.cos(p.rotZ) * hcy, 0);
  }
  shimU.uT.value = ((t * 1.6) % 5) - 1.5;
  shimU.uGain.value = 0.35 + 0.9 * glow;
  // the notes floating up from whoever sings them
  let pi = 0;
  for (const e of NOTES) {
    if (e.t > t || pi >= notePool.length) { if (e.t > t) break; continue; }
    const age = t - e.t;
    if (age > 2.0) continue;
    const m = notePool[pi++], f = friends[e.who], p = f.root.position;
    m.geometry = noteMesh(e.m % 12);
    const R = rng(Math.round(e.t * 1000));
    const side = (R() - 0.5) * 1.6;
    m.visible = true;
    m.position.set(p.x + side + Math.sin(age * 3 + side) * 0.3, p.y + f.height * 0.9 + age * 1.5, p.z + 0.4);
    m.rotation.set(0, Math.sin(age * 2) * 0.6, Math.sin(age * 4) * 0.2);
    m.scale.setScalar(backOut(age / 0.25) * (e.who === "STAR" ? 1.4 : 1.1));
    m.material.opacity = 1 - smooth((age - 1.3) / 0.7);
  }
  for (; pi < notePool.length; pi++) notePool[pi].visible = false;
  // Z's over the sleepers
  let zi = 0;
  for (const [key, z0] of Object.entries(S.SLEEP)) {
    for (let k = 0; k < 3; k++) {
      const period = 2.4, age = ((t - z0 - 1.5 - k * 0.8) % period + period) % period;
      if (t < z0 + 1.5 + k * 0.8 || zi >= zPool.length) continue;
      const m = zPool[zi++], f = friends[key], p = f.root.position;
      m.visible = true;
      m.position.set(p.x + 0.4 + age * 0.5, p.y + f.height + age * 0.9, p.z + 0.2);
      m.scale.setScalar(0.7 + age * 0.35);
      m.material.opacity = Math.min(1, age * 3) * (1 - smooth((age - 1.6) / 0.8));
    }
  }
  for (; zi < zPool.length; zi++) zPool[zi].visible = false;
  // confetti
  let ci = 0;
  for (const bst of BURSTS) {
    const age = t - bst.t;
    if (age < 0 || age > 4) continue;
    const R = rng(bst.seed);
    for (let i = 0; i < bst.n && ci < CONF_N; i++, ci++) {
      const a = R() * Math.PI * 2, up = 7 + R() * 7, out = 2 + R() * 6, spin = R() * 10;
      const drag = (1 - Math.exp(-age * 1.2)) / 1.2;
      tmpV.set(bst.at[0] + Math.cos(a) * out * drag, bst.at[1] + up * drag - 2.2 * age * age * 0.5 - Math.max(0, age - 1) * 0.6, bst.at[2] + Math.sin(a) * out * drag);
      tmpE.set(spin * age, spin * age * 0.7, age * 3 + i);
      tmpQ.setFromEuler(tmpE);
      tmpM.compose(tmpV, tmpQ, one.clone().multiplyScalar(age > 3.4 ? 1 - (age - 3.4) / 0.6 : 1));
      confetti.setMatrixAt(ci, tmpM);
    }
  }
  confetti.count = ci;
  confetti.instanceMatrix.needsUpdate = true;
  // golden sparkles round the peacock; fireflies at night
  {
    const pos = sparkles.g.attributes.position, R = rng(8);
    const fire = 1 - smooth((day - 0.1) / 0.4);
    for (let i = 0; i < sparkles.n; i++) {
      const a = R() * Math.PI * 2, r = 1 + R() * 4, h = R() * 5, sp = 0.3 + R();
      if (i < 60) pos.setXYZ(i, Math.cos(a + t * sp) * r, 1.8 + h + Math.sin(t * 2 + i) * 0.3, -7.6 + Math.sin(a + t * sp) * r * 0.6);
      else pos.setXYZ(i, Math.cos(a + t * sp * 0.3) * (3 + r * 2.5), 0.6 + h * 0.6 + Math.sin(t * 1.3 + i) * 0.5, -1 + Math.sin(a + t * sp * 0.3) * (2 + r * 1.5));
    }
    pos.needsUpdate = true;
    sparkles.m.opacity = Math.max(glow, fire * 0.9);
    sparkles.m.color.set(glow > fire ? "#ffe27a" : "#d8ff7a");
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
