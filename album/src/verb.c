/* SPDX-License-Identifier: GPL-3.0-only */
/* ALBUM's reverb: a big, dark room. Four allpasses smear the input, then eight delay lines feed each other
 * through a Hadamard matrix (a feedback delay network). Each line has a low-pass in its loop, so the highs die
 * first and the tail never hisses, and each line's length drifts a few samples so the tail moves slowly.
 * The lines are int16 and need 2 x (VLEN_ALL + AP_ALL) = about 44 KB of RAM. */
#include "album.h"
#include "verb.h"

#define NL      8
#define MOD     12                     /* the drift, +- samples */
static const uint16_t LEN[NL] = { 1559, 1789, 2053, 2347, 2617, 2879, 3163, 3449 };
#define VLEN_ALL (1559 + 1789 + 2053 + 2347 + 2617 + 2879 + 3163 + 3449 + NL * (2 * MOD + 2))
static const uint16_t AP[4] = { 223, 347, 461, 587 };
#define AP_ALL  (223 + 347 + 461 + 587)
#define AP_G    20316                  /* 0.62, Q15 */

static int16_t line[VLEN_ALL], apb[AP_ALL];
static int16_t *base[NL], *apbase[4];
static uint16_t size[NL], wp[NL], apw[4];
static int32_t g[NL], lp[NL], damp;   /* g Q15, damp Q14 */
static uint32_t mph[NL], minc[NL];

void verb_init(void)
{
    int i;
    int16_t *p = line, *q = apb;
    for (i = 0; i < NL; i++) {
        base[i] = p, size[i] = (uint16_t)(LEN[i] + 2 * MOD + 2), p += size[i];
        wp[i] = 0, lp[i] = 0;
        mph[i] = 0x20000000u * (uint32_t)i;
        minc[i] = 2400u + 530u * (uint32_t)i;          /* 0.03 to 0.06 Hz, a little different per line */
    }
    for (i = 0; i < 4; i++)
        apbase[i] = q, q += AP[i], apw[i] = 0;
    for (i = 0; i < VLEN_ALL; i++)
        line[i] = 0;
    for (i = 0; i < AP_ALL; i++)
        apb[i] = 0;
    verb_set(4000, 3000);
}

void verb_set(uint32_t time_ms, uint32_t damp_hz)
{
    int i;
    if (time_ms < 200u)
        time_ms = 200u;
    for (i = 0; i < NL; i++)                              /* -60 dB after time_ms: 2^(-9.97 len / samples) */
        g[i] = (int32_t)(exp2_neg(14804u * LEN[i] / time_ms) >> 15);
    damp = 16384 - (int32_t)(exp2_neg(damp_hz * 13465u / 1000u) >> 16);
}

static inline int16_t sat16(int32_t x) { return (int16_t)(x > 32767 ? 32767 : x < -32768 ? -32768 : x); }

/* a smooth -1..1 from a phase, Q15 (a parabola per half: close enough to a sine for a drift) */
static inline int32_t tri_sine(uint32_t ph)
{
    int32_t x = (int32_t)(ph >> 16) - 32768;              /* -32768..32767 */
    int32_t ax = x < 0 ? -x : x;
    return (x * (32768 - ax)) >> 13;
}

void verb_process(const int32_t *in, int32_t *out, int32_t send)
{
    int i, j, k;
    int32_t back[NL];
    for (j = 0; j < NL; j++) {                            /* how far back to read, with the drift, Q8 samples */
        mph[j] += minc[j] * BLOCK;
        back[j] = LEN[j] * 256 + ((tri_sine(mph[j]) * MOD) >> 7);
    }
    for (i = 0; i < BLOCK; i++) {
        int32_t x = (((in[2 * i] + in[2 * i + 1]) >> 1) * (send >> 3)) >> 12;
        for (k = 0; k < 4; k++) {                         /* allpass smear */
            int16_t *b = apbase[k];
            int32_t d = b[apw[k]];
            int32_t w = x + ((d * AP_G) >> 15);
            x = d - ((w * AP_G) >> 15);
            b[apw[k]] = sat16(w);
            if (++apw[k] >= AP[k])
                apw[k] = 0;
        }
        int32_t y[NL];
        for (j = 0; j < NL; j++) {                        /* read each line LEN +- drift back, interpolated */
            int32_t r = (int32_t)wp[j] - (back[j] >> 8), fr = back[j] & 255;
            while (r < 1) r += size[j];
            int32_t a = base[j][r % size[j]], b = base[j][(r - 1) % size[j]];
            int32_t s = a + (((b - a) * fr) >> 8);
            lp[j] += ((s - lp[j]) * damp) >> 14;
            y[j] = lp[j];
        }
        /* Hadamard 8 x 8 by butterflies, then 1 / sqrt 8 */
        for (k = 1; k < NL; k <<= 1)
            for (j = 0; j < NL; j++)
                if (!(j & k)) {
                    int32_t a = y[j], b = y[j + k];
                    y[j] = a + b, y[j + k] = a - b;
                }
        for (j = 0; j < NL; j++) {
            int32_t h = ((y[j] >> 2) * 11585) >> 13;
            int32_t v = ((h * (g[j] >> 1)) >> 14) + ((j & 1) ? -x : x);
            base[j][wp[j]] = sat16(v);
            if (++wp[j] >= size[j])
                wp[j] = 0;
        }
        out[2 * i]     = (lp[0] - lp[2] + lp[4] - lp[6]) >> 1;
        out[2 * i + 1] = (lp[1] - lp[3] + lp[5] - lp[7]) >> 1;
    }
}
