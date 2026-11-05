// Rainbow mode, a one-minute tour of what is new: the hellos of the ten languages, quickly, then the new things played on
// the English build. Writes what record_tour.mjs writes (frames.rgb, audio.wav, captions.json); compose_tour.py makes it.
//   node tools/video/record_short.mjs build OUT_DIR    (build/emu/felucca.wasm and build/langs/LL/felucca.wasm)
import fs from "fs";
const [build, out] = process.argv.slice(2);
const B = { HOME: 6, SAVE: 7, SEQ: 9, PLAY: 10 }, EN = { ALGO: 1, PRESETS: 2, K4: 6 };
const K = { F3: 0, A3: 4, B3: 6, C: 7, D: 9, E: 11, F: 12, G: 14, A: 16, B: 18, C2: 19, D2: 21, E2: 23, G2: 26 };
const FR = { KING_AXOLOTL: 66, SPIDER_MOM: 61, SAX_CAT: 75, TIGER_CUB: 70, T_REX: 40, BUNNY: 24, SNAIL: 82, PIANO_PAL: 73,
             SCIENTIST: 58, DRAGON_DUCK: 62, FLYTRAP: 59 };
const LANGS = [["pt", "Português"], ["es", "Español"], ["fr", "Français"], ["it", "Italiano"], ["de", "Deutsch"],
               ["nl", "Nederlands"], ["sv", "Svenska"], ["no", "Norsk"], ["da", "Dansk"], ["ja", "日本語"]];
const FPS = 30, SPF = 1470;
const raw = fs.openSync(`${out}/frames.rgb`, "w"), pcm = [], keys = [], cap = [];
let T = 0;

async function part(wasm, len, script, pre = 0) {   // (pre: ms played before it is recorded)
  const { instance } = await WebAssembly.instantiate(fs.readFileSync(wasm), {});
  const ex = instance.exports, mem = ex.memory;
  ex._initialize(); ex.web_nor_erase(); ex.web_boot(); ex.web_master(1023);
  let keysNow = 0;
  const ev = [], watchers = [];
  const at = (t, f) => ev.push([t, f]);
  const setKeys = (m) => { keysNow = m; ex.web_keys(m); };
  const a = {
    ex, at, setKeys,
    C: (t, x, y) => cap.push([T + t, x, y]),
    note: (t, k, l) => { at(t, () => setKeys(1 << k)); at(t + l, () => setKeys(0)); },
    hold: (t, ks, l) => { at(t, () => setKeys(ks.reduce((m, k) => m | (1 << k), 0))); at(t + l, () => setKeys(0)); },
    tap: (t, b) => { at(t, () => ex.web_buttons(1 << b)); at(t + 80, () => ex.web_buttons(0)); },
    turn: (t, r, n, gap = 90) => { for (let i = 0; i < Math.abs(n); i++) at(t + i * gap, () => ex.web_enc(r, Math.sign(n))); },
    friend: (t, f) => at(t, () => ex.web_kid_friend_set(f)),
    watch: (t, f) => at(t, () => watchers.push(f)),
  };
  a.tune = (t, ks, step) => ks.forEach((k, i) => k !== null && a.note(t + i * step, k, step - 60));
  a.chords = (t, n, wait = 450, l = 600) => { let done = 0, lit = 0, since = 0, until = 0; a.watch(t, (ms) => {   // CHORDS
    if (until) { if (ms < until) return false; setKeys(0); until = 0; done++; lit = 0; return done >= n; }
    const m = ex.web_lit_keys() & 0x7FFFFFF;
    if (m !== lit) { lit = m; since = ms; }
    if (m && ms - since >= wait) { setKeys(m); until = ms + l; }
    return false; }); };
  a.copyMe = (t, n, step = 380) => { let done = 0, busy = false; a.watch(t, (ms) => {                       // COPY ME
    if (busy) return false;
    if (ex.web_kid_copy_state() !== 2) return done >= n;
    const ks = [...Array(ex.web_kid_copy_len()).keys()].map((i) => ex.web_kid_copy_key(i));
    busy = true;
    ks.forEach((k, i) => a.note(ms + 350 + i * step, k, step - 110));
    at(ms + 350 + ks.length * step + 200, () => { busy = false; done++; });
    return false; }); };
  script(a);
  for (let k = 0; k < Math.round(pre * 44.1); k += 147) ex.web_render(147);
  const frames = Math.round(len / 1000 * FPS);
  for (let f = 0; f < frames; f++) {
    const now = f * 1000 / FPS;
    ev.sort((p, q) => p[0] - q[0]);
    while (ev.length && ev[0][0] <= now) ev.shift()[1]();
    for (let i = watchers.length - 1; i >= 0; i--) if (watchers[i](now)) watchers.splice(i, 1);
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
  T += frames * 1000 / FPS;
}

// the opening: a tune
await part(`${build}/emu/felucca.wasm`, 2800, (a) => {
  a.C(0, "Rainbow mode", "a free music toy for little hands, on the M-VAVE FM-1");
  a.friend(900, FR.KING_AXOLOTL);
  a.tune(1100, [K.C, K.E, K.G, K.C2], 250);
});
// the languages: each one's hello, a moment each
for (const [code, name] of LANGS)
  await part(`${build}/langs/${code}/felucca.wasm`, 1250, (a) => a.C(0, "Now in 10 more languages", name), 1100);
// what is new, on the English build
let t = 0;
await part(`${build}/emu/felucca.wasm`, 41500, (a) => {
  a.note(300, K.C, 100);
  // 94 friends
  a.C(t, "94 friends", "36 new ones since the last post");
  [FR.SPIDER_MOM, FR.T_REX, FR.SAX_CAT, FR.TIGER_CUB].forEach((f, i) => { a.friend(t + 400 + i * 1000, f); a.tune(t + 750 + i * 1000, [K.E, K.G], 200); });
  t += 4500;
  // hats that fit
  a.friend(t, FR.BUNNY);
  a.C(t, "Hats that fit", "for grown-ups: hold HOME, then turn KNOB 4");
  a.at(t + 200, () => a.ex.web_buttons(1 << B.HOME));
  [0, 1, 2].forEach((i) => a.turn(t + 1400 + i * 600, EN.K4, 1));
  a.at(t + 3200, () => a.ex.web_buttons(0));
  a.friend(t + 3400, FR.SNAIL);
  t += 4500;
  // 3 FRIENDS: magic chords
  a.friend(t, FR.PIANO_PAL);
  a.turn(t + 200, EN.ALGO, 1);
  a.C(t, "Magic chords", "3 FRIENDS: a major chord on every key");
  a.hold(t + 1600, [K.C], 500); a.hold(t + 2200, [15], 500); a.hold(t + 2800, [17], 500); a.hold(t + 3400, [K.C2], 800);
  t += 4500;
  // CHORDS: lessons
  a.turn(t, EN.ALGO, 5);
  a.C(t, "CHORDS", "chord lessons, from first chords to lofi");
  a.chords(t + 1200, 3);
  t += 5500;
  // COPY ME, and a secret at 25 stars
  a.turn(t, EN.ALGO, 1);
  a.at(t, () => a.ex.web_kid_stars_set(24));
  a.C(t, "COPY ME", "the friend plays it, your kid plays it back");
  a.copyMe(t + 1400, 1);
  a.C(t + 5000, "Stars open secrets", "every game won is a star. 25: the northern lights");
  t += 7500;
  // 21 beats
  a.turn(t, EN.ALGO, -7, 60);
  a.friend(t + 600, FR.SCIENTIST);
  a.tap(t + 900, B.PLAY);
  a.C(t, "21 beats", "ACID, LOFI and a real drum break");
  a.tune(t + 1300, [K.C, K.C, K.E, K.C, K.G, K.F, K.E, K.C, K.C, K.E], 250);
  a.tap(t + 4300, B.PLAY);
  t += 4500;
  // WRITE: loop and layer
  a.friend(t, FR.DRAGON_DUCK);
  a.tap(t + 400, B.SAVE);
  a.C(t, "Write a song", "it loops, with a new friend on each layer");
  a.tap(t + 900, B.PLAY);
  a.tune(t + 1200, [K.C, null, K.E, null, K.G, null, K.E, null], 330);
  a.turn(t + 4000, EN.PRESETS, 1);
  a.tune(t + 4200, [null, K.C2, null, K.B, null, K.G, null, K.A], 330);
  t += 7000;
  a.tap(t - 100, B.PLAY); a.tap(t + 200, B.SAVE);
  // the end card
  a.C(t, "What should we add next?", "__END__");
  a.tune(t + 400, [K.E, K.G, K.C2, null, K.G, K.C2], 300);
});

fs.closeSync(raw);
let pk = 0; for (const v of pcm) pk = Math.max(pk, Math.abs(v));
const g = 0.89 / pk, wav = Buffer.alloc(44 + pcm.length * 2);
wav.write("RIFF", 0); wav.writeUInt32LE(36 + pcm.length * 2, 4); wav.write("WAVEfmt ", 8); wav.writeUInt32LE(16, 16);
wav.writeUInt16LE(1, 20); wav.writeUInt16LE(2, 22); wav.writeUInt32LE(44100, 24); wav.writeUInt32LE(44100 * 4, 28);
wav.writeUInt16LE(4, 32); wav.writeUInt16LE(16, 34); wav.write("data", 36); wav.writeUInt32LE(pcm.length * 2, 40);
pcm.forEach((v, i) => wav.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(v * g * 32767))), 44 + i * 2));
fs.writeFileSync(`${out}/audio.wav`, wav);
fs.writeFileSync(`${out}/captions.json`, JSON.stringify({ fps: FPS, frames: keys.length, captions: cap, keys, list_gap: 1450 }));
console.log(`frames ${keys.length} (${(keys.length / FPS).toFixed(1)} s), peak ${pk.toFixed(3)}`);
