// What the Rainbow Island films share: voxels from pixel art, the toy's letters, its band, and the speech bubbles that
// show each note in the toy's colours. (world.js and halloween.js keep their own voxel code; their bubbles come from here.)
import * as THREE from "three";
import { FONT, OUTLINE } from "./pics.js";

export const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
export const lerp = (a, b, u) => a + (b - a) * u;
export const smooth = (u) => { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); };
export const ease = (a, b, t) => smooth((t - a) / (b - a));
export const backOut = (u) => { u = clamp(u, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
export const bump = (age, len) => (age < 0 || age > len ? 0 : Math.sin(Math.PI * age / len));
export function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
export const NOTE_COL = ["#ec2834", "#f65c28", "#ff8c1a", "#ffb81e", "#ffda24", "#82d638", "#46c46e", "#1eb096", "#4678d2", "#9254e2", "#c454d2", "#f256b0"];
export const NOTE_NAME = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
export const RAINBOW = ["#ec3440", "#ff8c1e", "#ffd82e", "#50c85a", "#3880f4", "#9658e2", "#ff78be"];

// ------------------------------------------------------------------ voxels to a mesh (only the faces that show)
const FACES = [
  [[1, 0, 0], [[1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 0, 1]]], [[-1, 0, 0], [[0, 0, 1], [0, 1, 1], [0, 1, 0], [0, 0, 0]]],
  [[0, 1, 0], [[0, 1, 1], [1, 1, 1], [1, 1, 0], [0, 1, 0]]], [[0, -1, 0], [[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1]]],
  [[0, 0, 1], [[1, 0, 1], [1, 1, 1], [0, 1, 1], [0, 0, 1]]], [[0, 0, -1], [[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]]],
];
export function voxGeometry(vox, size, ox = 0, oy = 0, oz = 0) {   // vox: Map "x,y,z" -> THREE.Color
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
export const colorOf = (() => { const cache = {}; return (h) => cache[h] || (cache[h] = new THREE.Color(h)); })();
// a pixel picture to plump voxels: each pixel a column through it, thicker the farther it is from the edge
export function plump(w, h, at, opt = {}) {
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

// ------------------------------------------------------------------ the toy's 5 x 7 letters, flat and in voxels
export function drawLetters(ctx, text, x, y, s, fill) {           // with a dark outline
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
export function voxLetter(ch, color, s, mat) {                    // one letter, outlined, standing on its baseline
  const w = 7, h = 9, px = new Array(w * h).fill(0), g = FONT[ch];
  if (g) for (let y = 0; y < 7; y++) for (let x = 0; x < 5; x++) if ((g[y] >> (4 - x)) & 1) px[(y + 1) * w + x + 1] = 1;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (px[y * w + x]) continue;
    for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++)
      if (y + dy >= 0 && y + dy < h && x + dx >= 0 && x + dx < w && px[(y + dy) * w + x + dx] === 1) px[y * w + x] = 2;
  }
  const sets = plump(w, h, (x, y) => (x < 0 || y < 0 || x >= w || y >= h ? null : px[y * w + x] === 1 ? color : px[y * w + x] === 2 ? OUTLINE : null), { max: 2, k: 1.4 });
  const m = new THREE.Mesh(voxGeometry(sets[0], s, -w * s / 2, 0, 0), mat);
  m.castShadow = true;
  return m;
}

// ------------------------------------------------------------------ speech bubbles: the notes, coloured, with their letters
// Laid out from the inside out: a column a note (its head, its stem, a flag on a short note, its letter under it), the
// columns' real reach, then the same padding on all four sides, so the notes sit in the middle of their bubble.
export const BUB = { W: 640, H: 300 };
const COLW = 90, RX = 23, RY = 16, STEM = 60, SPREAD = 44, PADX = 38, PADY = 30, LS = 8, B0 = 8;
function bubbleLayout(line, midi) {
  const shown = line.notes.slice(-6), n = shown.length;
  const half = (nn) => { const name = NOTE_NAME[midi(nn) % 12], ls = name.length > 1 ? 6 : LS; return ((name.length * 6 - 1) * ls) / 2 + 5; };
  const reachL = Math.max(RX + 4, half(shown[0][1]));             // the first column: its head, or its letter
  const reachR = line.tag === "oops" ? 34 : Math.max(shown[n - 1][2] < 0.3 ? 47 : 26, half(shown[n - 1][1]));   // the last: its flag, stem or letter
  const bw = 2 * PADX + (n - 1 + (line.tag === "oops" ? 1 : 0)) * COLW + reachL + reachR;   // (a wrong note: a column more, for a ?)
  const x0 = Math.round((BUB.W - bw) / 2);
  const cyHi = B0 + PADY + STEM, cyLo = cyHi + SPREAD;            // the highest note's stem meets the top padding
  const letters = cyLo + RY + 20;                                 // the letters' top, under the lowest head
  const y1 = letters + 7 * LS + PADY - 6;                         // (the letters' outline reaches a little lower)
  return { x0, x1: x0 + bw, y0: B0, y1, first: x0 + PADX + reachL, cyHi, cyLo, letters };
}
export function drawBubble(ctx, line, t, midi) {
  const L = bubbleLayout(line, midi), sung = line.notes.filter(([d]) => line.t + d <= t + 0.02);
  ctx.clearRect(0, 0, BUB.W, BUB.H);
  const { x0, x1, y0, y1 } = L, r = Math.min(46, (x1 - x0) / 2, (y1 - y0) / 2), tx = BUB.W / 2;
  ctx.beginPath();
  ctx.moveTo(x0 + r, y0); ctx.arcTo(x1, y0, x1, y1, r); ctx.arcTo(x1, y1, x0, y1, r);
  ctx.lineTo(tx + 16, y1); ctx.lineTo(tx - 22, BUB.H - 6); ctx.lineTo(tx - 16, y1);
  ctx.arcTo(x0, y1, x0, y0, r); ctx.arcTo(x0, y0, x1, y0, r); ctx.closePath();
  ctx.fillStyle = "#ffffff"; ctx.fill();
  ctx.lineWidth = 10; ctx.strokeStyle = OUTLINE; ctx.stroke();
  const all = line.notes.map(([, nn]) => midi(nn)), lo = Math.min(...all), hi = Math.max(...all);
  sung.slice(-6).forEach(([d, nn, len], i) => {
    const m = midi(nn), pc = m % 12, age = t - (line.t + d), pop = 1 + 0.45 * Math.exp(-age * 10);
    const cx = L.first + i * COLW, cy = hi > lo ? L.cyLo - ((m - lo) / (hi - lo)) * (L.cyLo - L.cyHi) : (L.cyHi + L.cyLo) / 2;
    ctx.save();
    ctx.translate(cx, cy); ctx.scale(pop, pop);
    ctx.save(); ctx.rotate(-0.35);
    ctx.beginPath(); ctx.ellipse(0, 0, RX, RY, 0, 0, Math.PI * 2);
    ctx.fillStyle = NOTE_COL[pc]; ctx.fill(); ctx.lineWidth = 5; ctx.strokeStyle = OUTLINE; ctx.stroke();
    ctx.restore();
    ctx.fillStyle = OUTLINE;
    ctx.fillRect(RX - 6, -STEM, 6, STEM - 2);
    if (len < 0.3) {
      ctx.beginPath(); ctx.moveTo(RX, -STEM); ctx.quadraticCurveTo(RX + 22, -STEM + 18, RX + 18, -STEM + 38);
      ctx.lineWidth = 6; ctx.strokeStyle = OUTLINE; ctx.stroke();
    }
    ctx.restore();
    const name = NOTE_NAME[pc], ls = name.length > 1 ? 6 : LS;
    drawLetters(ctx, name, cx - ((name.length * 6 - 1) * ls) / 2, L.letters, ls, NOTE_COL[pc]);
  });
  if (line.tag === "oops" && sung.length === line.notes.length && t > line.t + line.notes[line.notes.length - 1][0] + 0.3)
    drawLetters(ctx, "?", L.first + Math.min(6, line.notes.length) * COLW - 18, (L.cyHi + L.cyLo) / 2 - 40, 9, "#ff5470");
}
// the bubbles in the scene: one sprite each, placed over the singer's head, sized so it reads from where the camera is
export function bubbleSystem(scene, { midi, lineEnd, max = 6 }) {
  const list = [];
  for (let i = 0; i < max; i++) {
    const cv = document.createElement("canvas");
    cv.width = BUB.W; cv.height = BUB.H;
    const tex = new THREE.CanvasTexture(cv);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.minFilter = THREE.LinearFilter;
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false, fog: false }));
    sp.renderOrder = 10;
    sp.visible = false;
    scene.add(sp);
    list.push({ ctx: cv.getContext("2d"), tex, sp });
  }
  // active: the lines showing; where(line): the singer's position and height (and dx, dy: the bubble moved aside, so it
  // does not hide what the singer holds); camera: for the size
  return (t, active, where, camera) => list.forEach((b, i) => {
    const l = active[i];
    b.sp.visible = !!l;
    if (!l) return;
    const { pos: p, height, dx = 0, dy = 0 } = where(l), n = active.length;
    const age = t - (l.t - 0.1), out = lineEnd(l) + 1.0 - t;
    const far = clamp(camera.position.distanceTo(p) / 13, 1, 2.1);
    const s = Math.min(backOut(age / 0.3), smooth(out / 0.25)) * (n > 2 ? 0.8 : 1) * far;
    drawBubble(b.ctx, l, t, midi);
    b.tex.needsUpdate = true;
    const w = 4.16 * s, h = w * BUB.H / BUB.W;
    b.sp.position.set(p.x + 0.6 + dx * far, p.y + height + h / 2 + 0.2 + dy + (n > 2 ? (i % 2) * 0.9 * far : 0), p.z + 0.5);
    b.sp.scale.set(w, h, 1);
  });
}

// ------------------------------------------------------------------ the toy's band at the bottom: a word, sliding up
export function bandSystem(hud, W, H) {
  const cv = document.createElement("canvas");
  cv.width = W; cv.height = Math.round(H * 0.13);
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace;
  const band = new THREE.Mesh(new THREE.PlaneGeometry(W, cv.height), new THREE.MeshBasicMaterial({ map: tex, transparent: true }));
  hud.add(band);
  let drawn = "";
  return (t, BANDS) => {
    const cur = BANDS.filter((b) => t >= b.t && t < b.t + b.len).pop();
    if (!cur) { band.visible = false; return; }
    const age = t - cur.t, rest = cur.t + cur.len - t, h = cv.height;
    band.visible = true;
    band.position.set(W / 2, h / 2 - h * (1 - Math.min(backOut(age / 0.35), smooth(rest / 0.3))), 0);
    const key = cur.text + cur.col[0];
    if (drawn !== key) {
      const ctx = cv.getContext("2d");
      ctx.fillStyle = cur.col[0]; ctx.fillRect(0, 0, W, h);
      ctx.fillStyle = cur.col[1]; ctx.fillRect(0, h - h * 0.16, W, h * 0.16);
      ctx.fillStyle = OUTLINE; ctx.fillRect(0, 0, W, Math.max(4, h * 0.04));
      const s = Math.max(4, Math.min(Math.floor(h * 0.1), Math.floor((W * 0.92) / (cur.text.length * 6)))), tw = (cur.text.length * 6 - 1) * s;
      drawLetters(ctx, cur.text, (W - tw) / 2, (h * 0.84 - 7 * s) / 2 + h * 0.03, s, "#ffffff");
      tex.needsUpdate = true;
      drawn = key;
    }
  };
}

// ------------------------------------------------------------------ voxel eighth notes that float up from a singer
const NOTE_GLYPH = ["...11", "...111", "...1.1", "...1..", "...1..", ".111..", "1111..", ".11..."];
const noteGeo = {};
export const noteMesh = (pc) => {
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
