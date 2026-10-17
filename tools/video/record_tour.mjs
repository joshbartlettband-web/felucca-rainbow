// Rainbow mode, a fresh tour: raw RGB frames (30 fps), a WAV, captions, and the keys held on each frame.
//   node tools/video/record_tour.mjs build/emu/felucca.wasm OUT_DIR   then compose_tour.py in OUT_DIR
//   (build/emu/felucca.wasm: web/emu/build.sh with Emscripten, or tools/video/build_wasm_clang.sh without; or run the tour-video workflow on GitHub)
import fs from "fs";
const [wasmPath, out] = process.argv.slice(2);
const B = { FX: 0, SCL: 1, ENV: 2, LFO: 3, EDIT: 4, GLO: 5, HOME: 6, SAVE: 7, ARP: 8, SEQ: 9, PLAY: 10, REC: 11, OCTDN: 12, OCTUP: 13 };
const EN = { SELECT: 0, ALGO: 1, PRESETS: 2, K1: 3, K2: 4, K3: 5, K4: 6 };
const K = { F3: 0, G3: 2, A3: 4, B3: 6, C: 7, D: 9, E: 11, F: 12, G: 14, A: 16, B: 18, C2: 19, D2: 21, E2: 23, F2: 24, G2: 26 };
const { instance } = await WebAssembly.instantiate(fs.readFileSync(wasmPath), {});
const ex = instance.exports, mem = ex.memory;
ex._initialize(); ex.web_nor_erase(); ex.web_boot(); ex.web_master(1023);
let keysNow = 0;
const setKeys = (m) => { keysNow = m; ex.web_keys(m); };
const ev = [], cap = [];
const at = (t, f) => ev.push([t, f]);
const C = (t, a, b) => cap.push([t, a, b]);
const note = (t, k, len) => { at(t, () => setKeys(1 << k)); at(t + len, () => setKeys(0)); };
const hold = (t, keys, len) => { at(t, () => setKeys(keys.reduce((a, k) => a | (1 << k), 0))); at(t + len, () => setKeys(0)); };
const tap = (t, b) => { at(t, () => ex.web_buttons(1 << b)); at(t + 80, () => ex.web_buttons(0)); };
const turn = (t, r, n, gap = 120) => { for (let i = 0; i < Math.abs(n); i++) at(t + i * gap, () => ex.web_enc(r, Math.sign(n))); };
const tune = (t, keys, step) => keys.forEach((k, i) => k !== null && note(t + i * step, k, step - 60));
let navTo = null, seqTo = null, copying = false, copyBusy = 0;
const go = (t, f) => at(t, () => { navTo = f; });
const Q = 500;                                                     // a beat at 120 BPM

// cold open: a tune, straight away
go(0, 4);                                                          // UNICORN
C(0, "Rainbow mode", "a free music toy for little hands, on the M-VAVE FM-1");
tune(700, [K.E, K.E, K.F, K.G, K.G, K.F, K.E, K.D, K.C, K.C, K.D, K.E, K.E, K.D, K.D], 290);
// 1. see the music
let t = 5400;
C(t, "1. See the music", "every note has its color, and the staff writes it down");
[[K.C, 1], [K.E, 1], [K.G, 1], [K.E, 1], [K.C2, 2], [K.G, 2]].reduce((s, [k, b]) => { note(s, k, Q * b * 0.95 - 10); return s + Q * b; }, t + 300);
C(t + 2900, "1. See the music", "long notes look long, and every four beats a barline");
t += 6600;
// 2. the friends, the newer ones, each in its home sky
const slide = (s, ks, step) => ks.forEach((k, i) => {                // a 303 slide: each key held over the next
  at(s + i * step, () => setKeys((1 << k) | (i ? 1 << ks[i - 1] : 0)));
  at(s + i * step + 70, () => setKeys(1 << k));
  if (i === ks.length - 1) at(s + (i + 1) * step, () => setKeys(0));
});
const FR = [[17, "new skies: Frog's home is the rain now", (s) => tune(s, [K.C, K.E, K.G, K.E], 260)],
            [37, "and Rocket's is fireworks", (s) => tune(s, [K.G, K.C2, K.E2, K.G2], 260)],
            [58, "Scientist: an acid bass that slides like a 303", (s) => slide(s, [K.A3, K.C, K.A3, K.E, K.D], 240)],
            [73, "Piano Pal plays a real recorded piano", (s) => { tune(s, [K.E, K.G, K.C2], 230); hold(s + 700, [K.C, K.E, K.G], 700); }],
            [76, "friends in sets: the farm, the sea, bugs, food", (s) => tune(s, [K.C, K.G3, K.C], 420)],
            [79, "Shark: a deep bass, under the sea", (s) => tune(s, [K.C, null, K.C, K.G3, K.A3, K.B3], 190)],
            [91, "Fire Truck: a siren that slides", (s) => tune(s, [K.C2, K.G, K.C2, K.G], 330)]];
FR.forEach(([f, sub, play], i) => { go(t, f); C(t, "2. Meet 94 friends", sub); play(t + 400); t += 1900; });
// 3. chords, one hand
go(t, 0);                                                          // DUCKY: an electric piano
turn(t + 100, EN.ALGO, 1);                                         // 3 FRIENDS
C(t, "3. Chords with one finger", "3 FRIENDS: one key, a whole chord, and its name");
note(t + 600, K.C, 600); note(t + 1300, K.F, 600); note(t + 2000, K.G, 700);
t += 3000;
turn(t, EN.ALGO, 1);                                               // STRUM
C(t, "3. Chords with one finger", "STRUM: black keys pick a chord, white keys strum it");
const sweep = (s, step) => [0, 2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19].forEach((k, i) => note(s + i * step, k, step + 30));
note(t + 400, 8, 300); sweep(t + 700, 70);
note(t + 1700, 3, 300); sweep(t + 2000, 70);
t += 3200;
turn(t, EN.ALGO, 1);                                               // ACCORDION
C(t, "3. Chords with one finger", "ACCORDION: chords on the black keys, jazz ones higher up");
hold(t + 400, [8], 700);                                           // C
hold(t + 1200, [22], 700); hold(t + 2000, [15], 700); hold(t + 2800, [20], 900);   // Dm9 G9 Cmaj9
t += 4000;
// 4. games
turn(t, EN.ALGO, 1);                                               // GUESS
C(t, "4. Games for the ears", "GUESS: a friend sings a note. Can you find it?");
at(t + 2600, () => setKeys(1 << ex.web_kid_guess())); at(t + 2900, () => setKeys(0));
C(t + 2700, "4. Games for the ears", "found it!");
t += 4200;
turn(t, EN.ALGO, 1);                                               // FOLLOW
C(t, "4. Games for the ears", "FOLLOW: the next key lights up, at your own pace");
tune(t + 900, [K.C, K.C, K.G, K.G, K.A, K.A, K.G, null], 380);
t += 4300;
go(t - 300, 73);                                                   // PIANO PAL (a gold hat shows on it)
turn(t, EN.ALGO, 2);                                               // (past CHORDS) COPY ME
at(t, () => { ex.web_kid_stars_set(9); copying = true; });        // nine stars, so the first round won opens the STAR hat
C(t, "4. Games for the ears", "COPY ME: the friend plays a tune, you play it back");
C(t + 3500, "4. Games for the ears", "every game won is a star. Ten stars: a new hat!");
C(t + 5600, "4. Games for the ears", "and every round, one note longer");
at(t + 8600, () => { copying = false; });
t += 9200;
// 5. loop and layer
turn(t, EN.ALGO, -7, 80);                                          // 1 FRIEND
tap(t + 700, B.SAVE);                                              // WRITE, an empty song
const P = t + 1200;
tap(P, B.PLAY);                                                    // two bars, in a loop
C(t, "5. Loop and layer", "WRITE: PLAY an empty song, and it loops two bars");
C(P + 1000, "5. Loop and layer", "play along, and next time round it plays it back");
const beats = (s, ks) => ks.forEach((k, c) => k !== null && note(s + c * Q + 20, k, 220));
beats(P, [K.C, null, K.E, null, K.G, null, K.E, null]);
go(P + 4000 - 300, 4);                                             // UNICORN, for the next layer
C(P + 4000, "5. Loop and layer", "PRESETS: another friend, another layer");
beats(P + 4000, [null, K.G, null, K.C2, null, K.E2, null, K.D2]);
C(P + 8000, "5. Loop and layer", "two friends, one loop");
tap(P + 11600, B.PLAY); tap(P + 11900, B.SAVE);
t = P + 12400;
// the summary, over the BREAK beat and three friends
turn(t, EN.ALGO, 1);
at(t + 200, () => { seqTo = 20; });                                // SEQ round to BREAK
C(t, "New since the last video", "__LIST__");
const items = 8, gap = 1300;
at(t + 3000, () => ex.web_buttons(1 << B.PLAY)); at(t + 3080, () => ex.web_buttons(0));
tune(t + 3500, [K.C, null, K.E, null, K.F, null, K.G, null, K.A, null, K.G, null, K.E, null, K.C], 400);
t += 900 + items * gap + 1500;
C(t, "What should we add next?", "__END__");
tune(t + 300, [K.E, K.G, K.C2, null, K.G, K.C2], 330);
tap(t + 3600, B.PLAY);
const END = t + 5200;

ev.sort((a, b) => a[0] - b[0]);
const FPS = 30, SPF = 1470, frames = Math.ceil(END / 1000 * FPS);
const raw = fs.openSync(`${out}/frames.rgb`, "w"), pcm = [], keys = [];
let e = 0;
const dyn = [];                                                   // (presses decided while recording)
for (let f = 0; f < frames; f++) {
  const tt = f * 1000 / FPS;
  while (e < ev.length && ev[e][0] <= tt) ev[e++][1]();
  if (navTo !== null) {
    const cur = ex.web_kid_friend();
    if (cur === navTo) navTo = null; else ex.web_enc(EN.PRESETS, (navTo - cur + 94) % 94 <= 47 ? 1 : -1);
  }
  if (seqTo !== null) {                                            // SEQ tapped, a tap every 4 frames, to the beat wanted
    if (ex.web_kid_beat() === seqTo && f % 4 === 0) seqTo = null;
    else if (f % 4 === 0) ex.web_buttons(1 << B.SEQ); else if (f % 4 === 2) ex.web_buttons(0);
  }
  if (copying && ex.web_kid_copy_state() === 2 && tt >= copyBusy) {   // COPY ME: the child's turn, so play the pattern back
    const n = ex.web_kid_copy_len(), ks = [...Array(n).keys()].map((i) => ex.web_kid_copy_key(i));
    ks.forEach((k, i) => { const s = tt + 250 + i * 380; dyn.push([s, () => setKeys(1 << k)], [s + 240, () => setKeys(0)]); });
    copyBusy = tt + 250 + n * 380 + 600;
    dyn.sort((a, b) => a[0] - b[0]);
  }
  while (dyn.length && dyn[0][0] <= tt) dyn.shift()[1]();
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
