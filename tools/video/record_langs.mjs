// Rainbow mode in ten languages, a tour: raw RGB frames (30 fps), a WAV, captions and the keys held on each frame, as
// record_tour.mjs writes them (compose_tour.py makes the video). Each language is its own browser build, so each part
// boots its own: the hello, a friend's name, then FOLLOW with one of that language's songs, its lit keys pressed.
//   node tools/video/record_langs.mjs build OUT_DIR    (build/emu/felucca.wasm and build/langs/LL/felucca.wasm)
import fs from "fs";
const [build, out] = process.argv.slice(2);
const B = { HOME: 6, SAVE: 7, SEQ: 9, PLAY: 10 }, EN = { ALGO: 1, PRESETS: 2 };
const K = { C: 7, D: 9, E: 11, F: 12, G: 14, A: 16, B: 18, C2: 19, D2: 21, E2: 23 };
const LANGS = [   // [code, its name, the friend shown, FOLLOW's song (SEQ steps from the first), the caption]
  ["pt", "Português", 27, 0, "Ciranda Cirandinha, from Brazil"],
  ["es", "Español", 26, 0, "Las mañanitas"],
  ["fr", "Français", 15, 0, "Au clair de la lune"],
  ["it", "Italiano", 34, 1, "Funiculì funiculà"],
  ["de", "Deutsch", 29, 0, "Alle meine Entchen"],
  ["nl", "Nederlands", 50, 1, "Lang zal hij leven"],
  ["sv", "Svenska", 4, 0, "Broder Jakob"],
  ["no", "Norsk", 54, 1, "Hurra for deg som fyller ditt år"],
  ["da", "Dansk", 0, 2, "Jeg ved en lærkerede, by Carl Nielsen"],
  ["ja", "日本語", 80, 12, "Akatombo (Red Dragonfly)"],
];
const FPS = 30, SPF = 1470;
const raw = fs.openSync(`${out}/frames.rgb`, "w"), pcm = [], keys = [], cap = [];
let T = 0;                                                         // the video's clock: where this part starts, ms

async function part(wasm, len, script) {
  const { instance } = await WebAssembly.instantiate(fs.readFileSync(wasm), {});
  const ex = instance.exports, mem = ex.memory;
  ex._initialize(); ex.web_nor_erase(); ex.web_boot(); ex.web_master(1023);
  let keysNow = 0;
  const ev = [], watchers = [];
  const at = (t, f) => ev.push([t, f]);
  const setKeys = (m) => { keysNow = m; ex.web_keys(m); };
  const api = {
    ex, at,
    C: (t, a, b) => cap.push([T + t, a, b]),
    note: (t, k, l) => { at(t, () => setKeys(1 << k)); at(t + l, () => setKeys(0)); },
    tap: (t, b) => { at(t, () => ex.web_buttons(1 << b)); at(t + 80, () => ex.web_buttons(0)); },
    turn: (t, r, n, gap = 90) => { for (let i = 0; i < Math.abs(n); i++) at(t + i * gap, () => ex.web_enc(r, Math.sign(n))); },
    follow: (t, n, step) => { let done = 0, next = 0; at(t, () => watchers.push((ms) => {   // the lit key, n times
      if (ms < next) return false;
      const lit = ex.web_lit_keys() & 0x7FFFFFF;
      if (lit) { const k = 31 - Math.clz32(lit & -lit); api.note(ms, k, step - 90); done++; }
      next = ms + step; return done >= n; })); },
  };
  api.tune = (t, ks, step) => ks.forEach((k, i) => k !== null && api.note(t + i * step, k, step - 60));
  script(api);
  const frames = Math.round(len / 1000 * FPS);
  for (let f = 0; f < frames; f++) {
    const now = f * 1000 / FPS;
    ev.sort((a, b) => a[0] - b[0]);
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

// the opening, in English: a tune
await part(`${build}/emu/felucca.wasm`, 5200, (a) => {
  a.C(0, "Rainbow mode", "now in 10 more languages, each with its own songs");
  a.at(1600, () => a.ex.web_kid_friend_set(66));
  a.tune(1900, [K.C, K.E, K.G, K.C2, K.G, K.E, K.C], 300);
});
// each language: the hello, a friend, then a song of its own on FOLLOW
for (const [code, name, friend, song, what] of LANGS) {
  await part(`${build}/langs/${code}/felucca.wasm`, 7600, (a) => {
    a.C(0, name, "the hello, in its own words");
    a.note(1600, K.C, 150);
    a.at(1800, () => a.ex.web_kid_friend_set(friend));         // (its name in the band for a second, then a tune)
    a.C(1800, name, "and every friend's name");
    a.tune(3000, [K.E, K.G, K.C2], 230);
    a.turn(3800, EN.ALGO, 5);
    for (let i = 0; i < song; i++) a.tap(4200 + i * 110, B.SEQ);
    a.C(3800, name, `FOLLOW: ${what}`);
    a.follow(4900, 8, 290);
  });
}
// what else is new, over a beat, and the end card (in English)
const ITEMS = ["10 languages, each with its own songs", "36 more friends, 94 in all", "11 hats, fitted to every head",
               "CHORDS and COPY ME, two new games", "Stars that open secrets", "10 more beats, 16 more songs",
               "Write songs in loops and layers", "Runs on the SMK-37 keyboard too"];
const gap = 1450;
await part(`${build}/emu/felucca.wasm`, 1000 + ITEMS.length * gap + 1800 + 5200, (a) => {
  a.at(300, () => a.ex.web_kid_friend_set(93));
  a.note(200, K.C, 120);
  a.tap(700, B.PLAY);
  a.C(0, "New since the last video", "__LIST__");
  a.tune(1000, [K.C, null, K.E, null, K.F, null, K.G, null, K.A, null, K.G, null, K.E, null, K.C, null, K.D, null, K.E, null, K.C,
                null, K.E, null, K.G, null, K.C2], 400);
  const t = 1000 + ITEMS.length * gap + 1800;
  a.C(t, "What should we add next?", "__END__");
  a.tune(t + 300, [K.E, K.G, K.C2, null, K.G, K.C2], 330);
  a.tap(t + 3600, B.PLAY);
});

fs.closeSync(raw);
let pk = 0; for (const v of pcm) pk = Math.max(pk, Math.abs(v));
const g = 0.89 / pk, wav = Buffer.alloc(44 + pcm.length * 2);
wav.write("RIFF", 0); wav.writeUInt32LE(36 + pcm.length * 2, 4); wav.write("WAVEfmt ", 8); wav.writeUInt32LE(16, 16);
wav.writeUInt16LE(1, 20); wav.writeUInt16LE(2, 22); wav.writeUInt32LE(44100, 24); wav.writeUInt32LE(44100 * 4, 28);
wav.writeUInt16LE(4, 32); wav.writeUInt16LE(16, 34); wav.write("data", 36); wav.writeUInt32LE(pcm.length * 2, 40);
pcm.forEach((v, i) => wav.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(v * g * 32767))), 44 + i * 2));
fs.writeFileSync(`${out}/audio.wav`, wav);
fs.writeFileSync(`${out}/captions.json`, JSON.stringify({ fps: FPS, frames: keys.length, captions: cap, keys, list_gap: gap, items: ITEMS }));
console.log(`frames ${keys.length} (${(keys.length / FPS).toFixed(1)} s), audio ${(pcm.length / 2 / 44100).toFixed(1)} s, peak ${pk.toFixed(3)}`);
