// Rainbow Island: Halloween. The spooky friends come out under the moon, the first film's friends come trick-or-treating
// in the toy's hats, everyone gets a fright, then candy, then a dance to the toy's SPOOKY beat. One timeline for the
// sound (audio.mjs) and the picture (halloween.js). Times in seconds.
export const FPS = 30;
export const DUR = 96;
export const TITLE_EP = "halloween";

const NOTE = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
export const midi = (s) => {
  const m = /^([A-G])(#?)(\d)$/.exec(s);
  return 12 * (+m[3] + 1) + NOTE[m[1]] + (m[2] ? 1 : 0);
};

// fr: the sound (kid.c KID_SOUND); a stand-in plays its look-alike's, as in the toy (BAT: SKELETON's theremin, PUMPKIN:
// SLIMY's glitch, SPIDER: WEB HERO's sync lead). pic: the picture (pics.js); name: the band's word; scale: bigger or smaller
export const CAST = {
  PUMPKIN:   { fr: 23, pos: [0, 1.6, -7.6], scale: 1.45, glow: ["#ffd82e"], name: "PUMPKIN" },
  GHOST:     { fr: 13, pos: [-3.4, 1.0, -1.8], float: true, name: "GHOST" },
  BAT:       { fr: 41, pos: [5.4, 4.4, -2.6], fly: true, scale: 0.85, name: "BAT" },
  SPIDER:    { fr: 14, pos: [7.5, 2.1, -5.9], hang: 4.9, scale: 0.8, name: "SPIDER" },
  WOLF:      { fr: 56, pos: [-10.2, 1.2, -3.2], name: "WOLF" },
  SKELETON:  { fr: 41, pos: [-7.0, 0, -0.6], name: "SKELETON" },
  SLIMY:     { fr: 23, pos: [3.0, 1.5, -4.4], float: true, name: "SLIMY" },
  FLYTRAP:   { fr: 59, pos: [-9.8, 0, 2.4], name: "FLYTRAP" },
  SCIENTIST: { fr: 58, pos: [-4.2, 0, 4.0], name: "SCIENTIST" },
  OWL:       { fr: 27, pos: [8.5, 5.15, -6.4], scale: 0.85, name: "OWL" },
  // trick-or-treaters, in the toy's hats
  DUCKY:     { fr: 0,  pos: [1.2, 0, 4.6], pic: "DUCKY_WIZARD", name: "DUCKY" },
  KITTY:     { fr: 16, pos: [3.8, 0, 3.9], pic: "KITTY_WIZARD", name: "KITTY" },
  BUNNY:     { fr: 24, pos: [6.4, 0, 2.8], pic: "BUNNY_TOPHAT", name: "BUNNY" },
  FROG:      { fr: 17, pos: [8.8, 0, 1.2], pic: "FROG_CROWN", name: "FROG" },
  APRIL:     { fr: 11, pos: [10.8, 0, -1.0], pic: "APRIL_WESTERN", name: "APRIL" },
};
export const SPOOKY = ["PUMPKIN", "GHOST", "BAT", "SPIDER", "WOLF", "SKELETON", "SLIMY", "FLYTRAP", "SCIENTIST"];
export const GUESTS = ["DUCKY", "KITTY", "BUNNY", "FROG", "APRIL"];

export const ENTER = {
  PUMPKIN:   { t: 9.6, kind: "light" },
  GHOST:     { t: 12.0, kind: "rise", from: [-3.4, -2.6, -1.8] },
  BAT:       { t: 14.4, kind: "fly", from: [18, 10, -12] },
  SPIDER:    { t: 16.8, kind: "drop", from: [7.5, 4.6, -5.9] },
  WOLF:      { t: 19.2, kind: "leap", from: [-15, 0, -1] },
  SKELETON:  { t: 22.2, kind: "walk", from: [-14, 0, 3] },
  SLIMY:     { t: 25.0, kind: "loop", from: [-6, 6, -9] },
  FLYTRAP:   { t: 27.6, kind: "peek", from: [-9.8, -2.6, 2.4] },
  SCIENTIST: { t: 29.8, kind: "pop", from: [-4.2, -2.8, 4.0] },
  OWL:       { t: 0, kind: "there" },
  DUCKY:     { t: 34.2, kind: "walk", from: [17, 0, 6.6] },
  KITTY:     { t: 34.5, kind: "walk", from: [19.5, 0, 5.9] },
  BUNNY:     { t: 34.8, kind: "hop", from: [22, 0, 4.8] },
  FROG:      { t: 35.1, kind: "hop", from: [24.4, 0, 3.2] },
  APRIL:     { t: 35.4, kind: "run", from: [26, 0, 1.0] },
};

// the party: Ghost's SPOOKY beat (kid.c KID_BEATS: 116 bpm, a bass in A minor)
export const BEAT_FRIEND = "GHOST";
export const BPM = 116;
export const SPB = 60 / BPM;
export const PARTY = { t0: 51.6, bars: 12 };
PARTY.t1 = PARTY.t0 + PARTY.bars * 4 * SPB;
export const beatAt = (b) => PARTY.t0 + b * SPB;

const lines = [];
const line = (t, who, notes, o = {}) => lines.push({ t, who, notes, bubble: o.bubble !== false, oct: o.oct || 0, tag: o.tag, say: o.say });
const tune = (list, spb) => {
  const out = [];
  let at = 0;
  for (const [n, d] of list) {
    if (n) out.push([at * spb, n, d * spb * 0.92]);
    at += d;
  }
  return out;
};
const even = (ns, step, len = step * 0.9) => ns.map((n, i) => [i * step, n, len]);

// ---- 0. HALLOWEEN, a letter at a time, as the bat flies over
export const TITLE = { t0: 1.8, step: 0.34, text: "HALLOWEEN", out: 7.9 };
line(TITLE.t0, "BAT", ["A3", "C4", "E4", "A4", "C5", "E5", "D5", "B4", "A4"].map((n, i) => [i * TITLE.step, n, 0.4]), { bubble: false, tag: "title" });

// ---- 1. The spooky friends come out, one by one
line(10.3, "PUMPKIN", [[0, "E4", 0.16], [0.22, "E4", 0.16], [0.44, "E4", 0.16], [0.7, "A3", 0.6]]);
line(12.8, "GHOST", [[0, "A4", 0.5], [0.58, "C5", 0.5], [1.16, "A4", 0.9]]);
line(15.4, "BAT", even(["E5", "G5", "E5", "G5"], 0.14, 0.12));
line(17.9, "SPIDER", even(["E5", "D5", "C5", "B4", "A4"], 0.16, 0.15));
line(20.3, "WOLF", [[0, "A4", 0.35], [0.42, "E5", 1.5]], { tag: "howl" });
line(23.4, "SKELETON", even(["E4", "A4", "C5", "B4", "A4"], 0.28, 0.26));
line(26.4, "SLIMY", [...even(["C5", "B4", "A#4", "A4"], 0.12, 0.11), [0.62, "E4", 0.4]]);
line(28.5, "FLYTRAP", even(["A3", "A3", "A3", "E4"], 0.19, 0.12), { tag: "chomp" });
line(30.7, "SCIENTIST", [[0, "A3", 0.7], [0.8, "E4", 0.35], [1.2, "A4", 0.55]]);
line(32.7, "OWL", [[0, "E4", 0.3], [0.42, "E4", 0.5]]);

// ---- 2. Trick or treat!
export const KNOCK = 37.6;
for (const [who, a, b, show] of [["DUCKY", "E4", "A4", 1], ["KITTY", "A4", "C5", 0], ["BUNNY", "C5", "E5", 1], ["FROG", "A3", "E4", 0], ["APRIL", "E4", "A4", 1]])
  line(KNOCK, who, [[0, a, 0.2], [0.27, a, 0.2], [0.54, b, 0.7]], { tag: "trick", bubble: !!show, say: "TRICK OR TREAT!" });
export const BOO = 39.6;
for (const [who, n] of [["GHOST", "A4"], ["WOLF", "E5"], ["SKELETON", "C5"], ["PUMPKIN", "A3"], ["SLIMY", "E4"]])
  line(BOO, who, [[0, n, 1.0]], { tag: "boo", bubble: who === "GHOST" || who === "SKELETON", say: "BOO!" });
export const EEK = 40.5;
[["KITTY", "E5"], ["BUNNY", "G5"], ["DUCKY", "C5"], ["FROG", "A4"], ["APRIL", "B4"]].forEach(([who, n], i) =>
  line(EEK + i * 0.1, who, [[0, n, 0.16]], { tag: "eek", bubble: false }));
// .. then everyone laughs
[["GHOST", ["A4", "C5", "A4", "C5", "A4"]], ["SKELETON", ["C5", "B4", "C5", "B4", "A4"]], ["DUCKY", ["C5", "B4", "C5", "B4", "A4"]],
 ["KITTY", ["E5", "D5", "E5", "D5", "C5"]], ["PUMPKIN", ["E4", "G4", "E4", "G4", "E4"]]].forEach(([who, ns], i) =>
  line(42.0 + i * 0.15, who, even(ns, 0.11, 0.1), { tag: "giggle", bubble: who === "GHOST" || who === "KITTY" }));
export const CANDY = 44.6;                                           // candy from the pumpkin, and its cheer
line(CANDY, "PUMPKIN", even(["C4", "E4", "G4", "C5"], 0.12, 0.14), { tag: "cheer", bubble: false });
line(46.2, "BUNNY", even(["C5", "E5", "G5"], 0.14, 0.13));
line(48.4, "GHOST", [[0, "A4", 0.3], [0.36, "C5", 0.3], [0.72, "E5", 0.7]]);

// ---- 3. The SPOOKY beat party: everyone takes a turn
{
  const at = (bar) => beatAt(bar * 4);
  line(at(2), "SKELETON", tune([["A4", 1], ["C5", .5], ["B4", .5], ["A4", 1], ["E4", 1], ["F4", 1], ["E4", .5], ["D4", .5], ["E4", 2]], SPB), { tag: "solo" });
  line(at(4), "GHOST", tune([["E5", 2], ["D5", 1], ["C5", 1], ["B4", 1.5], ["C5", .5], ["B4", 1], ["G#4", 1]], SPB), { tag: "solo" });
  line(at(6), "WOLF", tune([["A4", .5], ["E5", 3.5]], SPB), { tag: "howl" });
  line(at(7), "BAT", tune([["E5", .25], ["G5", .25], ["E5", .25], ["G5", .25], ["E5", .5], ["D5", .5], ["C5", 1], ["A4", 1]], SPB), { tag: "solo" });
  line(at(8), "FLYTRAP", tune([["A3", .5], ["A3", .5], ["C4", .5], ["A3", .5], ["D4", .5], ["A3", .5], ["E4", 1]], SPB), { tag: "solo" });
  line(at(9), "SCIENTIST", tune([["A3", .5], ["E4", .5], ["A3", .5], ["G4", .5], ["A3", .5], ["E4", .5], ["C4", 1]], SPB), { tag: "solo" });
  const mel = [["A4", .5], ["B4", .5], ["C5", .5], ["D5", .5], ["E5", 1], ["C5", 1], ["D5", .5], ["C5", .5], ["B4", .5], ["G#4", .5], ["A4", 1], ["E4", 1], ["A4", 3]];
  line(at(10), "SKELETON", tune(mel, SPB), { tag: "all" });
  line(at(10), "DUCKY", tune(mel, SPB), { tag: "all", bubble: false });
  line(at(10), "KITTY", tune(mel, SPB), { tag: "all" });
  line(at(10), "GHOST", tune([["E4", 2], ["A4", 2], ["F4", 2], ["E4", 2], ["E4", 3]], SPB), { tag: "all", bubble: false });
  line(at(12), "WOLF", [[0, "A4", 0.25], [0.3, "E5", 1.4]], { tag: "end", bubble: false });
  line(at(12), "PUMPKIN", [[0, "A3", 1.2]], { tag: "end", bubble: false });
  line(at(12), "BUNNY", [[0, "C5", 1.0]], { tag: "end", bubble: false });
}
export const BIGEND = PARTY.t1;

// ---- 4. Happy Halloween
line(79.2, "GHOST", [[0, "A4", 0.6], [0.7, "E4", 1.1]], { tag: "bye" });
line(81.4, "DUCKY", [[0, "G4", 0.3], [0.38, "E4", 0.3], [0.76, "C5", 0.6]], { tag: "bye" });
export const HAPPY = { t0: 83.4, step: 0.3, text: "HAPPY HALLOWEEN" };
line(HAPPY.t0, "BAT", ["C4", "E4", "G4", "C5", "E5", null, "A4", "G4", "E4", "C4", "D4", "E4", "G4", "A4", "C5"]
  .map((n, i) => n && [i * HAPPY.step, n, 0.4]).filter(Boolean), { bubble: false, tag: "title" });
export const FINALE = HAPPY.t0 + 14 * HAPPY.step + 0.3;            // the last letter: candy, and a jump
line(FINALE, "PUMPKIN", even(["C4", "E4", "G4", "C5"], 0.12, 0.16), { tag: "cheer", bubble: false });
line(90.6, "OWL", [[0, "E4", 0.5], [0.65, "A3", 1.1]], { tag: "hoo", bubble: false });

// a low ghostly hum under the arrivals and the goodbye (the Ghost's choir, held, quiet)
line(0.4, "GHOST", [[0, "A3", 9.2], [0, "E4", 9.2]], { tag: "bed", bubble: false });
line(9.8, "GHOST", [[0, "A3", 24.0], [0, "E4", 24.0]], { tag: "bed", bubble: false });
line(78.6, "GHOST", [[0, "A3", 16.5], [0, "E4", 16.5]], { tag: "bed", bubble: false });

export const LINES = lines.sort((a, b) => a.t - b.t);

// the camera: [time, position, where it looks]; the party goes once round (halloween.js)
export const CAM = [
  [0, [0, 26, 44], [0, 12, -10]],
  [6.0, [0, 15, 28], [0, 10, -6]],
  [8.6, [0, 7, 14], [0, 3, -6]],
  [9.8, [0, 5.2, 2.6], [0, 3.8, -7.6]],
  [11.6, [0, 5.2, 2.6], [0, 3.8, -7.6]],
  [12.4, [-1.6, 3.9, 7.6], [-3.4, 3.0, -1.4]],
  [14.0, [-1.6, 3.9, 7.6], [-3.4, 3.0, -1.4]],
  [14.8, [3.4, 5.4, 6.0], [5.4, 5.6, -2.6]],
  [16.4, [3.4, 5.4, 6.0], [5.4, 5.6, -2.6]],
  [17.2, [5.0, 4.4, 3.2], [7.5, 3.8, -5.9]],
  [18.8, [5.0, 4.4, 3.2], [7.5, 3.8, -5.9]],
  [19.6, [-5.4, 4.4, 6.0], [-10.2, 3.6, -3.2]],
  [21.8, [-5.4, 4.4, 6.0], [-10.2, 3.6, -3.2]],
  [22.6, [-4.8, 3.8, 8.4], [-7.0, 2.6, -0.6]],
  [24.6, [-4.8, 3.8, 8.4], [-7.0, 2.6, -0.6]],
  [25.4, [0.8, 5.0, 6.0], [3.0, 3.6, -4.4]],
  [27.2, [0.8, 5.0, 6.0], [3.0, 3.6, -4.4]],
  [27.9, [-8.2, 3.6, 10.4], [-9.8, 2.4, 2.4]],
  [29.4, [-8.2, 3.6, 10.4], [-9.8, 2.4, 2.4]],
  [30.1, [-3.2, 3.6, 11.9], [-4.2, 2.5, 4.0]],
  [31.9, [-3.2, 3.6, 11.9], [-4.2, 2.5, 4.0]],
  [32.5, [4.6, 7.0, 2.6], [8.5, 7.2, -6.4]],
  [33.9, [4.6, 7.0, 2.6], [8.5, 7.2, -6.4]],
  [35.0, [6, 5.6, 17.5], [6, 1.6, 1]],
  [37.4, [5, 5.2, 15.5], [5, 1.8, 2]],
  [39.2, [0, 6.2, 19], [0, 1.8, 0]],
  [44.2, [0, 6.2, 19], [0, 1.8, 0]],
  [45.6, [0, 7.5, 20], [0, 2.6, -1]],
  [48.2, [-1, 6, 16], [-1, 1.8, 0]],
  [51.6, [0, 6.5, 18], [0, 1.6, 0]],
  // (the party: halloween.js goes once round the island)
  [77.2, [0, 7.5, 20], [0, 1.8, 0]],
  [80.8, [1, 6, 15], [1, 1.8, 1]],
  [83.2, [0, 9.6, 26], [0, 8.4, -4]],
  [90.0, [0, 10, 27.5], [0, 8.6, -4]],
  [96.0, [0, 11, 30], [0, 9, -4]],
];
