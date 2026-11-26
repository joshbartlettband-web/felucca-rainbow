// The Bear and the Balloon: the first Winnie-the-Pooh story (A. A. Milne, 1926: the bear, the bees, the gorse bush, the
// blue balloon, "tut-tut, it looks like rain" and the popgun), acted by Rainbow mode's Bear on a new stage, a clearing
// in a wood. One timeline for the sound (audio.mjs) and the picture (honey.js). Times in seconds.
export const FPS = 30;
export const DUR = 103;

const NOTE = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
export const midi = (s) => {
  const m = /^([A-G])(#?)(\d)$/.exec(s);
  return 12 * (+m[3] + 1) + NOTE[m[1]] + (m[2] ? 1 : 0);
};

// fr: the sound (kid.c KID_SOUND). hidden: heard, not seen (a drum, a pad)
export const CAST = {
  BEAR:      { fr: 53, name: "BEAR" },                     // Pooh: the toy's Bear, its square bass
  ROBIN:     { fr: 74, name: "ROBIN" },                    // Christopher Robin: drawn for the film, Flute Bird's real flute
  BEE:       { fr: 28, name: "BEE" },
  BUTTERFLY: { fr: 15, name: "BUTTERFLY" },
  TOMS:      { fr: 92, hidden: true },                     // School Bus's toms: bumps down the tree
  DRUM:      { fr: 47, hidden: true },                     // Toy Drum: C#4 rim, D4 snare, D#4 clap
  SQUISH:    { fr: 58, hidden: true },                     // the Scientist's squelch: mud
  PAD:       { fr: 19, hidden: true },                     // Rainbow's cloud pad, under the cloud song
  PUFF:      { fr: 68, hidden: true },                     // Morning Glory's breathy wind
};

// the stage: a clearing in a wood
export const TREE = [7, 0, -7];                            // the honey tree; the bees live in a hole near its top
export const HOLE = [7, 12.4, -5.75];
export const BRANCHES = [[5.25, 2.8], [8.75, 5.2], [5.25, 7.6], [8.75, 10.0], [5.3, 11.9]];   // x, y, on the tree's front
export const GORSE = [6.4, 0, -2.4];
export const HOUSE = [-9.5, 0, -6.5];                      // Robin's house, its door facing the clearing
export const DOOR = [-9.5, 0, -4.3];
export const PUDDLE = [-3, 0, 1.8];
export const SKY = [1.0, 11.4, -3.0];                      // where the Bear floats, near the bees' hole but not near enough

export const BPM = 100;

const lines = [];
const line = (t, who, notes, o = {}) => lines.push({ t, who, notes, bubble: o.bubble !== false && !CAST[who].hidden, oct: o.oct || 0, tag: o.tag });
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

// ---- 0. The title, and the Bear's humming tune on Robin's flute
export const TITLE = { t0: 1.4, step: 0.16, rows: ["THE BEAR AND", "THE BALLOON"], out: 8.2 };
const HUM = [["C4", .5], ["E4", .5], ["G4", .5], ["A4", .5], ["G4", 1], ["E4", 1], ["F4", .5], ["A4", .5], ["G4", .5], ["E4", .5], ["C4", 2]];
line(1.6, "ROBIN", tune(HUM, 0.42), { tag: "title", bubble: false });

// ---- 1. The Bear, humming, hears a buzz: buzz means bees, bees make honey
export const WALK_IN = [9.6, 14.2];
line(10.2, "BEAR", tune(HUM.slice(0, 6), 0.4), { tag: "hum" });
line(14.6, "BEE", even(["E5", "F5", "E5", "F5", "E5", "F5"], 0.1, 0.09), { tag: "buzz" });
line(16.4, "BEAR", [[0, "G4", 0.3], [0.4, "C5", 0.6]]);
line(18.2, "BEAR", even(["C5", "E5", "G5"], 0.16, 0.15), { tag: "yum" });

// ---- 2. Up the tree, a branch a note, then CRACK, and down through the branches into the gorse bush
export const CLIMB = [21.8, 23.2, 24.6, 26.0, 27.4];       // a hop onto each branch
line(CLIMB[0] + 0.45, "BEAR", [[0, "C4", 0.4]], { tag: "climb" });
line(CLIMB[1] + 0.45, "BEAR", [[0, "E4", 0.4]], { tag: "climb" });
line(CLIMB[2] + 0.45, "BEAR", [[0, "G4", 0.4]], { tag: "climb" });
line(CLIMB[3] + 0.45, "BEAR", [[0, "A4", 0.4]], { tag: "climb" });
line(CLIMB[4] + 0.45, "BEAR", [[0, "C5", 0.3], [0.36, "C5", 0.5]], { tag: "climb" });
export const CRACK = 29.2;
line(CRACK, "DRUM", [[0, "D4", 0.15], [0.06, "D#4", 0.15]]);
export const BUMPS = [29.9, 30.35, 30.75, 31.1];           // the branches it bumps on the way down
line(BUMPS[0], "TOMS", BUMPS.map((b, i) => [b - BUMPS[0], ["G4", "E4", "C4", "A3"][i], 0.2]));
line(29.4, "BEAR", even(["G4", "E4", "C4", "A3"], 0.45, 0.3), { tag: "fall", bubble: false });
export const GORSE_AT = 31.6;
line(33.0, "BEAR", even(["E5", "E5", "G5"], 0.16, 0.12), { tag: "ouch" });

// ---- 3. To Robin's house: a knock, a balloon please, green or blue? Blue, like the sky
export const WALK_HOUSE = [34.3, 37.3];
export const KNOCK = 37.5;
line(KNOCK, "DRUM", even(["C#4", "C#4", "C#4"], 0.24, 0.1));
export const DOOR_OPEN = 38.4;
line(39.2, "ROBIN", [[0, "G4", 0.3], [0.38, "E4", 0.5]]);
line(40.4, "BEAR", even(["C4", "E4", "G4", "A4"], 0.24, 0.22), { tag: "ask" });
export const BALLOONS = 41.8;
line(42.4, "ROBIN", [[0, "G4", 0.3], [0.4, "E5", 0.5]], { tag: "which" });
line(44.0, "BEAR", [[0, "C5", 0.3], [0.38, "E5", 0.6]], { tag: "blue" });
export const TAKE = 45.4;                                  // the blue balloon's string goes to the Bear

// ---- 4. A roll in the mud (a little black cloud), then up, up, up
export const WALK_MUD = [45.8, 47.8];
export const ROLL = [48.2, 50.4];
line(48.3, "SQUISH", even(["A3", "A3", "C4", "A3"], 0.5, 0.35));
export const MUDDY = 49.3;                                 // the bear is black with mud from here
line(51.0, "ROBIN", even(["E5", "D5", "E5", "D5", "C5"], 0.11, 0.1), { tag: "giggle" });
export const RISE = [52.2, 58.2];
line(52.6, "BEAR", tune([["C4", 1], ["D4", 1], ["E4", 1], ["G4", 1], ["A4", 1], ["C5", 2]], 0.6), { tag: "up" });

// ---- 5. In the sky: the bees wonder; Robin's umbrella, tut-tut, it looks like rain; the Bear's cloud song
line(59.0, "BEE", even(["E5", "F5", "E5", "F5", "G5"], 0.12, 0.1), { tag: "buzz" });
line(60.8, "BEAR", [[0, "C5", 0.3], [0.36, "A4", 0.3], [0.72, "F4", 0.6]], { tag: "call" });
export const UMBRELLA = [62.2, 76.6];                      // open, and walking to and fro under the Bear
for (const at of [63.2, 65.4, 67.6, 69.8])
  line(at, "ROBIN", [[0, "E5", 0.18], [0.26, "E5", 0.3]], { tag: "tut" });
export const CLOUD = { t0: 64.4, spb: 0.55 };
line(CLOUD.t0, "BEAR", tune([["E4", 1], ["G4", 1], ["C5", 1], ["C5", 3], ["B4", 1], ["A4", 1], ["G4", 1], ["E4", 3]], CLOUD.spb), { tag: "cloud" });
line(63.6, "PAD", [[0, "C4", 2.3], [0, "E4", 2.3], [0, "G4", 2.3], [2.4, "C4", 2.3], [2.4, "F4", 2.3], [2.4, "A4", 2.3],
  [4.8, "B3", 2.3], [4.8, "D4", 2.3], [4.8, "G4", 2.3], [7.2, "C4", 1.6], [7.2, "E4", 1.6], [7.2, "G4", 1.6]], { tag: "pad" });
export const SWARM = [71.6, 79.6];                         // the bees come out and round the Bear
line(71.8, "BEE", even(["E5", "F5", "E5", "F5", "E5", "F5", "E5", "F5"], 0.09, 0.08), { tag: "buzz" });
line(72.9, "BEE", even(["G5", "F5", "G5", "F5", "G5", "F5"], 0.09, 0.08), { tag: "buzz", bubble: false });
export const NOSE = 73.6;                                  // a bee sits on the Bear's nose
line(74.4, "BEAR", [[0, "G4", 0.3], [0.36, "F4", 0.3], [0.72, "D4", 0.7]], { tag: "wrong" });

// ---- 6. Shoot the balloon! Pop: ow. Pop: the balloon. Down, slowly
line(76.2, "BEAR", even(["C4", "C4", "G4"], 0.26, 0.22), { tag: "shoot" });
export const GUN = 77.2;                                   // the umbrella away, the popgun up
export const SHOTS = [78.4, 80.0];
line(SHOTS[0], "DRUM", [[0, "C#4", 0.1], [0.02, "D4", 0.12]]);
line(SHOTS[0] + 0.42, "BEAR", [[0, "G5", 0.16]], { tag: "ow" });
line(SHOTS[1], "DRUM", [[0, "C#4", 0.1], [0.02, "D4", 0.12]]);
export const POP = SHOTS[1] + 0.4;
line(POP, "DRUM", [[0, "D#4", 0.2], [0.03, "D4", 0.2]]);
export const FALL = [POP + 0.3, POP + 6.3];
line(81.2, "BEAR", tune([["C5", 1], ["B4", 1], ["A4", 1], ["G4", 1], ["F4", 1], ["E4", 1], ["D4", 1], ["C4", 2]], 0.6), { tag: "down" });
line(86.9, "ROBIN", even(["C5", "E5", "G5"], 0.15, 0.14), { tag: "yay" });

// ---- 7. A butterfly lands on his nose, and he has to blow it off: POOH!
export const FLUTTER = [88.4, 91.0];
line(91.2, "BUTTERFLY", [[0, "E5", 0.3], [0.36, "G5", 0.5]]);
export const BLOW = 92.6;
line(BLOW, "PUFF", [[0, "G4", 0.5]]);
line(BLOW + 0.05, "BEAR", [[0, "C4", 0.5]], { tag: "puff", bubble: false });
line(94.2, "ROBIN", even(["E5", "D5", "E5", "D5", "C5"], 0.11, 0.1), { tag: "giggle" });
line(94.4, "BEAR", even(["C5", "B4", "C5", "B4", "A4"], 0.11, 0.1), { tag: "giggle", bubble: false });
export const THE_END = 96.2;
line(THE_END, "ROBIN", tune([["G4", .5], ["E4", .5], ["C5", 2]], 0.42), { tag: "end", bubble: false });

// a soft bed under the story: Rainbow's cloud pad, C, A minor, F, G, quiet (not under the cloud song, which has its own)
const BED = [["C4", "E4", "G4"], ["C4", "E4", "A4"], ["C4", "F4", "A4"], ["B3", "D4", "G4"]];
for (const [from, to] of [[9.4, 62.6], [72.2, 100.6]])
  for (let at = from; at < to - 1; at += 9.6)
    line(at, "PAD", BED.flatMap((ch, i) => ch.map((n) => [i * 2.4, n, Math.min(2.35, to - at - i * 2.4)])).filter(([d, , l]) => l > 0.3), { tag: "bed" });

export const LINES = lines.sort((a, b) => a.t - b.t);

// the words in the toy's band: names, and the story's few words
const G = ["#60c85a", "#389c42"], P = ["#966ee6", "#7854c8"], O = ["#f0782a", "#c0561a"], Y = ["#d8a020", "#a87810"];
export const BANDS = [
  [9.9, 1.9, "BEAR", G], [14.8, 1.4, "BUZZ!", Y], [16.3, 1.8, "BUZZ MEANS BEES", P], [18.2, 2.0, "BEES MAKE HONEY", P],
  [21.8, 2.0, "UP AND UP", P], [CRACK, 0.9, "CRACK!", O], [30.1, 1.4, "OH HELP!", O], [GORSE_AT, 1.4, "INTO THE GORSE BUSH", P],
  [33.0, 1.2, "OUCH!", O], [34.3, 2.3, "OFF TO SEE ROBIN", P], [38.4, 1.6, "ROBIN", G], [40.3, 1.6, "A BALLOON PLEASE?", P],
  [42.2, 1.7, "GREEN OR BLUE?", P], [44.0, 1.8, "BLUE LIKE THE SKY", P], [48.2, 1.6, "SQUISH!", O],
  [50.4, 2.2, "A LITTLE BLACK CLOUD", P], [53.0, 2.0, "UP UP UP", P], [58.9, 1.6, "BZZ?", Y], [60.6, 2.0, "OPEN YOUR UMBRELLA", P],
  [63.0, 2.6, "TUT-TUT IT LOOKS LIKE RAIN", P], [66.4, 2.6, "HOW SWEET TO BE A CLOUD", P], [71.7, 1.6, "BZZZZ!", Y],
  [74.2, 2.0, "THE WRONG SORT OF BEES", P], [76.0, 1.8, "SHOOT THE BALLOON!", O], [SHOTS[0] + 0.4, 1.0, "OW!", O],
  [POP, 1.0, "POP!", O], [81.6, 2.4, "DOWN SLOWLY", P], [88.6, 1.8, "BUTTERFLY", G], [BLOW, 2.2, "POOH!", Y],
  [97.6, 3.0, "AFTER A. A. MILNE, 1926", P],
].map(([t, len, text, col]) => ({ t, len, text, col }));

// the camera: [time, position, where it looks]
export const CAM = [
  [0, [-6, 20, 40], [2, 10, -6]],
  [6.0, [-2, 12, 26], [1, 9, -6]],
  [8.6, [6, 3.4, 13], [5, 1.6, 0]],
  [11.2, [8, 3.2, 10], [6, 1.4, 1]],
  [14.0, [3, 3.0, 8.5], [3, 1.6, 0.6]],
  [15.2, [2, 2.4, 7], [5.4, 8.0, -5]],                    // the Bear looks up: so does the camera
  [17.8, [1, 3.4, 6], [6.6, 11.6, -5.8]],
  [19.6, [3, 3.0, 8.5], [3.5, 1.6, 0.2]],
  [21.4, [3.4, 3.6, 9], [6.6, 2.6, -5.4]],
  [27.6, [3.4, 11.6, 6.8], [6.6, 11.0, -5.6]],
  [29.0, [3.4, 11.6, 6.8], [6.6, 11.0, -5.6]],
  [31.2, [4.2, 4.0, 7.8], [6.4, 1.8, -2.6]],
  [33.4, [3.6, 3.2, 6.6], [5.6, 1.4, -1.6]],
  [37.0, [-5.2, 3.8, 6.0], [-8.2, 2.2, -2.8]],
  [41.6, [-5.6, 4.4, 6.6], [-8.0, 2.6, -2.8]],
  [45.4, [-5.6, 4.4, 7.4], [-7.0, 2.8, -1.6]],
  [48.0, [-1.6, 3.6, 8.6], [-3.0, 1.4, 1.6]],
  [50.0, [-1.6, 3.6, 8.6], [-3.0, 1.4, 1.6]],
  [51.0, [-3.6, 4.2, 11.8], [-4.8, 2.4, 2.2]],
  [52.4, [-2, 4.6, 11], [-2.4, 3.0, 0.6]],
  [55.0, [-5, 8.5, 14], [-1, 8.4, -1]],
  [58.0, [-5, 13, 12.5], [1.4, 13.6, -3.0]],
  [61.6, [-5, 13, 12.5], [1.4, 13.6, -3.0]],
  [62.6, [-1, 4.6, 13], [-0.6, 2.2, 1.6]],                // down to Robin and the umbrella
  [65.6, [-1, 4.6, 13], [-0.6, 2.2, 1.6]],
  [66.4, [-5, 13, 12.5], [1.4, 13.6, -3.0]],              // up to the Bear's cloud song
  [71.0, [-5, 13, 12.5], [1.4, 13.6, -3.0]],
  [72.2, [-2.6, 13.6, 7.0], [1.0, 13.4, -3.0]],           // the bees round the Bear
  [76.6, [-2.6, 13.6, 7.0], [1.0, 13.4, -3.0]],
  [77.2, [-2.0, 3.4, 9.8], [0.4, 2.8, 1.6]],              // Robin and the popgun
  [77.9, [-2.0, 3.4, 9.8], [0.4, 3.0, 1.6]],
  [78.3, [-6, 7.5, 24], [0.6, 7.6, -1]],                  // .. and the Bear up above
  [81.4, [-6, 7.5, 24], [0.6, 7.6, -1]],
  [84.2, [-3, 5.5, 13], [1.6, 5.0, -0.4]],                // down with him
  [86.8, [-1.0, 3.8, 10], [1.2, 1.8, 0.6]],
  [91.0, [0.6, 3.2, 7.6], [1.4, 2.2, 0.3]],
  [94.8, [0.6, 3.6, 9], [1.0, 2.0, 0.2]],
  [98.0, [0, 8, 20], [0, 6, -4]],
  [103, [0, 10, 26], [0, 7, -4]],
];
