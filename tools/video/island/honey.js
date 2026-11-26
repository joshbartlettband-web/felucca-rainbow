// The Bear and the Balloon: a clearing in a wood, a honey tree with bees in a hole near the top, a gorse bush at its foot,
// Robin's cottage, a mud puddle, and the props the story needs (two balloons, an umbrella, a cork popgun). renderAt(t)
// draws the frame at time t from honey.mjs alone.
import * as THREE from "three";
import * as S from "./honey.mjs";
import { PICS, OUTLINE } from "./pics.js";
import { clamp, lerp, smooth, ease, backOut, bump, rng, NOTE_COL, voxGeometry, colorOf, plump, voxLetter, noteMesh,
  bubbleSystem, bandSystem } from "./common.js";

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
scene.fog = new THREE.FogExp2("#d4ecff", 0.0085);
const camera = new THREE.PerspectiveCamera(40, W / H, 0.1, 500);
const V3 = (a) => new THREE.Vector3(...a);
const matVox = new THREE.MeshLambertMaterial({ vertexColors: true });
const mesh = (vox, s, o = [0, 0, 0], mat = matVox) => {
  const m = new THREE.Mesh(voxGeometry(vox, s, ...o), mat);
  m.castShadow = m.receiveShadow = true;
  return m;
};

// ------------------------------------------------------------------ the friends
const VS = 0.062;
function buildPic(p, scale = 1) {
  const w = p.w || 48, h = p.h || 48, pal = p.pal;
  const at = (x, y) => (x < 0 || y < 0 || x >= w || y >= h ? null : (p.px.charCodeAt(y * w + x) - 48 ? pal[p.px.charCodeAt(y * w + x) - 49] : null));
  const g = new THREE.Group();
  for (const m of Object.values(plump(w, h, at))) g.add(mesh(m, VS, [-(w / 2) * VS, 0, 0]));
  let y0 = h;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (at(x, y)) y0 = Math.min(y0, y);
  g.scale.setScalar(scale);
  return { g, height: (h - y0) * VS * scale };
}
const actor = (pic, scale = 1) => {
  const root = new THREE.Group(), body = new THREE.Group(), { g, height } = buildPic(PICS[pic], scale);
  body.add(g); root.add(body); scene.add(root);
  return { root, body, g, height };
};
const bear = actor("BEAR"), robin = actor("ROBIN", 0.95), bee = actor("BEE", 0.5), fly = actor("BUTTERFLY", 0.34);
const mud = buildPic(PICS.BEAR_MUD);
bear.body.add(mud.g);
const who = { BEAR: bear, ROBIN: robin, BEE: bee, BUTTERFLY: fly };

// ------------------------------------------------------------------ the ground: grass, a path, the puddle, low hills far off
{
  const R = rng(4), m = new Map(), CELL = 1, RAD = 48;
  const pathD = (x, z) => {                                     // distance to the paths: in from the right, to the tree, to the house
    const seg = (ax, az, bx, bz) => { const dx = bx - ax, dz = bz - az, u = clamp(((x - ax) * dx + (z - az) * dz) / (dx * dx + dz * dz), 0, 1); return Math.hypot(x - ax - u * dx, z - az - u * dz); };
    return Math.min(seg(20, 4, 4, 0.8), seg(4, 0.8, 6, -3.5), seg(4, 0.8, -7.5, -2.6), seg(-7.5, -2.6, -9.5, -4));
  };
  for (let i = -RAD; i <= RAD; i++) for (let j = -RAD; j <= RAD; j++) {
    const x = i * CELL, z = j * CELL, r = Math.hypot(x, z);
    if (r > RAD) continue;
    const hill = r > 20 ? Math.round((Math.sin(x * 0.21) * Math.cos(z * 0.17) * 1.5 + 1.2) * smooth((r - 20) / 14) * 2) : 0;
    const puddle = Math.hypot(x - S.PUDDLE[0], (z - S.PUDDLE[2]) * 1.2) < 1.9;
    for (let y = -1; y <= hill; y++) {
      let c = ["#7ed957", "#74cf4e", "#86df5e", "#6cc84a"][(i * 7 + j * 3) & 3];
      if (y < hill) c = "#9a6a3e";
      else if (puddle) c = "#4a3a30";
      else if (pathD(x, z) < 0.9 + R() * 0.3) c = (i + j) & 1 ? "#d8b47c" : "#ccaa72";
      m.set(`${i},${y},${j}`, colorOf(c));
    }
    if (puddle) m.delete(`${i},0,${j}`);
  }
  const g = voxGeometry(m, 1, -0.5, -1, -0.5);
  g.scale(1, 0.4, 1);
  const ground = new THREE.Mesh(g, matVox);
  ground.receiveShadow = true;
  scene.add(ground);
  // the puddle's shine
  const shine = new THREE.Mesh(new THREE.CylinderGeometry(1.7, 1.7, 0.02, 24), new THREE.MeshLambertMaterial({ color: "#5a463a", emissive: "#2a2018" }));
  shine.scale.set(1, 1, 0.83);
  shine.position.set(S.PUDDLE[0], -0.33, S.PUDDLE[2]);
  scene.add(shine);
}

// ------------------------------------------------------------------ the honey tree, its branches, the bees' hole
const breakable = new THREE.Group();
{
  const s = 0.3, m = new Map(), [tx, , tz] = S.TREE, R = rng(41);
  for (let y = -1; y < 50; y++) {
    const rr = 4.4 - y * 0.02 + (y < 4 ? (4 - y) * 0.5 : 0);
    for (let i = -7; i <= 7; i++) for (let k = -7; k <= 7; k++)
      if (Math.hypot(i, k) < rr) m.set(`${i},${y},${k}`, colorOf((y + i * 3 + k) % 5 ? "#8a5a32" : "#76492a"));
  }
  // the hole near the top, on the front: dark inside, honey at the bottom
  const hy = Math.round(S.HOLE[1] / s);
  for (let y = hy - 3; y <= hy + 3; y++) for (let i = -2; i <= 2; i++) for (let k = 2; k <= 6; k++) {
    if ((i * i) / 6 + ((y - hy) * (y - hy)) / 10 > 1) continue;
    m.delete(`${i},${y},${k}`);
    if (k === 2) m.set(`${i},${y},1`, colorOf(y < hy - 1 ? "#ffb81e" : "#2a1a10"));
  }
  for (const [i, y] of [[-1, hy - 4], [1, hy - 4], [1, hy - 5], [0, hy - 4]]) m.set(`${i},${y},4`, colorOf("#ffb81e"));   // a drip of honey
  // the branches the bear climbs (the top one breaks)
  S.BRANCHES.forEach(([bx, by], n) => {
    const bm = n === 4 ? new Map() : m;
    const dir = Math.sign(bx - tx), from = 3, to = Math.round(Math.abs(bx - tx) / s) + 2, yy = Math.round(by / s);
    for (let u = from; u <= to; u++) for (let dy = -1; dy <= 0; dy++) for (let k = 3; k <= 6; k++)
      bm.set(`${dir * u},${yy + dy + (u > to - 2 ? 1 : 0) * 0},${k}`, colorOf((u + dy) & 1 ? "#8a5a32" : "#7a4e2a"));
    if (n === 4) breakable.add(mesh(bm, s));
  });
  // the canopy: three round blobs of leaves
  for (const [cx, cy, cz, r] of [[0, 62, -2, 15], [-9, 58, -1, 11], [9, 59, -3, 11]])
    for (let i = -r; i <= r; i++) for (let j = -r; j <= r; j++) for (let k = -r; k <= r; k++)
      if (i * i + (j * 1.2) ** 2 + k * k < r * r + R() * 10) m.set(`${cx + i},${cy + j},${cz + k}`, colorOf(R() < 0.03 ? "#ff8fb0" : (i + j + k) & 1 ? "#4cbf5a" : "#5ccf68"));
  const tree = mesh(m, s);
  tree.position.set(tx, 0, tz);
  scene.add(tree);
  breakable.position.set(tx, 0, tz);
  scene.add(breakable);
}
// the gorse bush: prickly green, little yellow flowers
{
  const m = new Map(), R = rng(5), s = 0.22;
  for (let i = -8; i <= 8; i++) for (let j = 0; j <= 9; j++) for (let k = -7; k <= 7; k++)
    if (i * i + ((j - 3.5) * 1.3) ** 2 + k * k < 60 + R() * 16) m.set(`${i},${j},${k}`, colorOf(R() < 0.14 ? "#ffd82e" : (i + j + k) & 1 ? "#2f7d3c" : "#3b8e46"));
  for (let n = 0; n < 40; n++) {                                // the prickles: spikes poking out
    const a = R() * Math.PI * 2, e = R() * 1.2, r = 8.5;
    m.set(`${Math.round(Math.cos(a) * Math.cos(e) * r)},${Math.round(3.5 + Math.sin(e) * r * 0.8)},${Math.round(Math.sin(a) * Math.cos(e) * r)}`, colorOf("#1f5c2a"));
  }
  const g = mesh(m, s);
  g.position.set(...S.GORSE);
  scene.add(g);
}
// Robin's cottage: cream walls, a red roof, a round window, a green door that opens
const door = new THREE.Group();
{
  const s = 0.25, m = new Map(), Wd = 9, Dp = 8, Hh = 10;
  for (let i = -Wd; i <= Wd; i++) for (let k = -Dp; k <= Dp; k++) for (let y = 0; y < Hh; y++) {
    if (Math.abs(i) < Wd && Math.abs(k) < Dp) continue;
    m.set(`${i},${y},${k}`, colorOf((i + y) % 4 ? "#fff1d6" : "#f2e2c2"));
  }
  for (let y = 0; y < 13; y++) for (let i = -Wd - 1 + y; i <= Wd + 1 - y; i++) for (let k = -Dp - 1; k <= Dp + 1; k++)
    if (i === -Wd - 1 + y || i === Wd + 1 - y || y === 12) m.set(`${i},${Hh + y},${k}`, colorOf((k + y) & 1 ? "#d9443c" : "#c23a34"));
  for (let y = Hh + 4; y < Hh + 12; y++) for (let i = 4; i <= 5; i++) for (let k = -2; k <= -1; k++) m.set(`${i},${y},${k}`, colorOf("#9a8a8a"));   // chimney
  for (let i = -2; i <= 2; i++) for (let y = 0; y < 7; y++) m.delete(`${i},${y},${Dp}`);                            // the doorway
  for (const cx of [-6, 6]) for (let i = -2; i <= 2; i++) for (let y = 4; y <= 8; y++)                                 // round windows
    if ((i * i + (y - 6) * (y - 6)) < 5) m.set(`${cx + i},${y},${Dp}`, colorOf(i * i + (y - 6) * (y - 6) < 2 ? "#bfe6ff" : "#8a5a32"));
  const house = mesh(m, s);
  house.position.set(...S.HOUSE);
  scene.add(house);
  const dm = new Map();
  for (let i = 0; i < 5; i++) for (let y = 0; y < 7; y++) dm.set(`${i},${y},0`, colorOf(i === 3 && y === 3 ? "#ffd82e" : (i + y) & 1 ? "#3e9e48" : "#358c3f"));
  door.add(mesh(dm, s, [0, 0, -s]));
  door.position.set(S.HOUSE[0] - 2.5 * s, 0, S.HOUSE[2] + Dp * s + s);
  scene.add(door);
}
// the wood round the clearing, flowers in the grass, clouds
{
  const R = rng(13), tm = new Map(), s = 0.5;
  let n = 0;
  while (n < 70) {
    const a = R() * Math.PI * 2, r = 17 + R() * 26, x = Math.cos(a) * r, z = Math.sin(a) * r;
    if (z > 4 && Math.abs(x) < 16 + z * 0.4 && r < 34) continue;      // (the cameras' side stays open)
    n++;
    const gx = Math.round(x / s), gz = Math.round(z / s), h = 8 + Math.floor(R() * 8), pine = R() < 0.45;
    for (let y = 0; y < h; y++) for (const [i, k] of [[0, 0], [1, 0], [0, 1], [1, 1]]) tm.set(`${gx + i},${y},${gz + k}`, colorOf("#7a4e2a"));
    const lr = 3 + Math.floor(R() * 3), leaf = pine ? ["#2f8a4a", "#277a40"] : ["#5cc45a", "#4fb24e"];
    for (let i = -lr - 1; i <= lr + 1; i++) for (let j = -lr; j <= lr * 2; j++) for (let k = -lr - 1; k <= lr + 1; k++) {
      const inside = pine ? Math.hypot(i, k) < (lr + 1) * (1 - (j + lr) / (lr * 3.2)) : i * i + j * j * 0.8 + k * k < lr * lr + 2;
      if (inside) tm.set(`${gx + i},${h + j + (pine ? lr : 0)},${gz + k}`, colorOf(leaf[(i + j + k) & 1]));
    }
  }
  scene.add(mesh(tm, s));
  const fm = new Map(), fs = 0.18;
  for (let k = 0; k < 160; k++) {
    const a = R() * Math.PI * 2, r = 2 + R() * 15, x = Math.cos(a) * r, z = Math.sin(a) * r;
    if (Math.hypot(x - S.TREE[0], z - S.TREE[2]) < 3 || Math.hypot(x - S.HOUSE[0], z - S.HOUSE[2]) < 4.5 || Math.hypot(x - S.PUDDLE[0], z - S.PUDDLE[2]) < 2.6 || Math.hypot(x - S.GORSE[0], z - S.GORSE[2]) < 2.4) continue;
    const gx = Math.round(x / fs), gz = Math.round(z / fs), col = ["#ff5c8a", "#ffd23e", "#ffffff", "#b07cff", "#6fb8ff"][Math.floor(R() * 5)];
    for (let y = 0; y < 2; y++) fm.set(`${gx},${y},${gz}`, colorOf("#3e9e48"));
    for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) fm.set(`${gx + dx},2,${gz + dz}`, colorOf(col));
    fm.set(`${gx},2,${gz}`, colorOf("#ffe066"));
  }
  scene.add(mesh(fm, fs));
}
const cloudVox = (r, seed) => {
  const R = rng(seed), m = new Map(), balls = [];
  for (let i = 0; i < 5; i++) balls.push([(R() - 0.5) * r * 2.2, (R() - 0.3) * r * 0.5, (R() - 0.5) * r * 0.8, r * (0.55 + R() * 0.45)]);
  for (let x = -r * 3; x <= r * 3; x++) for (let y = -r; y <= r * 1.5; y++) for (let z = -r * 1.5; z <= r * 1.5; z++)
    if (balls.some(([bx, by, bz, br]) => (x - bx) ** 2 + ((y - by) * 1.3) ** 2 + (z - bz) ** 2 < br * br)) m.set(`${x},${y},${z}`, colorOf(y < -r * 0.2 ? "#e6ecff" : "#ffffff"));
  return m;
};
const clouds = [];
for (let i = 0; i < 8; i++) {
  const c = new THREE.Mesh(voxGeometry(cloudVox(4 + (i % 3), 30 + i), 0.7), matVox);
  scene.add(c);
  clouds.push({ m: c, a: (i / 8) * Math.PI * 2, r: 50 + (i % 3) * 10, y: 22 + (i % 3) * 5 });
}
const sky = new THREE.Mesh(new THREE.SphereGeometry(400, 32, 16), new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false, fog: false,
  vertexShader: "varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
  fragmentShader: "varying vec3 vP; void main(){ float h = clamp(vP.y * 1.4 + 0.1, 0.0, 1.0); vec3 c = mix(vec3(0.85,0.93,1.0), vec3(0.38,0.66,1.0), pow(h, 0.7)); gl_FragColor = vec4(pow(c, vec3(2.2)), 1.0); }",
}));
scene.add(sky);
const sun = new THREE.Mesh(new THREE.SphereGeometry(10, 16, 12), new THREE.MeshBasicMaterial({ color: "#fff3b0", fog: false }));
sun.position.set(-90, 120, -260);
scene.add(sun);
scene.add(new THREE.HemisphereLight("#ffffff", "#6a8a4a", 1.25));
const sunL = new THREE.DirectionalLight("#fff0d8", 2.1);
sunL.position.set(-12, 30, 16);
sunL.castShadow = true;
sunL.shadow.mapSize.set(2048, 2048);
Object.assign(sunL.shadow.camera, { left: -22, right: 22, top: 26, bottom: -14, near: 1, far: 120 });
sunL.shadow.bias = -0.0006;
sunL.shadow.normalBias = 0.02;
sunL.target.position.set(0, 4, -2);
scene.add(sunL, sunL.target);

// ------------------------------------------------------------------ props: balloons, strings, an umbrella, a popgun, little bees
const balloonVox = (col, dark) => {
  const m = new Map();
  for (let i = -6; i <= 6; i++) for (let j = -7; j <= 8; j++) for (let k = -6; k <= 6; k++) {
    if (i * i / 36 + (j > 0 ? j * j / 64 : j * j / 49) + k * k / 36 > 1) continue;
    const hi = (i + 3) ** 2 + (j - 4) ** 2 + (k - 5) ** 2 < 5;
    m.set(`${i},${j},${k}`, colorOf(hi ? "#ffffff" : i + k > 4 ? dark : col));
  }
  for (const [i, j] of [[0, -8], [-1, -9], [0, -9], [1, -9]]) m.set(`${i},${j},0`, colorOf(dark));   // the knot
  return m;
};
const balloon = (col, dark) => {
  const g = new THREE.Group();
  g.add(mesh(balloonVox(col, dark), 0.16, [0, 0, 0]));
  scene.add(g);
  return g;
};
const blueB = balloon("#4a90ff", "#2f62c8"), greenB = balloon("#58d060", "#38a048");
const stringMat = new THREE.MeshBasicMaterial({ color: "#f4f0ff" });
const stringOf = () => { const m = new THREE.Mesh(new THREE.BoxGeometry(0.03, 1, 0.03), stringMat); scene.add(m); return m; };
const blueS = stringOf(), greenS = stringOf();
function stretch(m, a, b) {                                   // a thin box from point a to point b
  const d = new THREE.Vector3().subVectors(b, a), len = d.length();
  m.position.copy(a).addScaledVector(d, 0.5);
  m.scale.set(1, Math.max(0.01, len), 1);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
}
const umbrella = new THREE.Group();
{
  const m = new Map(), s = 0.1;
  for (let i = -13; i <= 13; i++) for (let k = -13; k <= 13; k++) {
    const r = Math.hypot(i, k);
    if (r > 13) continue;
    const y = Math.round(6 - r * r / 30), panel = Math.floor(((Math.atan2(k, i) + Math.PI) / (Math.PI * 2)) * 8);
    m.set(`${i},${y},${k}`, colorOf(panel & 1 ? "#ff5c7a" : "#ffffff"));
    m.set(`${i},${y - 1},${k}`, colorOf(panel & 1 ? "#d84462" : "#e6e6f0"));
  }
  for (let y = -26; y < 7; y++) m.set(`0,${y},0`, colorOf("#6a4a3a"));
  for (const [i, y] of [[1, -27], [2, -27], [3, -26], [3, -25]]) m.set(`${i},${y},0`, colorOf("#6a4a3a"));
  umbrella.add(mesh(m, s, [0, 2.6, 0]));
  scene.add(umbrella);
}
const gun = new THREE.Group(), cork = new THREE.Group();
{
  const m = new Map(), s = 0.07;
  for (let x = 0; x < 12; x++) for (let y = 0; y < 2; y++) for (let z = 0; z < 2; z++) m.set(`${x},${y},${z}`, colorOf(x > 9 ? "#c88a4a" : "#8890a8"));
  for (let x = -6; x < 1; x++) for (let y = -2; y < 2; y++) for (let z = 0; z < 2; z++) if (!(x < -3 && y < -1)) m.set(`${x},${y},${z}`, colorOf("#8a5a32"));
  gun.add(mesh(m, s, [0, -0.07, -0.07]));
  scene.add(gun);
  const cm = new Map();
  for (let x = 0; x < 3; x++) for (let y = 0; y < 2; y++) for (let z = 0; z < 2; z++) cm.set(`${x},${y},${z}`, colorOf("#d8a866"));
  cork.add(mesh(cm, 0.08, [-0.12, -0.08, -0.08]));
  scene.add(cork);
}
const beeVox = (() => {
  const m = new Map();
  for (let x = 0; x < 4; x++) for (let y = 0; y < 3; y++) for (let z = 0; z < 3; z++) m.set(`${x},${y},${z}`, colorOf(x === 1 || x === 3 ? "#2a1a10" : "#ffd23e"));
  m.set("1,3,1", colorOf("#e8f4ff")); m.set("2,3,1", colorOf("#e8f4ff"));
  return voxGeometry(m, 0.075, -0.15, -0.11, -0.11);
})();
const bees = [];
for (let i = 0; i < 14; i++) { const b = new THREE.Mesh(beeVox, matVox); scene.add(b); bees.push(b); }

// bits: mud, prickles, balloon pieces, a puff of breath
const BITS = 160;
const bits = new THREE.InstancedMesh(new THREE.BoxGeometry(0.1, 0.1, 0.1), new THREE.MeshLambertMaterial(), BITS);
bits.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
for (let i = 0; i < BITS; i++) bits.setColorAt(i, colorOf("#ffffff"));
scene.add(bits);

// ------------------------------------------------------------------ title and THE END, in honey colours
const HONEY = ["#ffb81e", "#f6802a", "#ffd23e", "#e86a2a"];
const matLetter = new THREE.MeshLambertMaterial({ vertexColors: true, emissive: "#ffffff", emissiveIntensity: 0.12 });
const rowsOf = (rows) => rows.map((txt, r) => [...txt].map((ch, i) => {
  if (ch === " ") return null;
  const m = voxLetter(ch, HONEY[(i + r) % 4], 0.34, matLetter);
  scene.add(m);
  return m;
}));
const title = rowsOf(S.TITLE.rows), theEnd = rowsOf(["THE END"]);

// ------------------------------------------------------------------ notes, bubbles, the band
const lineEnd = (l) => l.t + Math.max(...l.notes.map(([d, , len]) => d + len));
const NOTES = [];
for (const l of S.LINES) if (!S.CAST[l.who].hidden && l.tag !== "title" && l.tag !== "end") for (const [d, n] of l.notes) NOTES.push({ t: l.t + d, who: l.who, m: S.midi(n) });
NOTES.sort((a, b) => a.t - b.t);
const notePool = [];
for (let i = 0; i < 40; i++) {
  const m = new THREE.Mesh(noteMesh(0), new THREE.MeshLambertMaterial({ vertexColors: true, transparent: true }));
  m.visible = false; scene.add(m); notePool.push(m);
}
const bubbles = bubbleSystem(scene, { midi: S.midi, lineEnd });
const hud = new THREE.Scene(), hudCam = new THREE.OrthographicCamera(0, W, H, 0, -1, 1);
const fadeMat = new THREE.MeshBasicMaterial({ color: "#000000", transparent: true, opacity: 0 });
const fader = new THREE.Mesh(new THREE.PlaneGeometry(W, H), fadeMat);
fader.position.set(W / 2, H / 2, 0.5);
hud.add(fader);
const band = bandSystem(hud, W, H);
const kickOf = (name, t) => { let k = 0; for (const e of NOTES) { if (e.t > t) break; if (e.who === name) k = Math.max(k, bump(t - e.t, 0.26)); } return k; };

// ------------------------------------------------------------------ the Bear's day
const BR = S.BRANCHES.map(([x, y]) => V3([x, y + 0.24, -4.85]));
const SKYP = V3(S.SKY);
function hop(a, b, u, h) { const p = new THREE.Vector3().lerpVectors(a, b, smooth(u)); p.y += Math.sin(clamp(u, 0, 1) * Math.PI) * h; return p; }
function bearPose(t) {
  let pos, rotY = 0, rotZ = 0, rotX = 0, sx = 1, sy = 1, mid = false, vis = true;
  const start = V3([16, 0, 4]), look = V3([3.4, 0, 0.6]), base = V3([5.4, 0, -4.6]);
  const hut = V3([-6.1, 0, -2.0]), edge = V3([-1.2, 0, 1.8]), rolled = V3([-4.4, 0, 1.8]), land = V3([2.0, 0, 0.2]);
  const air = (u) => { const p = new THREE.Vector3().lerpVectors(rolled, SKYP, smooth(u)); p.x += Math.sin(u * Math.PI * 3) * 0.6; return p; };
  if (t < S.WALK_IN[0]) return { vis: false };
  if (t < S.WALK_IN[1]) {
    const u = (t - S.WALK_IN[0]) / (S.WALK_IN[1] - S.WALK_IN[0]);
    pos = new THREE.Vector3().lerpVectors(start, look, smooth(u));
    pos.y += Math.abs(Math.sin(u * 7 * Math.PI)) * 0.14; rotZ = Math.sin(u * 7 * Math.PI) * 0.08; rotY = 0.4;
  } else if (t < 20.4) {
    pos = look.clone();
    rotX = -0.3 * ease(14.8, 15.4, t) * (1 - ease(19.4, 20.2, t));
    rotY = -0.5 * ease(14.8, 15.4, t);
    pos.y += bump(t - 18.2, 0.5) * 0.9;
  } else if (t < S.CLIMB[0]) {
    const u = (t - 20.4) / (S.CLIMB[0] - 20.4);
    pos = new THREE.Vector3().lerpVectors(look, base, smooth(u)); pos.y += Math.abs(Math.sin(u * 3 * Math.PI)) * 0.12;
  } else if (t < S.CRACK) {
    let i = 0;
    while (i < 4 && t >= S.CLIMB[i + 1]) i++;
    const from = i === 0 ? base : BR[i - 1], u = (t - S.CLIMB[i]) / 0.55;
    pos = u < 1 ? hop(from, BR[i], u, 1.0) : BR[i].clone();
    if (u >= 1) { const k = bump(u - 1, 0.5); sy *= 1 - 0.12 * k; sx *= 1 + 0.08 * k; }
    rotZ = (i % 2 ? -1 : 1) * 0.06;
    if (i === 4) { rotX = -0.25 * ease(S.CLIMB[4] + 0.6, S.CLIMB[4] + 1.0, t); pos.x += 0.4 * ease(S.CLIMB[4] + 0.6, S.CLIMB[4] + 1.2, t); }
  } else if (t < S.GORSE_AT) {                                 // down through the branches, tumbling
    const keys = [[S.CRACK + 0.2, V3([5.7, BR[4].y, -4.85])], ...S.BUMPS.map((b, i) => [b, BR[3 - i]]), [S.GORSE_AT, V3([S.GORSE[0], 0.2, S.GORSE[2]])]];
    if (t < keys[0][0]) pos = keys[0][1].clone();
    else {
      let i = 0;
      while (i < keys.length - 2 && t >= keys[i + 1][0]) i++;
      const u = clamp((t - keys[i][0]) / (keys[i + 1][0] - keys[i][0]), 0, 1);
      pos = new THREE.Vector3().lerpVectors(keys[i][1], keys[i + 1][1], u);
      pos.y += Math.sin(u * Math.PI) * 0.5 - u * u * 0.3;
    }
    rotZ = (t - S.CRACK) * 9; mid = true;
  } else if (t < 32.6) {                                       // in the gorse bush
    pos = V3([S.GORSE[0], -0.15 - 0.6 * bump(t - S.GORSE_AT, 0.5), S.GORSE[2] + 0.3]);
    rotZ = Math.sin(t * 30) * 0.12 * (1 - ease(32.0, 32.6, t)); mid = true;
  } else if (t < S.WALK_HOUSE[0]) {
    pos = hop(V3([S.GORSE[0], -0.15, S.GORSE[2] + 0.3]), V3([4.6, 0, -0.8]), (t - 32.6) / 0.5, 1.6);
    rotZ = Math.sin(t * 24) * 0.14 * ease(33.0, 33.1, t) * (1 - ease(33.8, 34.2, t));
  } else if (t < S.WALK_HOUSE[1]) {
    const u = (t - S.WALK_HOUSE[0]) / (S.WALK_HOUSE[1] - S.WALK_HOUSE[0]);
    pos = new THREE.Vector3().lerpVectors(V3([4.6, 0, -0.8]), hut, smooth(u));
    pos.y += Math.abs(Math.sin(u * 8 * Math.PI)) * 0.14; rotZ = Math.sin(u * 8 * Math.PI) * 0.08; rotY = -0.5;
  } else if (t < S.WALK_MUD[0]) {
    pos = hut.clone(); rotY = -0.35;
    for (let k = 0; k < 3; k++) pos.x -= bump(t - S.KNOCK - k * 0.24, 0.2) * 0.25;
    if (t > S.DOOR_OPEN + 0.6) rotY = -0.6;
  } else if (t < S.WALK_MUD[1]) {
    const u = (t - S.WALK_MUD[0]) / (S.WALK_MUD[1] - S.WALK_MUD[0]);
    pos = new THREE.Vector3().lerpVectors(hut, edge, smooth(u)); pos.y += Math.abs(Math.sin(u * 6 * Math.PI)) * 0.14; rotY = 0.4;
  } else if (t < S.ROLL[1]) {
    const u = clamp((t - S.ROLL[0]) / (S.ROLL[1] - S.ROLL[0]), 0, 1);
    pos = new THREE.Vector3().lerpVectors(edge, rolled, smooth(u)); pos.y -= 0.1 * Math.sin(u * Math.PI);
    rotZ = smooth(u) * Math.PI * 4; mid = true;
  } else if (t < S.RISE[0]) {
    pos = rolled.clone(); sy *= 1 + bump(t - 50.6, 0.4) * 0.1;
  } else if (t < S.RISE[1]) {
    pos = air((t - S.RISE[0]) / (S.RISE[1] - S.RISE[0]));
    rotZ = Math.sin(t * 1.6) * 0.08;
  } else if (t < S.FALL[0]) {
    pos = SKYP.clone(); pos.x += Math.sin(t * 0.9) * 0.3; pos.y += Math.sin(t * 1.3) * 0.15;
    rotZ = Math.sin(t * 0.9) * 0.08;
    const hit = bump(t - S.SHOTS[0] - 0.4, 0.5);               // ow!
    pos.y += hit * 0.5; rotZ += Math.sin(t * 40) * 0.2 * hit;
  } else if (t < S.FALL[1]) {                                  // down slowly, swaying like a leaf
    const u = (t - S.FALL[0]) / (S.FALL[1] - S.FALL[0]);
    pos = new THREE.Vector3().lerpVectors(SKYP, land, u * (0.6 + 0.4 * u));
    pos.x += Math.sin(u * Math.PI * 3) * 1.0 * (1 - u); rotZ = Math.sin(u * Math.PI * 3) * 0.25 * (1 - u);
  } else {
    pos = land.clone();
    const k = bump(t - S.FALL[1], 0.35); sy *= 1 - 0.2 * k; sx *= 1 + 0.12 * k;
    if (t > S.BLOW - 0.2) { const b = bump(t - S.BLOW, 0.5); sx *= 1 + 0.12 * b; sy *= 1 - 0.06 * b; rotX = 0.12 * b; }
  }
  const kick = kickOf("BEAR", t);
  if (!(t > S.RISE[0] && t < S.FALL[1])) pos.y += kick * 0.28;
  sy *= 1 + kick * 0.08 + Math.sin(t * 2.1) * 0.015;
  return { vis, pos, rotY, rotZ, rotX, sx, sy, mid };
}
function robinPose(t) {
  if (t < S.DOOR_OPEN + 0.2) return { vis: false };
  const out = V3([-9.0, 0, -2.6]), watch = V3([-6.4, 0, 3.0]), under = (x) => V3([x, 0, 2.2]), end = V3([-1.0, 0, 1.4]);
  let pos, rotY = 0.3, rotZ = 0, sy = 1, sx = 1;
  if (t < S.DOOR_OPEN + 1.0) pos = new THREE.Vector3().lerpVectors(V3([S.DOOR[0], 0, S.DOOR[2] - 0.3]), out, smooth((t - S.DOOR_OPEN - 0.2) / 0.8));
  else if (t < 46.2) pos = out.clone();
  else if (t < 48.4) { const u = (t - 46.2) / 2.2; pos = new THREE.Vector3().lerpVectors(out, watch, smooth(u)); pos.y += Math.abs(Math.sin(u * 6 * Math.PI)) * 0.12; }
  else if (t < S.UMBRELLA[0]) pos = watch.clone();
  else if (t < S.UMBRELLA[0] + 1.2) { const u = (t - S.UMBRELLA[0]) / 1.2; pos = new THREE.Vector3().lerpVectors(watch, under(-1.0), smooth(u)); pos.y += Math.abs(Math.sin(u * 4 * Math.PI)) * 0.12; }
  else if (t < S.GUN) {                                        // to and fro under the Bear, tut-tut
    const ph = (t - S.UMBRELLA[0] - 1.2) / 4.4 * Math.PI * 2;
    pos = under(-1.0 + Math.sin(ph) * 1.9); pos.y += Math.abs(Math.sin(ph * 3)) * 0.1;
    rotY = Math.cos(ph) > 0 ? 0.5 : -0.5;
  } else {                                                     // the shots; then out of the way as the Bear comes down
    const shotAt = under(-1.0 + Math.sin(((S.GUN - S.UMBRELLA[0] - 1.2) / 4.4) * Math.PI * 2) * 1.9), u = clamp((t - S.POP - 0.8) / 1.4, 0, 1);
    pos = new THREE.Vector3().lerpVectors(shotAt, end, smooth(u)); pos.y += Math.abs(Math.sin(u * 4 * Math.PI)) * 0.12 * (u < 1 ? 1 : 0);
    rotY = u > 0 && u < 1 ? -0.5 : 0.25;
  }
  const kick = kickOf("ROBIN", t);
  pos.y += kick * 0.26 + bump(t - 86.9, 0.5) * 0.8;
  sy *= 1 + kick * 0.08 + Math.sin(t * 2.3 + 1) * 0.015;
  return { vis: true, pos, rotY, rotZ, sx, sy };
}
const handOf = (pose) => {                                     // Robin's right hand (the picture's, turned with it)
  const p = pose.pos, a = pose.rotY || 0;
  return new THREE.Vector3(p.x + 0.62 * Math.cos(a), p.y + 0.78, p.z + 0.3 - 0.62 * Math.sin(a));
};
const place = (a, p) => {
  a.root.visible = p.vis;
  if (!p.vis) return;
  a.root.position.copy(p.pos);
  a.root.rotation.set(p.rotX || 0, p.rotY || 0, 0);
  a.body.rotation.set(0, 0, p.rotZ || 0);
  a.body.scale.set(p.sx || 1, p.sy || 1, ((p.sx || 1) + (p.sy || 1)) / 2);
  const hc = p.mid ? a.height / 2 : 0;
  a.body.position.set(Math.sin(p.rotZ || 0) * hc, hc - Math.cos(p.rotZ || 0) * hc, 0);
};

// ------------------------------------------------------------------ the camera
function camAt(t) {
  const K = S.CAM;
  let i = 0;
  while (i < K.length - 2 && t >= K[i + 1][0]) i++;
  const u = smooth((t - K[i][0]) / (K[i + 1][0] - K[i][0])), a = K[i], b = K[i + 1];
  return { p: new THREE.Vector3().lerpVectors(V3(a[1]), V3(b[1]), u), l: new THREE.Vector3().lerpVectors(V3(a[2]), V3(b[2]), u) };
}

// ------------------------------------------------------------------ one frame
const tmpM = new THREE.Matrix4(), tmpQ = new THREE.Quaternion(), tmpE = new THREE.Euler(), tmpV = new THREE.Vector3(), tmpS = new THREE.Vector3();
window.renderAt = (t) => {
  const c = camAt(t);
  camera.position.copy(c.p); camera.lookAt(c.l); camera.updateMatrixWorld();
  for (const cl of clouds) { const a = cl.a + t * 0.006; cl.m.position.set(Math.cos(a) * cl.r, cl.y, Math.sin(a) * cl.r - 20); }
  // the Bear (muddy after the roll) and Robin
  const bp = bearPose(t), rp = robinPose(t);
  if (!bp.vis) bp.pos = V3([16, 0, 4]);                         // (offstage: a place to be measured from)
  if (!rp.vis) rp.pos = V3([S.DOOR[0], 0, S.DOOR[2] - 0.5]);
  place(bear, bp); place(robin, rp);
  bear.g.visible = t < S.MUDDY; mud.g.visible = t >= S.MUDDY;
  // the breaking branch
  {
    const u = clamp((t - S.CRACK) / 1.6, 0, 1);
    breakable.position.set(S.TREE[0] - u * 0.8, -u * u * 12.2, S.TREE[2] + u * 1.2);
    breakable.rotation.set(0, 0, u * 1.4);
    breakable.visible = u < 1;
  }
  // the door opens for Robin
  door.rotation.y = -1.7 * ease(S.DOOR_OPEN - 0.2, S.DOOR_OPEN + 0.3, t);
  // balloons: two from behind Robin; the blue one goes to the Bear, the green one home again
  const rhand = rp.vis ? handOf(rp) : V3([-9, 0.8, -3]);
  const bearTop = bp.vis ? new THREE.Vector3(bp.pos.x, bp.pos.y + bear.height * (bp.sy || 1), bp.pos.z) : V3([0, 0, 0]);
  const showB = t > S.BALLOONS && t < S.POP;
  blueB.visible = blueS.visible = showB;
  greenB.visible = greenS.visible = t > S.BALLOONS && t < 48.4;
  if (showB) {
    const rise = backOut((t - S.BALLOONS) / 0.8), take = ease(S.TAKE, S.TAKE + 0.8, t);
    const hold = new THREE.Vector3().lerpVectors(rhand, bearTop, take);
    const bpos = hold.clone().add(new THREE.Vector3(0.7 * (1 - take) + Math.sin(t * 1.7) * 0.15, 2.0 + 0.6 * rise - take * 0.4, -0.2));
    bpos.x += bump(t - 44.0, 0.8) * 0.3;                          // (this one, please)
    blueB.position.copy(bpos);
    blueB.scale.setScalar(rise * (1 + bump(t - 44.0, 0.6) * 0.12));
    stretch(blueS, hold, bpos.clone().add(new THREE.Vector3(0, -1.3 * rise, 0)));
  }
  if (greenB.visible) {
    const home = ease(S.TAKE + 0.4, 48.4, t), hold = rhand.clone();
    const gpos = new THREE.Vector3().lerpVectors(hold.clone().add(new THREE.Vector3(-0.9 + Math.sin(t * 1.4) * 0.15, 2.5 * backOut((t - S.BALLOONS) / 0.8), -0.1)), V3([S.DOOR[0], 2.6, S.DOOR[2] - 0.8]), home);
    greenB.position.copy(gpos);
    greenB.scale.setScalar(backOut((t - S.BALLOONS) / 0.8) * (1 - 0.6 * home));
    stretch(greenS, home < 0.05 ? hold : gpos.clone().add(new THREE.Vector3(0, -1.4, 0)), gpos.clone().add(new THREE.Vector3(0, -1.3, 0)));
  }
  // the umbrella, open over Robin; then the popgun, pointing up at its target
  const um = t > S.UMBRELLA[0] && t < S.GUN && rp.vis;
  umbrella.visible = um;
  if (um) {
    const open = backOut((t - S.UMBRELLA[0]) / 0.6) * (1 - ease(S.GUN - 0.3, S.GUN, t));
    umbrella.position.copy(rhand).add(new THREE.Vector3(-0.1, 0.1, 0));
    umbrella.scale.set(open, 1, open);
    umbrella.rotation.set(0, t * 0.3, Math.sin(t * 2) * 0.08);
  }
  const gunOn = t > S.GUN && t < S.FALL[0] + 1.0 && rp.vis;
  gun.visible = gunOn;
  const target = (k) => (k === 0 ? new THREE.Vector3(bp.pos.x, bp.pos.y + bear.height * 0.55, bp.pos.z) : blueB.position.clone());
  if (gunOn) {
    const k = t < S.SHOTS[0] + 0.5 ? 0 : 1, aim = target(k).sub(rhand).normalize();
    gun.position.copy(rhand);
    gun.quaternion.setFromUnitVectors(new THREE.Vector3(1, 0, 0), aim);
    const recoil = bump(t - S.SHOTS[0], 0.25) + bump(t - S.SHOTS[1], 0.25);
    gun.position.addScaledVector(aim, -0.15 * recoil);
  }
  cork.visible = false;
  S.SHOTS.forEach((s, k) => {
    const u = (t - s) / 0.4;
    if (u < 0 || u > 1) return;
    cork.visible = true;
    cork.position.lerpVectors(rhand, target(k), u);
    cork.rotation.set(0, 0, t * 20);
  });
  // the Bee and the little bees: round their hole; out round the Bear; one on its nose
  const hole = V3(S.HOLE), nose = new THREE.Vector3(bp.pos.x, bp.pos.y + bear.height * 0.42, bp.pos.z + 0.75);
  const swarm = ease(S.SWARM[0], S.SWARM[0] + 1.0, t) * (1 - ease(S.SWARM[1] - 0.6, S.SWARM[1] + 0.6, t));
  bees.forEach((b, i) => {
    const a = t * (1.6 + (i % 4) * 0.3) + i * 1.7, r0 = 0.8 + (i % 3) * 0.35, r1 = 1.6 + (i % 4) * 0.25;
    const home = V3([hole.x + Math.cos(a) * r0, hole.y + Math.sin(a * 1.3) * 0.5, hole.z + 0.6 + Math.sin(a) * r0 * 0.6]);
    const round = V3([bp.pos.x + Math.cos(a) * r1, bp.pos.y + bear.height * 0.5 + Math.sin(a * 1.7) * 0.8, bp.pos.z + Math.sin(a) * r1]);
    b.visible = t > 13.8;
    b.position.lerpVectors(home, round, swarm);
    b.rotation.set(0, -a, Math.sin(t * 40 + i) * 0.2);
  });
  {
    let pos;
    const a = t * 1.3;
    const aroundHole = V3([hole.x + Math.cos(a) * 1.4, hole.y + 0.6 + Math.sin(a * 1.7) * 0.4, hole.z + 1.0]);
    if (t < 14.2) pos = V3([hole.x, hole.y, hole.z - 0.5]);
    else if (t < S.NOSE - 1.2) pos = new THREE.Vector3().lerpVectors(aroundHole, V3([bp.pos.x + Math.cos(a) * 1.6, bp.pos.y + 1.8, bp.pos.z + Math.sin(a) * 1.6]), swarm);
    else if (t < S.SHOTS[0] + 0.4) pos = new THREE.Vector3().lerpVectors(V3([bp.pos.x + 1.6, bp.pos.y + 2.2, bp.pos.z + 1]), nose, ease(S.NOSE - 1.2, S.NOSE, t));
    else pos = new THREE.Vector3().lerpVectors(nose, aroundHole, ease(S.SHOTS[0] + 0.4, S.SHOTS[0] + 2.0, t));
    place(bee, { vis: t > 14.2, pos, rotY: -0.3, rotZ: Math.sin(t * 9) * 0.1, sx: 1 + Math.sin(t * 50) * 0.06, sy: 1 + kickOf("BEE", t) * 0.15 });
  }
  // the butterfly: in, onto the Bear's nose, and off again when he blows
  {
    const bnose = new THREE.Vector3(bp.pos.x, bp.pos.y + bear.height * 0.42 - 0.5, bp.pos.z + 0.85);
    let pos;
    if (t < S.FLUTTER[1]) { const u = clamp((t - S.FLUTTER[0]) / (S.FLUTTER[1] - S.FLUTTER[0]), 0, 1); pos = new THREE.Vector3().lerpVectors(V3([-7, 4, 4]), bnose, smooth(u)); pos.y += Math.sin(u * Math.PI * 4) * 0.5 * (1 - u); }
    else if (t < S.BLOW + 0.1) pos = bnose;
    else { const u = (t - S.BLOW - 0.1) / 2.2; pos = new THREE.Vector3().lerpVectors(bnose, V3([7, 7, 2]), smooth(u)); pos.y += Math.sin(u * 12) * 0.3; }
    place(fly, { vis: t > S.FLUTTER[0] && t < S.BLOW + 2.4, pos, rotY: 0.2, sx: 0.55 + 0.45 * Math.abs(Math.sin(t * (t > S.FLUTTER[1] && t < S.BLOW ? 3 : 14))), sy: 1 });
  }
  // bits: mud from the roll, prickles from the gorse, balloon pieces, a puff of breath
  let bi = 0;
  const burst = (t0, n, seed, at, cols, up, out, life = 1.6) => {
    const age = t - t0;
    if (age < 0 || age > life) return;
    const R = rng(seed);
    for (let i = 0; i < n && bi < BITS; i++, bi++) {
      const a = R() * Math.PI * 2, vu = up * (0.5 + R()), vo = out * (0.4 + R());
      tmpV.set(at.x + Math.cos(a) * vo * age, at.y + vu * age - 4.9 * age * age, at.z + Math.sin(a) * vo * age);
      tmpE.set(age * 6 + i, age * 4, 0); tmpQ.setFromEuler(tmpE);
      tmpS.setScalar((1 - age / life) * (0.7 + R() * 0.8));
      tmpM.compose(tmpV, tmpQ, tmpS);
      bits.setMatrixAt(bi, tmpM);
      bits.setColorAt(bi, colorOf(cols[i % cols.length]));
    }
  };
  burst(S.GORSE_AT, 30, 1, V3([S.GORSE[0], 1.2, S.GORSE[2]]), ["#2f7d3c", "#ffd82e", "#1f5c2a"], 3.5, 2.2);
  burst(32.7, 16, 2, V3([S.GORSE[0] - 0.8, 0.8, S.GORSE[2] + 0.6]), ["#1f5c2a", "#ffd82e"], 2.5, 1.6);
  for (let k = 0; k < 4; k++) burst(S.ROLL[0] + 0.2 + k * 0.5, 12, 10 + k, V3([lerp(-1.2, -4.4, k / 3), 0.1, S.PUDDLE[2]]), ["#4a3a30", "#5e4a3c", "#3a2c24"], 3.0, 1.6, 1.1);
  burst(S.POP, 40, 3, blueB.position.clone(), ["#4a90ff", "#2f62c8", "#ffffff"], 2.5, 4.0, 1.4);
  burst(S.BLOW, 18, 4, V3([bp.pos.x - 0.2, bp.pos.y + bear.height * 0.35, bp.pos.z + 0.9]), ["#ffffff", "#eef4ff"], 0.6, 1.4, 0.9);
  bits.count = bi;
  bits.instanceMatrix.needsUpdate = true;
  if (bits.instanceColor) bits.instanceColor.needsUpdate = true;
  // notes floating up from whoever sings
  let pi = 0;
  for (const e of NOTES) {
    if (e.t > t) break;
    const age = t - e.t;
    if (age > 2 || pi >= notePool.length) continue;
    const a = who[e.who];
    if (!a.root.visible) continue;
    const m = notePool[pi++], p = a.root.position, side = (rng(Math.round(e.t * 1000))() - 0.5) * 1.6;
    m.geometry = noteMesh(e.m % 12); m.visible = true;
    m.position.set(p.x + side + Math.sin(age * 3 + side) * 0.3, p.y + a.height * 0.9 + age * 1.5, p.z + 0.4);
    m.rotation.set(0, Math.sin(age * 2) * 0.6, Math.sin(age * 4) * 0.2);
    m.scale.setScalar(backOut(age / 0.25));
    m.material.opacity = 1 - smooth((age - 1.3) / 0.7);
  }
  for (; pi < notePool.length; pi++) notePool[pi].visible = false;
  // the title, and THE END
  title.forEach((row, r) => row.forEach((m, i) => {
    if (!m) return;
    const n = row.length, idx = (r ? S.TITLE.rows[0].length : 0) + i, age = t - S.TITLE.t0 - idx * S.TITLE.step;
    const away = smooth((t - S.TITLE.out - idx * 0.02) / 1.2);
    m.visible = age > 0 && away < 1;
    if (!m.visible) return;
    m.position.set((i - (n - 1) / 2) * 2.2 - 1, (r ? 9.4 : 12.4) + Math.sin(t * 2 + idx) * 0.12 + away * 14, 1);
    m.rotation.set(0, Math.sin(t * 1.3 + idx * 0.6) * 0.16, 0);
    m.scale.setScalar(backOut(age / 0.45) * (1 + bump(age, 0.3) * 0.25));
  }));
  theEnd[0].forEach((m, i) => {
    if (!m) return;
    const age = t - S.THE_END - 0.2 - i * 0.15;
    m.visible = age > 0;
    if (!m.visible) return;
    m.position.set((i - 3) * 2.3 - 1, 10.6 + Math.sin(t * 1.6 + i) * 0.14, 1);
    m.rotation.set(0, Math.sin(t + i) * 0.15, 0);
    m.scale.setScalar(backOut(age / 0.5));
  });
  // speech bubbles over whoever sings
  const active = S.LINES.filter((l) => l.bubble && who[l.who].root.visible && t >= l.t - 0.1 && t < lineEnd(l) + 1.0);
  bubbles(t, active, (l) => {
    const a = who[l.who], o = { pos: a.root.position, height: a.height };
    if (l.who === "BEAR" && t > S.TAKE + 0.8 && t < S.POP) Object.assign(o, { dx: 2.3, dy: -a.height * 0.7 });   // (beside him: his balloon is above)
    if (l.who === "ROBIN" && t > S.UMBRELLA[0] && t < S.GUN) Object.assign(o, { dx: -2.0, dy: 0.4 });          // (beside the umbrella)
    return o;
  }, camera);
  renderer.clear();
  renderer.render(scene, camera);
  band(t, S.BANDS);
  fadeMat.opacity = Math.max(1 - smooth(t / 0.8), smooth((t - (S.DUR - 1.6)) / 1.4));
  fader.visible = fadeMat.opacity > 0.001;
  renderer.clearDepth();
  renderer.render(hud, hudCam);
};
window.ready = true;
