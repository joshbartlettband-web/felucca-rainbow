// The soundtrack, from the real thing: each line of script.mjs is played on the friend's own sound by Rainbow mode
// itself (the firmware's browser build, felucca.wasm), one fresh toy per line, and mixed at its time. The party's
// beat is the toy's own beat (PLAY with the episode's BEAT_FRIEND: Ducky's DANCE, or Ghost's SPOOKY). Writes a 44.1 kHz
// stereo WAV.
//   node audio.mjs felucca.wasm out.wav [script.mjs | halloween.mjs]
import fs from "fs";
import path from "path";
import { pathToFileURL } from "url";
const EP = await import(pathToFileURL(path.resolve(process.argv[4] || new URL("./script.mjs", import.meta.url).pathname)).href);
const { LINES, PARTY, DUR, midi, CAST } = EP;

const SR = 44100;
const B = { HOME: 6, PLAY: 10, OCTDN: 12, OCTUP: 13 };
const mod = await WebAssembly.compile(fs.readFileSync(process.argv[2] || "felucca.wasm"));

async function toy() {
  const inst = await WebAssembly.instantiate(mod, {});
  const ex = inst.exports, mem = ex.memory;
  ex._initialize();
  ex.web_nor_erase();
  ex.web_boot();
  ex.web_master(1023);
  let rec = null;
  const render = (sec) => {
    let n = Math.round(sec * SR);
    while (n > 0) {
      const m = Math.min(128, n);
      ex.web_render(m);
      if (rec) {
        const l = new Float32Array(mem.buffer, ex.web_out_l(), m), r = new Float32Array(mem.buffer, ex.web_out_r(), m);
        for (let i = 0; i < m; i++) { rec.l.push(l[i]); rec.r.push(r[i]); }
      }
      n -= m;
    }
  };
  render(5);                                   // the hello, and the first friend
  return { ex, render, start: () => { rec = { l: [], r: [] }; }, take: () => rec };
}

// one line: the friend, its octave, and its notes as key presses (a key's note: kb_map's 53 + k)
async function sing(line) {
  const t = await toy();
  t.ex.web_kid_friend_set(CASTFR[line.who]);
  t.render(2.5);                               // (its arrival: the band and the sky settle)
  for (let i = 0; i < Math.abs(line.oct); i++) {
    t.ex.web_buttons(1 << (line.oct < 0 ? B.OCTDN : B.OCTUP)); t.render(0.1); t.ex.web_buttons(0); t.render(0.2);
  }
  t.render(1.6);                               // (the octave's word goes)
  // key changes: a note down at its start, up a little before its end (a key pressed again needs a frame up)
  const ev = [];
  for (const [d, n, len] of line.notes) {
    const k = midi(n) - 53;
    if (k < 0 || k > 26) throw new Error(`${line.who}: ${n} is off the keys`);
    ev.push([d, k, 1], [d + Math.max(0.06, len - 0.035), k, 0]);
  }
  ev.sort((a, b) => a[0] - b[0] || a[2] - b[2]);
  const PRE = 0.0075;                          // keys are read every 15 ms: press half a frame early
  t.start();
  let now = 0, mask = 0;
  for (const [at, k, on] of ev) {
    const when = Math.max(0, at + 0.2 - PRE);  // (the recording starts 0.2 s before the first note)
    if (when > now) { t.render(when - now); now = when; }
    mask = on ? mask | (1 << k) : mask & ~(1 << k);
    t.ex.web_keys(mask);
  }
  t.render(3.0);                               // the tail: echoes and releases
  t.ex.web_keys(0);
  const r = t.take();
  return { at: line.t - 0.2, l: r.l, r: r.r };
}

// the beat: PLAY on the beat's friend (its favourite beat), recorded, then lined up on its first hit
async function beat() {
  const t = await toy();
  t.ex.web_kid_friend_set(CASTFR[EP.BEAT_FRIEND || "DUCKY"]);
  t.render(2.5);
  t.start();
  t.render(0.3);
  t.ex.web_buttons(1 << B.PLAY); t.render(0.1); t.ex.web_buttons(0);
  const len = PARTY.t1 - PARTY.t0;
  t.render(len + 1.0);
  const r = t.take();
  let first = 0;
  while (first < r.l.length && Math.abs(r.l[first]) < 0.02 && Math.abs(r.r[first]) < 0.02) first++;
  // a little before the hit's peak: the first sample over 2 %, minus 3 ms (its attack)
  first = Math.max(0, first - Math.round(0.003 * SR));
  const keep = Math.round((len + 0.45) * SR);
  const l = r.l.slice(first, first + keep), rr = r.r.slice(first, first + keep);
  const fade = Math.round(0.4 * SR);           // the last downbeat rings 0.45 s, then a fade
  for (let i = 0; i < fade; i++) { const g = 1 - i / fade; l[keep - fade + i] *= g; rr[keep - fade + i] *= g; }
  return { at: PARTY.t0, l, r: rr };
}

const CASTFR = Object.fromEntries(Object.entries(CAST).map(([k, v]) => [k, v.fr]));
const stems = [];
for (const line of LINES) {
  stems.push(await sing(line));
  process.stdout.write(".");
}
stems.push(await beat());
console.log(`\n${stems.length} stems`);

// each line to about the same loudness (its loudest 50 ms), the beat a little under the voices
const loud = (s) => {
  const w = Math.round(0.05 * SR);
  let best = 0;
  for (let i = 0; i + w <= s.l.length; i += w >> 1) {
    let e = 0;
    for (let j = i; j < i + w; j++) e += s.l[j] * s.l[j] + s.r[j] * s.r[j];
    best = Math.max(best, Math.sqrt(e / (2 * w)));
  }
  return best;
};
const lv = LINES.map((l) => l.tag);
stems.forEach((s, i) => {
  const tag = i < LINES.length ? lv[i] : "beat";
  const group = ["giggle", "together", "ooh", "all", "end", "trick", "boo", "eek"];
  const want = tag === "beat" ? 0.075 : tag === "bed" ? 0.022 : group.includes(tag) ? 0.07 : 0.1;
  const g = Math.max(0.4, Math.min(5, want / Math.max(1e-4, loud(s))));
  for (let j = 0; j < s.l.length; j++) { s.l[j] *= g; s.r[j] *= g; }
});

// mix, with a gentle limit, to 16-bit WAV
const N = Math.round(DUR * SR), L = new Float32Array(N), R = new Float32Array(N);
for (const s of stems) {
  const o = Math.round(s.at * SR);
  for (let i = 0; i < s.l.length; i++) {
    const j = o + i;
    if (j >= 0 && j < N) { L[j] += s.l[i]; R[j] += s.r[i]; }
  }
}
let peak = 0;
for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
const g = 0.6 / peak;                          // then a soft knee: loud enough, never clipped
const soft = (x) => { x *= g; const a = Math.abs(x); return a < 0.6 ? x : Math.sign(x) * (0.6 + 0.35 * Math.tanh((a - 0.6) / 0.35)); };
const buf = Buffer.alloc(44 + N * 4);
buf.write("RIFF", 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write("WAVEfmt ", 8);
buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22); buf.writeUInt32LE(SR, 24);
buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34); buf.write("data", 36); buf.writeUInt32LE(N * 4, 40);
for (let i = 0; i < N; i++) {
  buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, soft(L[i]))) * 32767), 44 + i * 4);
  buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, soft(R[i]))) * 32767), 46 + i * 4);
}
fs.writeFileSync(process.argv[3] || "soundtrack.wav", buf);
console.log(`peak before the mix's gain ${peak.toFixed(3)}, gain ${g.toFixed(2)}`);
