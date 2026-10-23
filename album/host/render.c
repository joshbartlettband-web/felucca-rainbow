/* SPDX-License-Identifier: GPL-3.0-only */
/* Renders a patch to a WAV file on a computer, with the FM-1's own sound code, to listen to before
 * building the firmware.
 *   cc -O2 -I../src -o render render.c ../src/album.c ../src/verb.c ../src/patches.c
 *   ./render 0 wing.wav */
#include <stdio.h>
#include <stdlib.h>
#include "album.h"

/* the demo: four held chords, voiced like open guitar chords, then a slow line on top of the last one.
 * time in seconds, note (MIDI), velocity (0 = off) */
typedef struct { float t; uint8_t note, vel; } Ev;
#define CH(t, a, b, c, d, len) {t,a,96},{t,b,90},{t,c,90},{t,d,84},{t+len,a,0},{t+len,b,0},{t+len,c,0},{t+len,d,0}
static const Ev SCORE[] = {
    CH(0.0f, 52, 59, 66, 68, 4.4f),        /* E add9 */
    CH(4.5f, 61, 64, 68, 71, 4.4f),        /* C#m7 */
    CH(9.0f, 57, 64, 68, 71, 4.4f),        /* A maj7 */
    CH(13.5f, 59, 64, 66, 71, 4.4f),       /* B sus4 */
    {18.0f, 52, 90}, {18.0f, 59, 84}, {26.0f, 52, 0}, {26.0f, 59, 0},
    {18.6f, 71, 100}, {20.4f, 71, 0}, {20.4f, 68, 92}, {22.2f, 68, 0},
    {22.2f, 66, 88}, {24.0f, 66, 0}, {24.0f, 64, 96}, {26.0f, 64, 0},
};
#define SECONDS 32.0f

static void put32(FILE *f, uint32_t v) { fputc(v, f); fputc(v >> 8, f); fputc(v >> 16, f); fputc(v >> 24, f); }
static void put16(FILE *f, uint16_t v) { fputc(v, f); fputc(v >> 8, f); }

int main(int argc, char **argv)
{
    int patch = argc > 1 ? atoi(argv[1]) : 0;
    const char *path = argc > 2 ? argv[2] : "out.wav";
    uint32_t frames = (uint32_t)(SECONDS * FS) / BLOCK * BLOCK, done = 0;
    int16_t buf[2 * BLOCK];
    size_t e = 0, ne = sizeof SCORE / sizeof SCORE[0];
    FILE *f = fopen(path, "wb");
    if (!f)
        return 1;
    fputs("RIFF", f); put32(f, 36 + frames * 4); fputs("WAVEfmt ", f);
    put32(f, 16); put16(f, 1); put16(f, 2); put32(f, FS); put32(f, FS * 4); put16(f, 4); put16(f, 16);
    fputs("data", f); put32(f, frames * 4);

    album_init();
    album_patch(patch);
    for (; done < frames; done += BLOCK) {
        float now = (float)done / FS;
        /* the score is in time order per chord; scan all of it for events due this block */
        for (e = 0; e < ne; e++)
            if (SCORE[e].t <= now && SCORE[e].t > now - (float)BLOCK / FS) {
                if (SCORE[e].vel)
                    album_note_on(SCORE[e].note, SCORE[e].vel);
                else
                    album_note_off(SCORE[e].note);
            }
        album_render(buf, BLOCK);
        for (int i = 0; i < 2 * BLOCK; i++)
            put16(f, (uint16_t)buf[i]);
    }
    fclose(f);
    printf("%s: %s, %.1f s\n", path, PATCHES[patch].name, (double)frames / FS);
    return 0;
}
