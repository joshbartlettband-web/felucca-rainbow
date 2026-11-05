# Amethyst: drum and bass for the FM-1

Amethyst is a working name for a new FM-1 firmware Josh is making with a friend. It plays drum and bass, and it is set
in a London a few years from now: wet streets, sodium lamps, tower blocks, and moss growing over all the concrete. A
break is always running. You play the bass and the chords over it, chop the break on the black keys, and hold a button
to build up to the drop.

Nothing here is built yet. This is the plan to talk over before any code. The questions at the end need answers from
Josh and the friend first.

![Eight mock screens: CANAL, ARCHES, PIRATE, NIGHT BUS, MOSS, the break's slices, CCTV and the hello](amethyst/sheet.png)

The screens above are sketches at the FM-1's size, each cut to 16 colors the way Album 01 cuts its photos. They come
from `tools/amethyst/mockups.py`, so they can be redrawn as the ideas change.

---

## 1. A minute with it

You switch it on and the stone glows. The first stage is CANAL: a brick bridge over the water, a lamp far down the
tunnel. The break is already rolling at 174.

You hold a low white key and a Reese bass growls under the break. Every white key fits, because they're all in A minor,
so nothing can go wrong. You tap the black keys and the break stutters: each one plays a slice of it, the way jungle
producers chopped breaks on an Akai sampler in 1994.

You hold FX. A snare roll climbs and the picture whites out. Let go, and on the next bar the kick and bass drop back in.
That's the whole game, and it's enough to lose an evening to.

## 2. Where to build it

Album 01 is the closest thing to this, so I'd start there.

Album is built on [fm1-base](https://github.com/charlesvestal/fm1-base) by Charles Vestal (MPL-2.0, so an app on it can
be MIT like Album). It already has what Amethyst needs most: the photo pipeline (`album/tools/photos.py`, 16 colors a
photo, about 18 KB each), a synth with detuned saws, a reverse reverb and a fuzz, a beat for every patch with fills and
an auto bass on the kick. Its template is 77 KB of the 581 KB app slot, and the flash's data area
(0x97000 to 0xDFFFF, 292 KB, shared with the saved settings) is there for samples.

Felucca, the base of this repo, is the other choice. It has a SLICE engine that already plays a break a slice a step,
a DRUM engine and a full sequencer. But it carries 13 engines, it's GPL-3.0, and Rainbow mode filled it to 97%. A DnB
toy would spend most of its time hiding what Felucca does.

So: a new repo on fm1-base, with Album's photo code and synth as the starting point. It could even be Album 02, if Josh
wants Amethyst to be the next record in that series.

## 3. How it plays

Two rules make it easy. The break never stops unless you stop it, and the keys can't play a wrong note.

| Control | What it does |
| --- | --- |
| White keys F3 to E4 (7) | The bass. A minor, so every key fits. Hold one and press another and it slides |
| White keys F4 to G5 (9) | Chords: a minor ninth, a major seventh and so on, one a key, in the stage's own voicing |
| Black keys (11) | Slices of the break, one each, in order. Tap a few and you're chopping |
| PRESETS | The stage: its picture, its break, its bass, its chords and its tempo |
| SELECT | The tempo, 160 to 180. The break is pitched with it, as a sampler did, not stretched |
| ALGORITHM | The break's pattern: AS PLAYED, CHOPPED, HALF TIME, ROLLER, TWO-STEP |
| KNOB 1 WOBBLE | The bass filter moves, slow to fast. The picture breathes with it |
| KNOB 2 FOG | Reverb and delay. Fog rolls over the picture |
| KNOB 3 GRIT | Crushed and driven. The picture goes grainy |
| KNOB 4 MOSS | Darker and softer, rain and crackle under it. The picture goes green |
| FX (hold) | BUILD: a snare roll and a riser while held. Let go and it drops on the next bar |
| SCL | REWIND: the record pulled back and the tune started again from bar 1 |
| ENV | HALF TIME, on and off |
| LFO | TAPE STOP |
| EDIT | Drums off and on (the bass carries on) |
| GLO | A dub siren, played on the keys while held |
| ARP | How the keys play: BASS AND CHORDS, ALL BASS, ALL CHORDS |
| SEQ | The break on or off |
| REC | Records four bars of what you play, then loops it. Again to add a layer |
| PLAY | Start and stop |
| SAVE | Keeps the stage's knobs and your loop |
| HOME | The stage back where it started |
| OCT- / OCT+ | The bass an octave down or up |
| MASTER | Volume |

FX for the build is the one I'd test first with real people. If the drop doesn't feel good, the rest won't save it.

## 4. The stages

Eight to start. Each one is a place, a break, a bass and a set of chords, tuned to sound like that place.

| # | Stage | The place | Break | Bass | Tempo |
| --- | --- | --- | --- | --- | --- |
| 1 | CANAL | A brick bridge over the water at night, moss in the mortar | A busy, bright break | Reese, slow | 174 |
| 2 | ARCHES | A rave under a railway arch, lasers from the back | A hard, chopped break | Reese, fast and driven | 174 |
| 3 | PIRATE | A tower block with an aerial and a red light on top | A rough old break | Sub, with a hoover on the chords | 170 |
| 4 | NIGHT BUS | Rain on the top deck's window, the city going past | A light two-step | Round sub | 172 |
| 5 | MOSS | Concrete, moss and amethyst growing out of it | A soft, swung break | Warm sub, slow slides | 170 |
| 6 | UNDERPASS | A tiled tunnel and a CCTV camera | A cold, dry roller | Neuro growl | 175 |
| 7 | ROOFTOP | The skyline at first light | A rolling, open break | Sub and a pad | 172 |
| 8 | FOG | The river under the bridges, nothing quite in focus | A break far off in the reverb | Long sub notes | 168 |

## 5. The breaks, and what we can ship

The famous breaks can't go in. The Amen is from "Amen, Brother" by the Winstons (1969). Richard L. Spencer owned the
copyright and was never paid for any of the sampling; a 2015 GoFundMe raised some money for him. Think (Lyn Collins,
1972), Apache (Incredible Bongo Band, 1973) and Funky Drummer (James Brown, 1970) are the same story. A firmware that
anyone can download is a sample pack, and nobody has given anyone the right to hand those recordings out.

A drum pattern on its own is much harder to own than a recording of it, as far as I understand it (worth checking
with someone who does this for a living). So the plan is to keep the patterns and replace the recordings.

| Source | License | What it gives us |
| --- | --- | --- |
| A drummer we know, recorded for this | CC0, if they agree | The real thing: eight breaks played in a live room at 174. The best option by a long way |
| [Virtuosity Drums](https://versilian-studios.com/) (Versilian Studios) | CC0 | A jazz kit played with sticks, six mic positions including Room and Vintage. A room mic is half of what makes a break sound like one. Felucca's piano already comes from Versilian |
| [VCSL](https://github.com/sgossner/VCSL) (Versilian Studios) | CC0 | More snares, toms and a frame drum |
| DrumGizmo kits (DRSKit, CrocellKit, MuldjordKit) | CC-BY 4.0 (from the SFZ catalog and Guix; check DrumGizmo's own pages) | Full acoustic kits. Each needs a credit |
| [Freesound](https://freesound.org/) | CC0 per sound, checked one by one | Rain, footsteps, buses, a lighter. Skip any "classic breakbeats" there: an uploader can't give away the Winstons' recording by marking it CC0 |
| [Selektaudio](https://selektaudio.com/loops/drums) | CC0, public domain or CC-BY, by loop | Says each loop comes with a note of where it came from. Check each one |

Until there's a drummer, the build can play the patterns of the classic breaks on Virtuosity Drums' hits, with ghost
notes and a little looseness in the timing, through a room. Felucca's `tools/gen_samples.py` already builds its BREAK
this way from its own drums, so the idea is tested.

A drummer would be the best part of this. Eight breaks in an afternoon, released CC0 with their name on them, and other
FM-1 projects could use them too.

The bass, the chords and the siren need no samples: they're synthesized, like Album's patches. London's own sounds
need care. The Underground's announcements belong to TfL, so a train or a station would have to be recorded by us.

## 6. The look

Album 01 is the starting point: one full-screen picture a stage, 16 colors, the name at the top, and the picture moving
with the sound. Here's how each idea could carry it, with its sketch.

1. Photos, as Album 01 does (CANAL). Real London at night, cut to 16 colors. The rows waver with the bass, FOG
   blurs them, the brightest colors flash on the kick. It needs photos: the friend's, Josh's, or ones we can license.
2. Rave stages (ARCHES). Drawn, not photographed: an arch, a warehouse, a roof. Lasers and strobes run on the beat,
   and the crowd jumps on the drop. Every stage can be the same club on a different night.
3. Pirate radio (PIRATE). PRESETS turns a tuning dial, with a bar of static between stations. Each stage is a
   station with a call sign. In the '90s, London's jungle stations broadcast from tower block roofs, so this one tells
   a bit of the music's history.
4. The night bus (NIGHT BUS). Rain on the window and lights sliding past at the tempo. TAPE STOP pulls the bus in.
5. Moss and amethyst (MOSS). A jam grows moss over concrete, and every drop grows a crystal. A long jam leaves a
   garden. It's a small game, and it gives the name a reason.
6. The chop (BREAK 3). The break drawn as its 11 slices, the black key under each one, the one you're playing lit.
   This works best as a layer that comes up over any stage while you play the black keys, then fades.
7. CCTV (CAM 04). A grainy camera on an underpass, the bar count as the timestamp. The picture glitches when you
   chop. The most noir of the lot.

My pick would be photos for the stages, with the rave lights drawn over them on the beat, the chop layer on the black
keys, and the moss growing as you play. The pirate dial makes a good way to move between stages.

The screen has no frame buffer. It's drawn in strips of rows, and a full redraw took about 60 ms on Rainbow mode. Album
unpacks one band of 16 rows (1,920 bytes) as it draws. So the lights have to be cheap: a color flash or a line per row
costs almost nothing, a big moving blur costs a lot. Each idea above was picked with that in mind.

## 7. Will it fit

Rough numbers, to be measured on the first build:

| Part | Size |
| --- | --- |
| fm1-base template | 77 KB |
| Album's synth and screen code, cut down | about 100 KB (a guess, to measure) |
| 9 pictures (8 stages and the hello), at Album's average | about 165 KB |
| A drum kit of 12 hits at 22 kHz, 4-bit (about 11 KB a second) | about 55 KB |
| The breaks as patterns | under 2 KB |
| Real breaks, two bars each at 174 (about 30 KB each), if the drummer happens | 240 KB for eight, in the data area |
| App slot / data area | 581 KB / 292 KB |

It fits without Bluetooth. Bluetooth MIDI costs 124 KB more, so it's a maybe. Whether the installer can write the data
area or the drums have to ride inside the app needs checking in fm1-base.

## 8. First steps

1. Answer the questions below.
2. Make the repo on fm1-base and get a blank build installing from a web page, as Album does.
3. One stage, end to end: a picture, a break on the kit, a Reese bass on the white keys, the slices on the black keys.
4. BUILD and the drop. Play it for people and watch their faces.
5. The other seven stages, then REC, then the moss.

## 9. Questions for Josh and the friend

1. Who is the friend, and what do they want to bring: tracks, photos, drawings, a drummer, their own sound?
2. Is this its own firmware, or Album 02?
3. Photos or drawings for the stages? If photos, whose, and are they of London?
4. Who is it for: people who already make DnB, or anyone who picks up an FM-1? It changes how much stays hidden.
5. Is there a drummer who'd record eight breaks?
6. 174 and A minor everywhere, or a tempo and key for each stage?
7. Is "Amethyst" staying? It could also be the name of the first stage, and the crystal on the hello.
