// Rainbow mode, a fresh tour: raw RGB frames (30 fps), a WAV, captions, and the keys held on each frame.
//   node tools/video/record_tour.mjs build/emu/felucca.wasm OUT_DIR   then compose_tour.py in OUT_DIR
// Everything is played on the browser build, as a child would: the games are won by pressing the keys they light, and the
// stars are set just short of a secret first, so the win on screen is the one that opens it.
import fs from "fs";
const [wasmPath, out] = process.argv.slice(2);
const B = { FX: 0, SCL: 1, ENV: 2, LFO: 3, EDIT: 4, GLO: 5, HOME: 6, SAVE: 7, ARP: 8, SEQ: 9, PLAY: 10, REC: 11, OCTDN: 12, OCTUP: 13 };
const EN = { SELECT: 0, ALGO: 1, PRESETS: 2, K1: 3, K2: 4, K3: 5, K4: 6 };
const K = { F3: 0, G3: 2, A3: 4, B3: 6, C: 7, D: 9, E: 11, F: 12, G: 14, A: 16, B: 18, C2: 19, D2: 21, E2: 23, F2: 24, G2: 26 };
const NF = 94;                                                     // the friends on PRESETS (the secret one waits for 50 stars)
const FR = { COW: 76, SHARK: 79, TRICERATOPS: 85, FIRE_TRUCK: 91, PIANO_PAL: 73, SAX_CAT: 75, SCIENTIST: 58, KING_AXOLOTL: 66,
             DRAGON_DUCK: 62, HELICOPTER: 93, BUNNY: 24, SNAIL: 82 };
const BEAT = { LOFI: 11, ACID: 12, BREAK: 20 }, SKY = { STREET: 10, SEA: 11, RAIN: 12, FIREWORKS: 13 };
const { instance } = await WebAssembly.instantiate(fs.readFileSync(wasmPath), {});
const ex = instance.exports, mem = ex.memory;
ex._initialize(); ex.web_nor_erase(); ex.web_boot(); ex.web_master(1023);
let keysNow = 0, now = 0;
const setKeys = (m) => { keysNow = m; ex.web_keys(m); };
const ev = [], watchers = [], cap = [];
const at = (t, f) => ev.push([t, f]);
const C = (t, a, b) => cap.push([t, a, b]);
const note = (t, k, len) => { at(t, () => setKeys(1 << k)); at(t + len, () => setKeys(0)); };
const hold = (t, keys, len) => { at(t, () => setKeys(keys.reduce((a, k) => a | (1 << k), 0))); at(t + len, () => setKeys(0)); };
const tap = (t, b) => { at(t, () => ex.web_buttons(1 << b)); at(t + 80, () => ex.web_buttons(0)); };
const turn = (t, r, n, gap = 120) => { for (let i = 0; i < Math.abs(n); i++) at(t + i * gap, () => ex.web_enc(r, Math.sign(n))); };
const tune = (t, keys, step) => keys.forEach((k, i) => k !== null && note(t + i * step, k, step - 60));
const watch = (t, f) => at(t, () => watchers.push(f));             // f(ms) each frame from t until it returns true
let navTo = null;
const go = (t, f) => at(t, () => { navTo = f; });
// a button tapped every 350 ms until get() reads the wanted value (a beat on SEQ, a sky on REC)
const seek = (t, b, get, want) => { let next = 0; watch(t, (ms) => {
  if (get() === want) { ex.web_buttons(0); return true; }
  if (ms >= next) { ex.web_buttons(1 << b); next = ms + 350; } else if (ms >= next - 270) ex.web_buttons(0);
  return false; }); };
// CHORDS: each lit chord, pressed a beat after it lights, n times
const chords = (t, n, wait = 650, len = 650) => { let done = 0, lit = 0, since = 0, until = 0; watch(t, (ms) => {
  if (until) { if (ms < until) return false; setKeys(0); until = 0; done++; lit = 0; return done >= n; }
  const m = ex.web_lit_keys() & 0x7FFFFFF;
  if (m !== lit) { lit = m; since = ms; }
  if (m && ms - since >= wait) { setKeys(m); until = ms + len; }
  return false; }); };
// COPY ME: each round, the friend's pattern played back on YOUR TURN, n rounds
const copyMe = (t, n, step = 420) => { let done = 0, busy = false; watch(t, (ms) => {
  if (busy) return false;
  if (ex.web_kid_copy_state() !== 2) return done >= n;
  const ks = [...Array(ex.web_kid_copy_len()).keys()].map((i) => ex.web_kid_copy_key(i));
  busy = true;
  ks.forEach((k, i) => note(ms + 450 + i * step, k, step - 120));
  at(ms + 450 + ks.length * step + 200, () => { busy = false; done++; });
  return false; }); };
const Q = 500;                                                     // a beat at 120 BPM

// FOLLOW: the lit key pressed, n times, a step apart
const follow = (t, n, step) => { let done = 0, next = 0; watch(t, (ms) => {
  if (ms < next) return false;
  const lit = ex.web_lit_keys() & 0x7FFFFFF;
  if (lit) { const k = 31 - Math.clz32(lit & -lit); note(ms, k, step - 90); done++; }
  next = ms + step; return done >= n; }); };

// cold open: a tune, straight away
go(0, FR.KING_AXOLOTL);
C(0, "Rainbow mode", "a free music toy for little hands, on the M-VAVE FM-1");
tune(700, [K.E, K.E, K.F, K.G, K.G, K.F, K.E, K.D, K.C, K.C, K.D, K.E, K.E, K.D, K.D], 290);
// 1. hats that fit, then the friends in them
let t = 5400;
C(t, "1. A hat for every friend", "for grown-ups: hold HOME, then turn KNOB 4");
at(t, () => ex.web_buttons(1 << B.HOME));
[0, 1, 2, 3].forEach((i) => turn(t + 1300 + i * 700, EN.K4, 1));
at(t + 1300 + 4 * 700, () => ex.web_buttons(0));
t += 4900;
const FRS = [[FR.BUNNY, "it sits on the head, not the ears", (s) => tune(s, [K.C, K.E, K.G, K.E], 280)],
             [FR.SNAIL, "the snail's head is its eyes", (s) => tune(s, [K.E, K.D, K.C], 360)],
             [FR.SHARK, "a shark wears it at the front", (s) => tune(s, [K.E, K.F, K.E, K.F, K.E, K.F], 180)],
             [FR.FIRE_TRUCK, "a fire truck wears it on the roof", (s) => { note(s, K.C, 450); note(s + 500, K.G, 450); }],
             [FR.COW, "94 friends, each one fitted", (s) => tune(s, [K.G, K.E, K.C, K.E], 280)]];
FRS.forEach(([f, sub, play]) => { go(t, f); C(t, "1. A hat for every friend", sub); play(t + 400); t += 1800; });
// 2. 3 FRIENDS: a major chord on every key, and the card that says so
go(t, FR.PIANO_PAL);
turn(t + 200, EN.ALGO, 1);
C(t, "2. Magic chords", "turn ALGORITHM and a card says how the keys play");
t += 2800;
C(t, "2. Magic chords", "every key is a major chord now, black keys too");
hold(t + 200, [K.C], 600); hold(t + 900, [K.E], 700);
C(t + 1800, "2. Magic chords", "try C, then G#, A# and back to C");
hold(t + 2000, [K.C], 500); hold(t + 2600, [15], 500); hold(t + 3200, [17], 500); hold(t + 3800, [K.C2], 1100);
t += 5400;
// 3. a beat under it
tap(t, B.PLAY);
seek(t + 300, B.SEQ, () => ex.web_kid_beat(), BEAT.LOFI);
C(t, "3. 21 beats", "PLAY for a beat, SEQ for the next one");
hold(t + 1000, [K.C], 900); hold(t + 2000, [K.A], 900); hold(t + 3000, [K.F], 900); hold(t + 4000, [K.G], 900);
tap(t + 5200, B.PLAY);
t += 5600;
// 4. FOLLOW: 24 songs now
turn(t, EN.ALGO, 4, 80);
C(t, "4. FOLLOW: songs to learn", "the next key lights up. Take your time");
for (let i = 0; i < 18; i++) tap(t + 2800 + i * 120, B.SEQ);      // (to the new ones: WHEN THE SAINTS)
C(t + 2800, "4. FOLLOW: songs to learn", "24 songs now, like When the Saints");
follow(t + 5400, 16, 330);
t += 11200;
// 5. COPY ME, and a secret sky at 25 stars
turn(t, EN.ALGO, 2);
at(t, () => ex.web_kid_stars_set(24));
C(t, "5. COPY ME", "listen to the friend, then play it back");
copyMe(t + 2400, 1);
C(t + 7200, "5. COPY ME", "every game won is a star. 25: a secret sky");
t += 9800;
// 6. DO RE MI
turn(t, EN.ALGO, -7, 80);
C(t, "6. DO RE MI", "for grown-ups: hold HOME, then turn KNOB 2");
at(t + 600, () => ex.web_buttons(1 << B.HOME));
turn(t + 1900, EN.K2, 1);
at(t + 2600, () => ex.web_buttons(0));
C(t + 3400, "6. DO RE MI", "the note names many countries learn first");
tune(t + 3600, [K.C, K.D, K.E, K.F, K.G, K.A, K.B, K.C2], 330);
hold(t + 6400, [K.C, K.E, K.G], 1200);
t += 8200;
// 7. WRITE, loop and layer
go(t, FR.DRAGON_DUCK);
tap(t + 800, B.SAVE);
C(t, "7. Write a song", "SAVE, then PLAY a loop and play into it");
tap(t + 1500, B.PLAY);
tune(t + 1900, [K.C, null, K.E, null, K.G, null, K.E, null], 500);
turn(t + 6000, EN.PRESETS, 1);
C(t + 6000, "7. Write a song", "PRESETS: another friend for the next layer");
tune(t + 6300, [null, K.C2, null, K.B, null, K.G, null, K.A], 500);
t += 11000;
tap(t, B.PLAY); tap(t + 300, B.SAVE);
// the summary, over a beat
go(t + 400, FR.HELICOPTER);
tap(t + 1100, B.PLAY);
C(t, "New since the last video", "__LIST__");
const items = 8, gap = 1450;
tune(t + 1400, [K.C, null, K.E, null, K.F, null, K.G, null, K.A, null, K.G, null, K.E, null, K.C, null, K.D, null, K.E, null, K.C], 400);
t += 1000 + items * gap + 1800;
C(t, "What should we add next?", "__END__");
tune(t + 300, [K.E, K.G, K.C2, null, K.G, K.C2], 330);
tap(t + 3600, B.PLAY);
const END = t + 5200;

ev.sort((a, b) => a[0] - b[0]);
const FPS = 30, SPF = 1470, frames = Math.ceil(END / 1000 * FPS);
const raw = fs.openSync(`${out}/frames.rgb`, "w"), pcm = [], keys = [];
let e = 0, sorted = ev.length;
for (let f = 0; f < frames; f++) {
  now = f * 1000 / FPS;
  if (ev.length !== sorted) { const rest = ev.splice(e).sort((a, b) => a[0] - b[0]); ev.push(...rest); sorted = ev.length; }
  while (e < ev.length && ev[e][0] <= now) { ev[e++][1](); if (ev.length !== sorted) { const rest = ev.splice(e).sort((a, b) => a[0] - b[0]); ev.push(...rest); sorted = ev.length; } }
  for (let i = watchers.length - 1; i >= 0; i--) if (watchers[i](now)) watchers.splice(i, 1);
  if (navTo !== null) {                                            // (straight there, as if PRESETS had turned)
    if (ex.web_kid_friend() !== navTo) ex.web_kid_friend_set(navTo);
    navTo = null;
  }
  for (let k = 0; k < SPF; k += 147) {
    ex.web_render(147);
    const l = new Float32Array(mem.buffer, ex.web_out_l(), 147), r = new Float32Array(mem.buffer, ex.web_out_r(), 147);
    for (let i = 0; i < 147; i++) pcm.push(l[i], r[i]);
  }
  keys.push([keysNow, ex.web_lit_keys()]);
  const fb = new Uint16Array(mem.buffer, ex.web_screen(), 240 * 240), b = Buffer.alloc(240 * 240 * 3);
  for (let i = 0; i < fb.length; i++) {
    const v = ((fb[i] & 255) << 8) | (fb[i] >> 8);
    b[i * 3] = ((v >> 11) << 3) | (v >> 13); b[i * 3 + 1] = (((v >> 5) & 63) << 2) | ((v >> 9) & 3); b[i * 3 + 2] = ((v & 31) << 3) | ((v >> 2) & 7);
  }
  fs.writeSync(raw, b);
}
fs.closeSync(raw);
let pk = 0; for (const v of pcm) pk = Math.max(pk, Math.abs(v));
const g = 0.89 / pk, wav = Buffer.alloc(44 + pcm.length * 2);
wav.write("RIFF", 0); wav.writeUInt32LE(36 + pcm.length * 2, 4); wav.write("WAVEfmt ", 8); wav.writeUInt32LE(16, 16);
wav.writeUInt16LE(1, 20); wav.writeUInt16LE(2, 22); wav.writeUInt32LE(44100, 24); wav.writeUInt32LE(44100 * 4, 28);
wav.writeUInt16LE(4, 32); wav.writeUInt16LE(16, 34); wav.write("data", 36); wav.writeUInt32LE(pcm.length * 2, 40);
pcm.forEach((v, i) => wav.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(v * g * 32767))), 44 + i * 2));
fs.writeFileSync(`${out}/audio.wav`, wav);
fs.writeFileSync(`${out}/captions.json`, JSON.stringify({ fps: FPS, frames, captions: cap, keys, list_gap: gap }));
console.log(`frames ${frames}, audio ${(pcm.length / 2 / 44100).toFixed(1)} s, peak ${pk.toFixed(3)} (gain ${g.toFixed(2)})`);
console.log(`stars ${ex.web_kid_stars()}, hat ${ex.web_kid_hat()}, scene ${ex.web_kid_scene()}, friend ${ex.web_kid_friend()}`);
