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
those seconds for a quick look.

The cast is all original friends. The look-alikes stay out of it.
