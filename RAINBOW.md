# Rainbow mode

This fork of Felucca turns the FM-1 into a music toy for young children. It starts in Rainbow mode every
time it powers on, with a hello in bouncing rainbow letters and confetti that greets the child by name, for a few
seconds or until a button or key is pressed. A grown-up can get back to the full Felucca by holding **HOME and
SAVE together for 3 seconds**. That brings back the music of your last session: Rainbow mode never
writes Felucca's autosave, so playing with the toy can't overwrite your own work. Rainbow mode comes back
at the next power-on.

## What everything does

| Control | What happens |
| --- | --- |
| Keys | Play the friend's sound. The note's letter shows big in the band at the bottom, in its own color, and the friend hops. A music staff drops in at the top and writes the note (see below). |
| PRESETS | Next or previous friend (94 of them, and a secret one; each with its own picture, sound, home sky and favorite beat). |
| ALGORITHM | How the keys play, one step per turn (below): 1 FRIEND, 3 FRIENDS, STRUM, ACCORDION, GUESS, FOLLOW, CHORDS, COPY ME. |
| SELECT | The beat slower or faster (SLOW, WALK, FAST). |
| KNOB 1 | Big and small. Low notes make a big friend, high notes a small one. OCT- and OCT+ do the same. |
| KNOB 2 | Day to night. The sky darkens, the sun sets, the moon comes out, and the sound gets softer and darker. |
| KNOB 3 | Echo. The sound repeats, and copies of the friend follow it around. |
| KNOB 4 | Wiggle. The sound wobbles (vibrato) and so does the friend. |
| FX | Tap: HICCUP. The sound stutters and the friend shakes. |
| SCL | Tap: BACKWARDS. The sound plays in reverse and the friend turns round. |
| ENV | Tap: SLEEPY. The sound winds down like a record player each time a note is played, and the friend droops and dozes. It wakes up by itself after 3 seconds. |
| LFO | Tap: SQUEAKY. Everything an octave up, and the friend shrinks. |
| EDIT | Tap: GIANT. Everything an octave down, and the friend grows. |
| GLO | Tap: FREEZE. The sound freezes in place and the friend turns to ice. |
| | The top row's effects turn on with a tap and off with another (one at a time; the lit button shows which). HICCUP, BACKWARDS, SLEEPY and FREEZE start again on every new note, so a key pressed after the tap always sounds. |
| PLAY | Starts and stops the beat: drums and a bass line that is always in key, so anything played fits. The friend dances. |
| SEQ | The next beat (21): DANCE, MARCH, SPOOKY, ROCK, DISCO, HIP HOP, TRAIN, SAMBA, REGGAE, LULLABY, HOEDOWN, LOFI, ACID, POLKA, BOSSA, FUNK, SKA, TRAP, SALSA, SHUFFLE, BREAK (Felucca's own drum loop, played back as it was made, at 120 BPM). |
| ARP | Sparkle: a held key plays up and down by itself. In ACCORDION it has three settings, one a press: SPARKLE TUNE (the white keys sparkle while the black keys' chords hold steady), SPARKLE ALL (the chords sparkle too) and off. |
| REC | The next sky (rainbow, stars, hearts, bubbles, flowers, confetti, clouds, snow, autumn leaves, desert, the street, under the sea, rain, fireworks, and the secret northern lights), with confetti. |
| HOME | A surprise friend, with confetti. Held for 1 second it opens the grown-ups' VOLUME instead (below). |
| SAVE | WRITE: write your own song (below). SAVE again goes back to playing. |
| HOME held 1 s, then OCT- / OCT+ | The grown-ups' VOLUME: the most the MASTER knob can give (below). |
| HOME held 1 s, then ALGORITHM | The grown-ups' NAME: the name the hello greets (below). |
| HOME held 1 s, then KNOB 4 | The HAT: ten hats (party, crown, top hat, rainbow bucket, wizard, beanie, western, chef, propeller, flowers) any friend can wear, or none; the band names it. Kept over power-off. Each friend's hat sits on whatever counts as its head (found from the picture: the first row wide enough to be a head, so ears, horns and a whale's spout are passed over; a few placed by hand), sized to that head, and may rise above the picture. (On the SMK-37: not yet.) |
| HOME held 1 s, then KNOB 3 | The STARS (below): how far the next secret is. |
| HOME held 1 s, then PRESETS | The grown-ups' LOOK-ALIKES: left swaps the friends drawn after TV and film characters for original stand-ins, right brings them back (below). |
| MASTER | Volume, up to the VOLUME the grown-ups chose (about half, unless changed). |

## ALGORITHM: how the keys play

| Setting | What the keys do |
| --- | --- |
| 1 FRIEND | Each key plays its note. |
| 3 FRIENDS | Each key plays the major chord built on it, black keys too, and three friends sing. D plays D major (D, F#, A), C# plays C# major. Not every chord is in key, and that's the fun: some pairs sound like magic (C, then A#, then C, or C then E), and finding them is the game. The band shows the chord: its letters in their colors and its name. Friends whose sound is one note at a time (a lead or a bass, like VACUUM or T-REX) sing the whole chord here, and in STRUM and ACCORDION too; in 1 FRIEND they keep their one-note slide. |
| STRUM | Like an Omnichord (an idea from u/veecheech, after dxsloop's arp mode). A black key picks a chord, the one on the white key just below it: F#: F, G#: G, A#: A minor, C#: C, D#: D minor (C to begin with), and plays its root low. The white keys, left to right, play that chord's notes upward, so a hand drawn across them strums it. The band shows the chord. (Not with the drum friends, whose keys are drums.) |
| ACCORDION | A black key plays a whole chord while it is held (the same chords as STRUM: F, G, A minor, C, D minor), and the white keys play their own notes, so one hand can play a tune over the chords. Each row of black keys voices them differently: the lowest (F#3 to D#4) plays plain triads, the next (F#4 to D#5) jazz ninths (Fmaj9, G9, Am9, Cmaj9, Dm9: root, 3rd, 7th and 9th), and the top key (F#5) a stack of fourths on F (F B E A, the "So What" sound). On friends whose engine plays three notes at a time (PHYS, GRAIN) the ninths become jazz shells (root, 3rd, 7th). The band shows the chord's letters and name and the staff writes it. |
| GUESS | An ear game (an idea from u/nutty_cartoon). A friend sings a note and the band shows ?. The right key: YES! and confetti. Another key: TRY AGAIN, with no sound of its own, and the friend sings the note again; after two tries the right key blinks. It starts with C and G and adds a note after three right in a row (C G E D A F B, then high C). PLAY: hear it again. |
| FOLLOW | Songs to learn (u/nutty_cartoon). The next note's key lights and the band shows its letter; the song is played at the child's own pace, and a wrong key changes nothing. At the end, a party, and it starts again. SEQ picks the song: Twinkle Twinkle, Mary Had a Little Lamb, Hot Cross Buns, Row Your Boat, Old MacDonald, Frere Jacques, London Bridge, Ode to Joy, Jingle Bells, Happy Birthday, Itsy Bitsy, Yankee Doodle, Oh Susanna, Amazing Grace, Silent Night, Joy to the World, Au Clair de la Lune (all old and free). |
| CHORDS | Chord lessons (u/Yablan on r/MVaveFM1). The next chord's keys light up and the band shows its letters and name; holding exactly those keys plays it, says YES! and lights the next. Four chords make a lesson, and a party comes at the end of each round. SEQ picks the lesson: FIRST CHORDS (C F G C), POP FOUR (C G Am F), SEVENTHS (Cmaj7 Am7 Dm7 G7), LOFI (Fmaj7 Em7 Dm7 Cmaj7) and LOFI JAZZ (Dm9 G13 Cmaj9, rootless, the way lofi keys are played). Each is voiced so the hand barely moves. PLAY starts the slow, swung LOFI beat: each chord gets a bar, the bass plays its root, and the next chord blinks a beat early. |
| COPY ME | A memory game. The friend plays two notes (the band says LISTEN and each key lights as it plays), then the band says YOUR TURN and the child plays them back on the five keys C D E G A. Right: YES! and a party, and the friend adds a note. A wrong key says TRY AGAIN and the friend plays it again; after three misses in a row the pattern gets one shorter. Eight notes in a row earns a STAR! and a fresh start. PLAY hears the pattern again. |

Each setting has a picture, for children who do not read yet: a smiling face, three singing friends, a harp, an accordion, a
speech bubble with a note and a question mark, piano keys with one lit, and two bubbles trading notes. It shows beside the setting's name when ALGORITHM turns,
and stays at the left of the band while any setting but 1 FRIEND is on.

In every setting, keys held together show their letters in their colors and, when it has one, the chord's name (MAJOR, MINOR,
SEVEN, DIM, SUS), whatever their order (u/nutty_cartoon). GUESS and FOLLOW keep the keys at their own notes (OCT 0).

A win has a sound too: when GUESS is right, a COPY ME round is played back, a FOLLOW song or a CHORDS lesson is finished, the
friend plays a little cheer up the C chord (two notes for a small win, four for a whole song, lesson or STAR!). A new friend (a
surprise from HOME) or a new sky (REC) gets the small one. The drum, bass and noise friends stay quiet, as their notes are no tune.

## Stars and secrets

Every game won earns a star: a right GUESS, a COPY ME round played back, a FOLLOW song or a CHORDS lesson finished. The count
is kept over power-off (written at every tenth star, at each secret, after half a minute without a win and when leaving Rainbow mode, so
the flash is not written at every win; a power-off in between loses at most nine stars). Some things wait
for stars:

| Stars | What opens |
| --- | --- |
| 10 | An eleventh hat, the STAR hat. It goes on at once; it joins the round on HOME held 1 s, then KNOB 4. |
| 25 | A secret sky, the northern lights (green and violet ribbons waving over stars). It is the sky at once, and joins REC's round from then on. |
| 50 | A secret friend, GOLD DUCKY (a crown and sparkles; a rock organ). It is there at once, and joins PRESETS from then on. |

The band says NEW HAT!, NEW SKY! or NEW FRIEND! and the friend plays the four-note cheer. HOME held 1 s, then KNOB 3, shows STARS and a
meter of how far the next secret is (there are no digits in the band's font). To start over, the grown-ups can erase the
FM-1's settings (the same as for the name and the hat). The SMK-37 counts stars too, but cannot show them yet.

## Drum friends

Scissors, Beat Bot, Toy Drum, Bongo and Monkey play drum kits: every key is a different drum (Felucca's GM drum map). For them the
band shows the drum's name (KICK, SNARE, CLAP, HI-HAT, OPEN HAT, TOM, CONGA, RIM, CLAVE, COWBELL, CYMBAL) in its own color instead of
a note letter, the staff stays quiet (drums are not notes on it), 3 FRIENDS plays one drum a key, and KNOB 1 / OCT only change the
friend's size: each key always plays the same drum. In WRITE their notes are written as the drums their keys play.

## How loud everything is

The friends were leveled by ear-loudness, not by peak: each one played the same phrase in the browser build and was measured
with the broadcast loudness method (ITU-R BS.1770, K-weighted, gated), then its P_LEVEL moved toward the middle (half a dB a
step). They had spread over 12 dB (a long organ note sounds far louder than a pluck with the same peak); now they are within about
3.5 dB. The thirteen beats were leveled the same way (now within half a dB of each other, about 4 dB under a friend). Three friends
singing (3 FRIENDS) play 2.5 dB softer and the ACCORDION's chords softer too, so a chord is about as loud as one note.
`web/emu/kid_test.mjs` checks the friends stay within 7 dB of each other on its own simpler measure.

## The staff

When the child plays, a treble clef and five lines drop in at the top of the screen and write the notes as colored heads (the color of the
letter in the band), left to right, up to 8 of them; the oldest drops off. Keys played together, or a key with ALGORITHM on (three friends), stack as a chord. A
black key gets a sharp sign, notes below the staff get their ledger lines, and **8VA / 8VB** (or 15MA / 15MB) shows over or under the
staff when OCT or KNOB 1 has moved the keys an octave or two up or down. Each note also shows how long it was held, against the beat: a quick tap is a sixteenth (a stem and two flags), then an eighth, a
quarter (about one beat), a half (an open head, about two beats) and a whole (an open head with no stem). The note grows through them
while the key is held, so a long sound can be seen to become a long note (suggested by u/theskyisfalling1 on r/MVaveFM1). The staff is
in 4/4 (shown after the clef) and draws a barline each time the written notes fill four beats; a note that runs past the bar gets the
line after it (a toy's staff writes no ties). WRITE's big staff has barlines too, every four columns (a column is a beat). It goes
after 6 seconds of quiet and starts again from the left. The big
letter stays in the band. The clef is the treble clef of the FreeSerif font (GNU FreeFont, GPL-3.0 or later), scaled down to a bitmap in
`tools/gen_kid_art.py`.

## WRITE: your own song

An idea from u/lastapoc on r/MVaveFM1 ("Mario Paint music mode"): SAVE opens a big staff for writing a song with the
friends, the way Mario Paint's composer did, and plays it back.

| In WRITE | What happens |
| --- | --- |
| Keys | Write a note in the yellow column (a drum friend's keys write its drums, as they play them): the friend being written with, in a ball of the note's color. It plays as it lands, and the column moves on when the key is let go. Two keys together make a chord (two notes in a column). The same key again takes its note out. |
| PRESETS | The friend to write with (shown in the band). A song has a band of up to three friends; a fourth takes the place of the one used least (its notes become the new friend's). |
| OCT- / OCT+ | The yellow column back and forward (32 columns, 4 pages of 8: the dots). |
| HOME | Wipes the column (held 1 s it is the grown-ups' VOLUME, as always). While the song plays, it wipes the column that is playing. |
| PLAY | Plays the song from the start, in a loop: the column turns green and the friend of each note hops along over it. PLAY again stops. On a song with nothing written yet, the loop is two bars, to play into (below). |
| Keys, while it plays | Loop and layer: a key is written where the beat is (into the nearest column), and is heard the next time round. The band says LOOP. PRESETS picks another friend for the next layer (up to three friends, two notes a column). A note is only added while it plays; HOME wipes the column being played. |
| SEQ | A beat under it: none, then each of the 21 (drums only). |
| SELECT | Slower or faster. |
| REC held 2 s | A new, empty song. |
| SAVE | Back to playing. |

The song is kept when the FM-1 is switched off: in 58 bytes of the settings that no engine uses (`favorites.factory[14]` and
`[15][0..25]`), so it never touches your projects or the autosave. It is written about 4 seconds after the last change (while
stopped) and when WRITE is left. A column is a beat (a quarter note); each friend plays on its own track (tracks 1 to 3, the
drums on 4), through Felucca's own sequencer.

## Volume, for grown-ups

Two guards, both in `kid.c` (`kid_master`):

- **Your maximum.** Hold **HOME for 1 second**: the band says VOLUME and shows eight dots. While HOME is still down, **OCT-** steps it
  down and **OCT+** up. Step 6 is the old "about half" and is where it starts; step 8 lets the MASTER knob go
  all the way, step 1 is very quiet. It is kept when the FM-1 is switched off. Let go of HOME and nothing else happens (no surprise
  friend). A shorter HOME press, and OCT- / OCT+ without HOME, do what they always did.
- **A limiter that follows it.** The FM-1 already had a peak limiter; in Rainbow mode its ceiling now moves with the volume (15 times the
  MASTER level it is at, never above the old fixed ceiling, and it catches every peak at once), a little above what a plain chord over a beat peaks at. So an effect that makes the sound louder
  (GIANT, FREEZE, echo, a chord on a beat) is held to the level already heard. Outside Rainbow mode the limiter is as it was.
- **Warmer for small speakers and headphones.** In Rainbow mode the highs are softened about 4 dB above ~3.3 kHz (the
  2.5 to 8 kHz band is the sharp one on a small speaker), each key also plays a quiet sub octave on track 3 (a soft
  triangle an octave under its lowest note, following the friend's envelope; not for the bass, drum and noise friends,
  STRUM, ACCORDION's chords apart or WRITE), the brightest friends are toned down, and the driest get a little reverb.

## Look-alikes, for grown-ups

Some friends are drawn after characters from TV and films. They are original drawings, but a parent may not want them (an idea from
u/ReallyLongLake on r/MVaveFM1). Hold **HOME for 1 second** and, while it is still down, turn **PRESETS left**: the band says
LOOK-ALIKES OFF, and each of them is replaced by an original stand-in with the same sound, sky and beat, so nothing is lost:

| Look-alike | Stand-in |
| --- | --- |
| Blue Pup | Spotty Pup |
| Red Pup | Fox |
| Red Monster | Fuzzy (one eye, little horns) |
| Blue Monster | Big Blue (short horns, two teeth) |
| Web Hero | Spider |
| Slimy | Pumpkin |
| Yellow Bird | Chick |
| Skeleton | Bat |
| Rancher | Horse |
| Rodeo | Cactus (in a western hat) |
| Space Hero | Alien |
| Spider Mom | Rainbow Mom (long hair and a rainbow headband) |
| Spider Grandma | Green Granny (silver curls, round glasses, a green cardigan) |
| Fairy Monster | Pixie (a leaf hat and lilac wings) |
| Grouch | Alley Cat (smiling out of a can) |
| Tiger Cub | Lion Cub |
| Raccoon | Squirrel (with an acorn) |

Turn **PRESETS right** the same way to bring the originals back. The choice is kept when the FM-1 is switched off (the top bit of the
VOLUME's byte). Songs in WRITE are untouched; their notes just show the stand-ins. The list is `STAND_INS` in
`tools/gen_kid_art.py` (the generator writes `KID_ALT`, used by `kid_art` in `firmware/src/kid.c`).

Note colors follow the colored tubes and bells used in many early music classes: C red, D orange,
E yellow, F green, G teal, A purple, B pink. Sharps get the color in between.

## The friends

Ducky, Pink Ducky, Cool Ducky, Axolotl, Unicorn, Giraffe, Goo, Goobert, Blue Pup, Red Monster,
Blue Monster, April (a dog), Scissors, Ghost, Web Hero, Butterfly, Kitty, Frog, Robot, Rainbow,
Princess Ducky, Red Pup, Yellow Bird, Slimy, Bunny, Panda, Penguin, Owl, Bee, Ladybug, Dino, Whale,
Octopus, Fish, Turtle, Ice Cream, Cupcake, Rocket, Strawberry, Star, and six suggested by u/veecheech on r/MVaveFM1:
T-Rex (a growly bass), Skeleton (a theremin: a sine with a wide vibrato that slides between notes), Rancher and Rodeo (twangy
plucks, and their own beat, HOEDOWN) Vacuum (the rave "hoover" sound, a joke for the grown-ups) and Space Hero (three buzzy saws that swoop into each note). See CREDITS.md.
Then four more drum kits, every key a different drum like Scissors, each one of Felucca's model kits: Beat Bot (the 80 kit, a
classic drum machine), Toy Drum (the 55 kit), Bongo (the 66 kit, congas) and Monkey (the 10 kit, a cymbal on the bell).
Then eight with the Sequential Prophet-5's classic sounds, made with Felucca's own engines (the nudge was Melodee's PROPHET
engine, another Felucca fork; none of Sequential's own programs are used): Elephant (poly brass), Race Car (the sync lead's sweep:
TRIO's SYNC with the envelope moving the second oscillator), Jellyfish (strings), Bear (a punchy saw bass), Snowman (glassy ring-mod
bells, like the Prophet's Poly-Mod), Crab (a snappy clav), Wolf (a howl that swells and slides) and Camel (a big, loping lead). Their
tweaks on top of the presets are the `TW_*` lists in `kid.c`. Four new skies came with them: clouds, snow, autumn leaves and a
desert at sunset. Four more came later, all drawn from a formula, so they use no memory for pictures: under the sea (light from above,
bubbles rising, swaying seaweed and a sandy floor; the sea friends' home), rain (a grey sky, streaks falling, ripples in the puddles;
Frog's home), fireworks (bursts of sparks in turn over a night sky; Rocket's home) and the secret northern lights.
Then three acid friends (u/litomanu asked for 303 sounds) on ANALOG's ACID, the squelchy resonant bass of a Roland TB-303:
Scientist (set as a TD-3, the 303 clone, often is: saw, cutoff low, resonance high, a strong envelope, a short decay; hold a key
while pressing the next and it slides into it in about 60 ms, as a 303 does), Flytrap (a driven square wave: a chomp, sliding the
same way) and Sunflower (a softer acid line with an echo; every note slides from the last, no need to hold keys over). Their
favorite beat is ACID: four on the floor, and Felucca's own acid line (A minor, with accents and slides of about 60 ms) played on
the ACID sound. All the friends' slides use Felucca's TIME glide (a slide takes the same time whatever the interval); its RATE
glide at small values slides in a few milliseconds, too fast to hear.
And some designed at home: Spider Mom (the classic web hero's mask in rainbow stripes, with long dark brown
hair; PHASE's RESO, ringing on) and Dragon Duck (a duck with horns, a bat wing and a puff of fire; VOICE's VOX LEAD with a growl). Then
Goobert went blue and squishy (ANALOG's PLUCK on a square wave through a ringing filter that pops open and
settles, with a little wobble), and a sky came with all the monster friends: the street, after a famous one on children's TV.
Two brick houses, a stoop, a lamp post and a trash can, with Blue Monster, Yellow Bird and Red Monster in the windows,
Goobert in the doorway, Goo on the steps and Slimy peeking out of the can. The friend being played is out on the
sidewalk, so its own spot is empty; at night the windows and the lamp light up. It is Red Monster's, Blue Monster's and
Yellow Bird's home sky, and with LOOK-ALIKES off the stand-ins move in instead. And Cool Ducky went green, in a rainbow bucket hat and
shades.

A second batch: Spider Grandma (a green web-hero mask with silver curls, a bun and pearls; WHEEL's GOSPEL organ),
Night Light (drawn from an axolotl night light: white, with mint gills, hugging a mint egg; ANALOG's SOFT PAD, a
soft glow), Green Queen (the night light as a green queen in a gold crown and a rainbow cape; PHASE's STRING), King
Axolotl (green, on a rainbow throne in red and green robes; FM6's BRASS fanfare), Fairy Monster (a pink fairy monster
with pigtails, little wings and a star wand, who moved in next door on the street; TRIO's RING BELL pitched up into a twinkle) and Morning Glory (a
vine with heart-shaped leaves and purple trumpet flowers; ANALOG's WIND, a breathy flute). Spider Grandma and Fairy Monster are
look-alikes, with Green Granny and Pixie as their stand-ins.

And a third: Grouch (a grumpy green monster in a trash can, lid on its head; TRIO's FAT BASS with a growl; it lives in
the street's can now, and Slimy moved into a window), Tiger Cub (in a red zip-up sweater; PHASE's ORGAN, bright and reedy, and the TRAIN
beat, for the trolley), Raccoon (with a box of collected treasures; PHASE's WIRE, under the stars) and Goldenrod
(a prairie flower: golden plumes on tall stems; ANALOG's STRINGS and HOEDOWN, for the prairie). Grouch, Tiger Cub and
Raccoon are look-alikes, with Alley Cat, Lion Cub and Squirrel as their stand-ins.

And three that play real recordings: Piano Pal, Flute Bird and Sax Cat use SAMPLE, the piano, flute and sax sets Felucca carries
(about 104 KB of its flash, which no friend used before). The drum break of SLICE (22 KB) is the one piece left over.

And a fourth, in sets. The farm: Cow (PHYS's DRONE STRING, a low moo of a drone), Pig (FM6's ORGAN) and Sheep (ANALOG's PWM STR,
fluffy strings). The sea: Shark (FM6's FM BASS), Seahorse (FM6's BELL with its modulators' ratio up: glassy) and Starfish (PHYS's
BOWED METAL, a singing bowl). Bugs: Snail (a slow, soft sine), Caterpillar (ANALOG's PLUCK on a square wave: a boop) and Firefly
(FM6's TINE EP, brighter and short: a ping). Dinosaurs: Triceratops (ANALOG's BRASS on a driven square: a tuba's honk) and
Stegosaurus (FM6's BRASS through another algorithm: gritty). Food: Pizza (FM6's MARIMBA through another algorithm), Donut (a wide
FM6 PAD) and Banana (a slow, boingy FM6 PLUCK). Things that go: Train (the last of Felucca's drum kits, 77, every key another drum),
Fire Truck (a square-wave siren: a wide vibrato and a glide), School Bus (PHYS's TOMS, a marching band) and Helicopter (NOISE's
WIND, a rotor's whoosh). The vehicles have no faces: a driver, a pilot or a bus full of friends smiles from the windows. Only the
Train, the Helicopter and Shark play no cheer, as their notes are no tune; the rest do. Every one is leveled with the others
(`web/emu/kid_test.mjs`, and by a K-weighted loudness over a phrase), and none is closer in sound to an older friend than the older
friends are to each other.

Each one uses one of Felucca's own factory sounds (listed in `firmware/src/kid.c`, `KID_SOUND`), with its
level set so they all play at about the same loudness. Each also has a home sky and a favorite beat
(Ghost and Slimy: SPOOKY, a ghost-hunting funk; Frog and Axolotl: REGGAE; Butterfly and Rainbow: LULLABY). Scissors
plays the drum kit: every key is a different drum.

The pictures are drawn on a roomy canvas, then trimmed, centred and stood on the bottom of a 48 x 48 grid;
a picture that would not fit stops the build, so none is ever cut off. On the screen they are drawn at 1x,
1.5x, 2x, 2.5x or 3x (KNOB 1) and kept inside the screen even at their biggest, hopping and wiggling.
They are stored a row at a time as runs of one colour (`KID_RLE`: 54 KB for all 112 pictures, friends and stand-ins, from 129 KB), and
`kid_row` in `kid.c` decodes a row as the screen is drawn, keeping the last 16 rows (about 800 B of RAM).

The characters are original drawings in the spirit of the ones children love, not copies, because this
repository and its website are public.

## Where it lives

- `installer-pin.txt`: a rollback switch for the public installer. A run number in it makes the site's installer offer that earlier
  run's firmware instead of the newest build (nothing is deleted; the browser version and the private installer stay on the newest, and
  the landing page says so while it is pinned). Empty it and push to follow the newest again.
- `tools/gen_kid_art.py`: the 95 pictures (94 and a secret), drawn from shapes on a 48 x 48 grid and outlined
  automatically. `python3 tools/gen_kid_art.py /tmp/kid_art.h --png /tmp/sheet.png` writes a contact
  sheet to look at. The build runs it (`tools/build.py` generate).
- `firmware/src/kid.c`: everything else (sounds, knobs, buttons, the screen). It takes over the main
  loop's frame while it is on (`firmware/src/main.c`). Build with `FELUCCA_KID=0` to leave it out.
- `web/emu/kid_test.mjs`: checks it in the browser build (`node web/emu/kid_test.mjs build/emu/felucca.wasm`).
- `landing/`: the site's front page (the one link to share): a demo video, screenshots, the friends and how to try it. The workflow
  copies it to the site's root and fills in the site's address.
- `.github/workflows/rainbow.yml`: GitHub builds the firmware and the browser version on every push to
  `main`, tests the browser version, and publishes both to this fork's GitHub Pages site:
  `/webapp/try/` plays it in the browser, `/webapp/installer/` puts it on the FM-1.

## A tip link on the website

The landing page has a "Say thanks" card with a tip button when the repository has a variable (or a secret) called `DONATE_URL`
(**Settings → Secrets and variables → Actions → Variables tab → New repository variable**), set to an `https://` link such as a
Ko-fi or Buy Me a Coffee page. Without it, or with anything that is not an `https://` link, the card is left out. Change it any time
and re-run the workflow (or push anything) to update the site.

## The name in the hello

Anyone can put a name in the hello, right on the FM-1: hold **HOME for 1 second, then turn ALGORITHM**. A YOUR NAME screen
opens with ten places. Turn **PRESETS** to pick the letter in the lit place (a space, then A to Z), turn **ALGORITHM** for the
next place or the one before, and press **SAVE** to keep it: the hello plays at once, greeting the name, and does at every
power-up from then on. **HOME** leaves without changing anything. To take the name away, make every place a space and SAVE.
The name is kept in a few spare bytes of the settings (`favorites.factory[13][20..30]`, `kid_name_*` in `kid.c`), so it
survives power-off, and it goes before a name the build has (below).

It can also be set from the website: the installer page has a name box. The name goes over USB to the FM-1 only
(the editor's NAME, cmd 50: ten letters or spaces; the reply is the result and the name kept), never to a server, and
the page keeps nothing. Typed before installing, it is sent once the install is done; sending it empty takes the name
away. Double Rainbow has the same command and keeps its name in the same bytes. `web/test_name_page.py` checks the box
against a fake FM-1 in Chromium.

## The private installer

No child's name is in this repository, and the installer on the public site has none built in: its hello is a plain HI!
(the same as the browser demo) until someone sets a name on the FM-1 (above). Two repository secrets (**Settings → Secrets and variables → Actions**) add a second, named build:

- `KID_NAME`: the name the hello greets, capitals only, at most 10 letters (`tools/gen_kid_art.py` reads it).
- `PRIVATE_PATH`: a long random word, 12 to 64 letters, digits, `-` or `_`.

With both set, the workflow builds a second firmware package that greets by name and puts its installer at
`https://USER.github.io/REPO/PRIVATE_PATH/`. That address is not linked from anywhere and is marked noindex, but it is not password
protected: anyone who learns it can open it, so it is for your own use, not for posting. The name is held scrambled inside the
firmware package (the FM-1's package format encodes the app), not as readable text, and GitHub hides both secrets in its logs.
With only one of them set, there is no private build.

## The greeting on a real FM-1

It was choppy on the first real FM-1 (a full-screen redraw every frame, with outline lookups for every pixel). Now the letters skip rows
they are nowhere near, and the whole greeting is computed in 2 x 2 blocks: in the browser build it costs about 7 times less (roughly 45
ms of CPU per second of device time on top of an idle screen, against about 345 before). It needs a check on the device. If it is
still not smooth: draw the still parts (sky, rainbow, grass) once and redraw only the letters, the friend and the confetti, or fewer confetti.

## Not checked yet on a real FM-1

- Drawing speed. The screen has no frame buffer, so moving pictures are drawn in strips. Animated skies
  (stars, hearts, bubbles, confetti, and the sea, rain, fireworks and northern lights, which do more work for each pixel)
  redraw the whole picture area, about 60 ms a frame over the screen's
  connection. If it feels slow on the device, the first thing to try is drawing only the friend's area.
- The volume steps (`KID_VOL_CAP` in `kid.c`, 8 steps of about 3 dB) and the limiter's ceiling (`KID_LIM_X2`): check that the middle steps feel right on the speaker and the headphones.
- The staff drawing on the animated skies (it adds the panel's pixels to each redraw).
- Loop and layer in WRITE: a key lands in the nearest beat's column, judged from the screen's frame clock, so on the device a
  frame's delay (about 30 ms) is the most it can be off. If notes land a column late at fast tempos, the rounding point
  (the half beat, `kw_notes`) is the thing to move.
- The BREAK beat: SLICE's break played a slice a step. It sounds right in the browser; on the device the first thing to listen for is
  a click where one slice ends and the next begins.
- The stars are written to the settings every tenth star and after half a minute of quiet (`settings_save`, which waits for the beat
  to stop). Settings writes are flash erases (about a hundred thousand are promised), so it is worth a look at how often that is
  in real use.

## The installer, after Album 01's

The installer (`web/index_pkg.html`, `web/fm1ota.js`) took four things from Album 01's (fm1-base, Charles Vestal): a
check before installing (don't unplug, back up first), a clear message when the FM-1 runs M-VAVE's Open firmware (it
takes only M-VAVE's own firmware, so the official firmware has to go back on first), a list to find an FM-1 that the
computer shows under another port name, and m-bootloader after the firmware (`web/m-bootloader/`, FM-1 packages only).
The m-bootloader option stays hidden until it has been tried on an FM-1 running Rainbow mode: add `?mboot` to the
installer's address to see it. Double Rainbow's installer has the same.
