# Rainbow Island, the film

A short 3D film for kids: Rainbow mode's friends spend a day on a floating island under a rainbow. Every friend is its own
48 x 48 pixel art, pushed out into little cubes and made thicker toward the middle. Every sound is the friend's own, played
by Rainbow mode itself in the browser build, and the speech bubbles show each note in the toy's colors with its letter.

The story, about 1 minute 50:

1. The Star rings each letter of RAINBOW MODE.
2. Ducky, Kitty, Bunny, Elephant, Bear, Frog and April arrive one by one and say hello in notes, then all together.
3. COPY ME: the Owl sings C D E G. The Frog gets the last note wrong (F#), everyone giggles, and the Frog gets it on
   the second try. YES! and confetti.
4. The Peacock rises on the hill and plays its harp while the island shimmers gold.
5. Beat Bot starts the DANCE beat and everyone takes a turn. The camera goes once round the island.
6. The sun sets, the Sheep floats in on a cloud and plays Brahms' Lullaby, and the friends fall asleep one by one.

`script.mjs` holds all of it: who sings which notes when, where everyone stands and the camera moves. The sound and the
picture both read it, so a note shows up in a bubble when it's heard.

## Making it

```sh
EMU_PREVIEW=0 sh web/emu/build.sh                           # (after ./build.sh once): build/emu/felucca.wasm
python3 tools/video/island/gen_pics.py                      # the cast's pictures and the toy's font -> pics.js
cd tools/video/island
npm install three@0.160.0
node audio.mjs ../../../build/emu/felucca.wasm soundtrack.wav
python3 -m http.server 8765 --bind 127.0.0.1 &              # world.html, for the browser
for k in 0 1 2 3; do node render.mjs $((k*833)) $(( k<3 ? (k+1)*833 : 3330 )) frames 1920 1080 & done; wait
ffmpeg -framerate 30 -i frames/f%05d.jpg -i soundtrack.wav -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest -movflags +faststart rainbow-island.mp4
```

The frames take about half a second each in software WebGL, so four browsers at once do the whole film in about
15 minutes. `renderAt(t)` draws any moment on its own, so `node stills.mjs st 1280 720 11.5 42.5 97` jumps straight to
those seconds for a quick look (`PAGE=halloween.html` for the second episode).

The cast is all original friends. The look-alikes stay out of it.

## Halloween

A second episode, about 1 minute 36, made at a young viewer's request "with all the spooky guys included". It's night on
the island under a big moon, with jack-o'-lanterns everywhere:

1. The Bat flies over and rings each letter of HALLOWEEN.
2. The spooky friends come out one by one: the Pumpkin lights up, the Ghost rises and glows, the Bat flaps in, the
   Spider drops on its thread, the Wolf leaps onto its rock and howls, then the Skeleton, Slimy (a loop-de-loop), the
   Flytrap (chomp) and the Scientist with a bubbling flask.
3. Ducky, Kitty, Bunny, Frog and April come trick-or-treating in the toy's hats (two wizard hats, a top hat, a crown
   and a cowboy hat). BOO! They jump, everyone laughs, and the Pumpkin throws candy.
4. Ghost's SPOOKY beat from the toy: the Skeleton, the Ghost, the Wolf, the Bat, the Flytrap and the Scientist take
   turns, then everyone plays together.
5. HAPPY HALLOWEEN, more candy, and the Owl's last hoo.

This one includes Skeleton and Slimy, which are drawn after film characters, because the request was for all of them.
Bat, Pumpkin and Spider are the toy's stand-ins (LOOK-ALIKES), so they sing in their look-alikes' sounds, as on the
toy: Bat on Skeleton's theremin, Pumpkin on Slimy's glitch, Spider on Web Hero's sync lead.

```sh
node audio.mjs ../../../build/emu/felucca.wasm halloween.wav halloween.mjs
for k in 0 1 2 3; do PAGE=halloween.html node render.mjs $((k*720)) $(((k+1)*720)) frames_h 1920 1080 & done; wait
ffmpeg -framerate 30 -i frames_h/f%05d.jpg -i halloween.wav -c:v libx264 -crf 24 -preset slow -tune animation \
  -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart rainbow-island-halloween.mp4
```

## The Bear and the Balloon

A third film, about 1 minute 43: the first Winnie-the-Pooh story (A. A. Milne, 1926), acted by Rainbow mode's Bear on a
new stage, a clearing in a wood. The story is Milne's (it's in the public domain in the US); nothing comes from the
Disney films. The Bear hears a buzz, climbs the honey tree, falls through the branches into the gorse bush, asks Robin
for a balloon (blue, like the sky), rolls in mud to be a little black cloud and floats up. Robin walks to and fro under
an umbrella ("tut-tut, it looks like rain"), the bees aren't fooled, Robin's popgun pops the balloon, the Bear comes down
slowly, and a butterfly lands on his nose: POOH!

New for it: Robin (a child drawn in the toy's style for the films, `kid()` in `gen_pics.py`, speaking on Flute Bird's
flute), the Bear covered in mud, the stage (the honey tree with its hole and branches, the gorse bush, Robin's cottage,
the puddle, the wood round the clearing) and the props (two balloons, an umbrella, a cork popgun, a swarm of bees).
School Bus's toms bump him down the tree, Toy Drum does the crack and the pops, the Scientist's squelch is the mud, and
Rainbow's cloud pad plays softly underneath.

`common.js` holds what the films share. The speech bubbles are laid out from the inside out: each note's head, stem,
flag and letter, then the same padding on all four sides. All three films use them.

```sh
node audio.mjs ../../../build/emu/felucca.wasm honey.wav honey.mjs
for k in 0 1 2 3; do PAGE=honey.html node render.mjs $((k*773)) $(( k<3 ? (k+1)*773 : 3090 )) frames_p 1920 1080 & done; wait
ffmpeg -framerate 30 -i frames_p/f%05d.jpg -i honey.wav -c:v libx264 -crf 24 -preset slow -tune animation \
  -pix_fmt yuv420p -c:a aac -b:a 160k -shortest -movflags +faststart the-bear-and-the-balloon.mp4
```
