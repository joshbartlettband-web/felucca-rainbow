// The story of "Rainbow Mode: a day on Rainbow Island". One timeline for the sound (audio.mjs, the real friends'
// voices from the firmware's browser build) and the picture (world.js, three.js). Times in seconds.
export const FPS = 30;
export const DUR = 111;

const NOTE = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
export const midi = (s) => {
  const m = /^([A-G])(#?)(\d)$/.exec(s);
  return 12 * (+m[3] + 1) + NOTE[m[1]] + (m[2] ? 1 : 0);
};

// friend index (kid.c KID_SOUND order), where it stands, and its picture's file
export const CAST = {
  STAR:     { fr: 39, pos: [0, 15.6, -8] },
  DUCKY:    { fr: 0,  pos: [-5.4, 0, 1.6] },
  KITTY:    { fr: 16, pos: [-2.7, 0, 3.0] },
  BUNNY:    { fr: 24, pos: [2.7, 0, 3.0] },
  ELEPHANT: { fr: 50, pos: [5.4, 0, 1.6] },
  BEAR:     { fr: 53, pos: [-8.2, 0, -0.6] },
  FROG:     { fr: 17, pos: [0, 0, 3.9] },
  APRIL:    { fr: 11, pos: [8.2, 0, -0.6] },
  OWL:      { fr: 27, pos: [8.1, 5.15, -6.2] },
  PEACOCK:  { fr: 94, pos: [0, 1.6, -7.6] },
  BEATBOT:  { fr: 46, pos: [0, 0, -2.6], file: "BEAT_BOT" },
  SHEEP:    { fr: 78, pos: [-9, 8.2, -9.5] },
};

// how each friend arrives: when, how, from where
export const ENTER = {
  STAR:     { t: 0.6, kind: "twinkle" },
  DUCKY:    { t: 9.8, kind: "pop", from: [-6.0, -2.2, -3.9] },
  KITTY:    { t: 12.2, kind: "peek", from: [-2.7, -3, 3.0] },
  BUNNY:    { t: 14.6, kind: "hop", from: [9, 0, 6] },
  ELEPHANT: { t: 17.3, kind: "walk", from: [13, 0, 3] },
  BEAR:     { t: 19.9, kind: "walk", from: [-14, 0, -1] },
  FROG:     { t: 22.5, kind: "leap", from: [-3, 0, 10] },
  APRIL:    { t: 24.9, kind: "run", from: [15, 0, 2] },
  OWL:      { t: 29.4, kind: "fly", from: [16, 11, -10] },
  PEACOCK:  { t: 45.4, kind: "rise", from: [0, -2.4, -7.6] },
  BEATBOT:  { t: 56.0, kind: "drop", from: [0, 16, -2.6] },
  SHEEP:    { t: 86.5, kind: "float", from: [-16, 9, -9.5] },
};

// the beat: Ducky's DANCE beat (kid.c KID_BEATS: 112 bpm), 12 bars from PARTY.t0, then a last downbeat
export const BPM = 112;
export const SPB = 60 / BPM;
export const PARTY = { t0: 58.4, bars: 12 };
PARTY.t1 = PARTY.t0 + PARTY.bars * 4 * SPB;          // the downbeat of bar 13: the last chord
export const beatAt = (b) => PARTY.t0 + b * SPB;

// a line: who sings, when, its notes [offset s, note, length s], and whether a speech bubble shows them
const lines = [];
const line = (t, who, notes, o = {}) => lines.push({ t, who, notes, bubble: o.bubble !== false, oct: o.oct || 0, tag: o.tag });
// notes in beats at a tempo (a rest is null)
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

// ---- 0. Title: the star rings each letter of RAINBOW MODE
export const TITLE = { t0: 1.6, step: 0.3, text: "RAINBOW MODE", out: 8.3 };
{
  const notes = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", null, "C5", "E5", "G5", "C5"];
  line(TITLE.t0, "STAR", notes.map((n, i) => n && [i * TITLE.step, n, 0.5]).filter(Boolean), { bubble: false, tag: "title" });
  line(5.9, "STAR", even(["G5", "E5", "C5"], 0.2, 0.35), { tag: "hi" });
}

// ---- 1. Hello! one by one, each in its own voice
line(10.5, "DUCKY", [[0, "G4", 0.32], [0.38, "E4", 0.55]]);
line(12.75, "KITTY", [[0, "E5", 0.28], [0.34, "C5", 0.6]]);
line(15.5, "BUNNY", even(["C4", "E4", "G4", "C5"], 0.17, 0.2));
line(18.1, "ELEPHANT", [[0, "G4", 0.18], [0.24, "G4", 0.18], [0.48, "C5", 0.8]]);
line(20.7, "BEAR", [[0, "C4", 0.38], [0.45, "G3", 0.38], [0.9, "C4", 0.75]], { oct: -1 });
line(23.45, "FROG", [[0, "C4", 0.22], [0.3, "C5", 0.5]]);
line(25.75, "APRIL", [[0, "A4", 0.15], [0.22, "A4", 0.15], [0.5, "D5", 0.45]]);
// all together: hel-lo! (G major, then C major)
for (const [who, a, b, oct] of [["DUCKY", "G4", "E4"], ["KITTY", "B4", "G4"], ["ELEPHANT", "D5", "C5"], ["BEAR", "G3", "C4", -1]])
  line(27.6, who, [[0, a, 0.4], [0.48, b, 0.85]], { oct: oct || 0, tag: "together" });

// ---- 2. COPY ME (the toy's memory game): the owl sings, the frog copies
line(30.6, "OWL", [[0, "G4", 0.3], [0.42, "G4", 0.5]]);
line(32.1, "OWL", even(["C4", "D4", "E4", "G4"], 0.4, 0.36), { tag: "pattern" });
line(34.3, "FROG", even(["C4", "D4", "E4", "F#4"], 0.4, 0.36), { tag: "oops" });
line(36.4, "KITTY", even(["E5", "D5", "E5", "D5", "C5"], 0.11, 0.1), { tag: "giggle" });
line(36.55, "BUNNY", even(["G4", "A4", "G4", "A4", "G4"], 0.11, 0.1), { tag: "giggle" });
line(36.7, "DUCKY", even(["C5", "B4", "C5", "B4", "A4"], 0.11, 0.1), { tag: "giggle" });
line(38.0, "OWL", even(["C4", "D4", "E4", "G4"], 0.45, 0.4), { tag: "pattern" });
line(40.3, "FROG", even(["C4", "D4", "E4", "G4"], 0.42, 0.38), { tag: "right" });
export const YES = 42.1;                                         // confetti, and the toy's cheer up the C major chord
line(YES, "DUCKY", even(["C4", "E4", "G4", "C5"], 0.12, 0.14), { tag: "cheer", bubble: false });
line(43.0, "OWL", [[0, "C5", 0.5]]);

// ---- 3. The Peacock: a harp in a great hall
line(47.0, "PEACOCK", [
  ...even(["C4", "E4", "G4", "C5", "E5", "G5"], 0.13, 1.15).map(([d, n]) => [d, n, 1.15 - d]),
  ...even(["F4", "A4", "C5", "F5"], 0.13).map(([d, n]) => [1.25 + d, n, 1.0 - d]),
  ...even(["G4", "B4", "D5", "G5"], 0.13).map(([d, n]) => [2.35 + d, n, 1.0 - d]),
  ...even(["C4", "E4", "G4", "C5", "E5", "G5"], 0.12).map(([d, n]) => [3.45 + d, n, 2.4 - d]),
], { tag: "grand" });
line(51.6, "OWL", [[0, "G4", 2.0]], { tag: "ooh" });
line(51.6, "ELEPHANT", [[0, "E4", 2.0]], { tag: "ooh" });
line(51.6, "BEAR", [[0, "C4", 2.0]], { oct: -1, tag: "ooh" });
line(54.2, "PEACOCK", [[0, "G4", 0.3], [0.35, "C5", 0.9]]);

// ---- 4. The party: Beat Bot says boom-tss and starts the beat, then everyone takes a turn
//      (Beat Bot's keys are drums: C4 the kick, D4 the snare, F#4 the closed hat; eng_drum.c's GM map)
line(56.9, "BEATBOT", [[0, "C4", 0.2], [0.27, "F#4", 0.15], [0.54, "D4", 0.2], [0.81, "F#4", 0.15]], { tag: "boomtss" });
{
  const at = (bar) => beatAt(bar * 4);
  line(at(2), "DUCKY", tune([["G4", .5], ["E4", .5], ["G4", .5], ["E4", .5], ["C5", 1], ["B4", .5], ["A4", .5],
    ["G4", 1], ["E4", .5], ["D4", .5], ["C4", 2]], SPB), { tag: "solo" });
  line(at(4), "KITTY", tune([["E5", .5], ["D5", .5], ["C5", .5], ["D5", .5], ["E5", 1], ["G5", 1],
    ["E5", .5], ["D5", .5], ["C5", 1], ["C5", 2]], SPB), { tag: "solo" });
  line(at(6), "ELEPHANT", tune([["G4", .5], ["G4", .5], ["A4", .5], ["G4", .5], ["C5", 1], ["C5", 1],
    ["D5", .5], ["C5", .5], ["A4", 1], ["G4", 2]], SPB), { tag: "solo" });
  line(at(8), "FROG", tune([["C4", .5], ["C4", .5], ["G4", 1], ["C4", .5], ["C4", .5], ["G4", 1]], SPB), { tag: "solo" });
  line(at(9), "BUNNY", tune([["C5", .25], ["B4", .25], ["A4", .25], ["G4", .25], ["A4", .5], ["G4", .5], ["E4", 1], ["C4", 1]], SPB), { tag: "solo" });
  // bars 11 and 12 all together, and the last chord on the downbeat of bar 13
  const mel = [["G4", .5], ["A4", .5], ["C5", .5], ["A4", .5], ["G4", 1], ["E4", 1],
    ["D4", .5], ["E4", .5], ["G4", .5], ["A4", .5], ["B4", 1], ["D5", 1], ["C5", 3]];
  const low = [["E4", .5], ["F4", .5], ["A4", .5], ["F4", .5], ["E4", 1], ["C4", 1],
    ["B3", .5], ["C4", .5], ["E4", .5], ["F4", .5], ["G4", 1], ["B4", 1], ["G4", 3]];
  line(at(10), "DUCKY", tune(mel, SPB), { tag: "all" });
  line(at(10), "KITTY", tune(mel, SPB), { tag: "all", bubble: false });
  line(at(10), "ELEPHANT", tune(low, SPB), { tag: "all" });
  line(at(12), "BEAR", [[0, "C4", 1.6]], { oct: -1, tag: "end", bubble: false });
  line(at(12), "PEACOCK", even(["C4", "E4", "G4", "C5", "E5", "G5"], 0.09).map(([d, n]) => [d, n, 1.9 - d]), { tag: "end", bubble: false });
  line(at(12), "APRIL", [[0, "E5", 1.2]], { tag: "end", bubble: false });
}
export const BIGEND = PARTY.t1;

// ---- 5. Goodnight: a yawn, the sheep's lullaby (Brahms, as in FOLLOW), and the owl's last hoo
line(85.0, "DUCKY", [[0, "E4", 0.9], [1.0, "C4", 1.1]], { tag: "yawn" });
export const LULLABY = { t0: 89.2, spb: 0.66 };
line(LULLABY.t0, "SHEEP", tune([["E4", .5], ["E4", .5], ["G4", 1.5], ["E4", .5], ["E4", .5], ["G4", 1.5], ["E4", .5], ["G4", .5],
  ["C5", 1], ["B4", 1], ["A4", 1], ["A4", 1], ["G4", 2], ["D4", .5], ["E4", .5], ["F4", 1], ["D4", 1], ["D4", .5], ["E4", .5],
  ["F4", 2], ["D4", .5], ["F4", .5], ["B4", .5], ["A4", .5], ["G4", 1], ["B4", 1], ["C5", 3]], LULLABY.spb), { tag: "lullaby" });
line(105.6, "OWL", [[0, "G4", 0.7], [0.85, "C4", 1.3]], { tag: "hoo" });
export const GOODNIGHT = { t0: 104.6, text: "GOODNIGHT" };

export const LINES = lines.sort((a, b) => a.t - b.t);

// who falls asleep when (during the lullaby), and the sky: 1 day, 0.5 dawn or dusk, 0 night
export const SLEEP = { APRIL: 92, BEAR: 93.5, FROG: 95, BUNNY: 96.5, KITTY: 98, ELEPHANT: 99.5, DUCKY: 101, BEATBOT: 97, PEACOCK: 102.5 };
export const SKY = [[0, 0.55], [7, 1], [84, 1], [88.5, 0.5], [93, 0]];
// shimmering gold over the island while the peacock is out
export const GLOW = [[44.6, 0], [46, 1], [53.5, 1], [56, 0]];

// the camera: [time, position, where it looks]; it eases between keys
export const CAM = [
  [0, [0, 30, 46], [0, 9, -6]],
  [5.6, [0, 15, 30], [0, 8, -6]],
  [8.4, [0, 9, 24], [0, 4, -4]],
  [9.6, [-3, 4.2, 12], [-4, 1.6, 0]],
  [12.0, [-3, 4.2, 12], [-4, 1.6, 0]],
  [14.0, [0, 4.6, 14], [0, 1.6, 1]],
  [17.2, [2, 4.6, 14], [2, 1.6, 1]],
  [19.6, [0, 5.5, 17], [0, 1.6, 0]],
  [22.0, [-1, 5.5, 17], [-1, 1.4, 0]],
  [24.6, [2, 5.4, 17], [2, 1.4, 0]],
  [27.2, [0, 6.2, 19], [0, 1.4, 0]],
  [29.2, [0, 6.2, 19], [0, 1.4, 0]],
  [31.0, [3.2, 6.6, 3.6], [7.8, 6.4, -6.2]],
  [33.6, [3.2, 6.6, 3.6], [7.8, 6.4, -6.2]],
  [34.6, [1.2, 4.3, 12.2], [0.4, 2.6, 3.4]],
  [36.0, [1.2, 4.3, 12.2], [0.4, 2.6, 3.4]],
  [36.6, [0, 5.0, 14.5], [-0.5, 1.8, 2]],
  [37.6, [0, 5.0, 14.5], [-0.5, 1.8, 2]],
  [38.3, [3.2, 6.6, 3.6], [7.8, 6.4, -6.2]],
  [39.9, [3.2, 6.6, 3.6], [7.8, 6.4, -6.2]],
  [40.8, [1.2, 4.3, 12.2], [0.4, 2.6, 3.4]],
  [42.0, [1.5, 4.2, 12.5], [0.4, 2.0, 3]],
  [44.0, [0, 6.5, 18], [0, 1.6, 0]],
  [46.0, [0, 4.5, 6], [0, 3.6, -7.6]],
  [51.2, [0, 4.2, 4.5], [0, 3.5, -7.6]],
  [54.0, [0, 7, 16], [0, 2.4, -3]],
  [56.4, [0, 6, 13], [0, 2.2, -2.6]],
  [58.4, [0, 6.5, 17], [0, 1.6, 0]],
  // the party: once round the island, and a little back for the end
  [62.6, [12, 8, 12], [0, 1.6, 0]],
  [66.9, [17, 7, -2], [0, 1.6, 0]],
  [71.2, [8, 9, -15], [0, 1.6, -1]],
  [75.5, [-10, 8, -12], [0, 1.6, 0]],
  [79.8, [-15, 7, 6], [0, 1.6, 0]],
  [84.2, [0, 7.5, 19], [0, 1.8, 0]],
  [87.2, [-3, 8.6, 5.5], [-9, 9.2, -9.5]],
  [91.8, [-3, 8.6, 5.5], [-9, 9.2, -9.5]],
  [95.5, [-1, 6.8, 17], [-3, 3, -3]],
  [102.0, [0, 5.5, 15], [0, 1.6, 0]],
  [106.0, [0, 9, 24], [0, 6, -6]],
  [111.0, [0, 12, 30], [0, 8, -6]],
];
