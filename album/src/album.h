/* SPDX-License-Identifier: GPL-3.0-only */
/* ALBUM: a firmware for the M-VAVE FM-1 made of twelve patches, each one a photo and a sound, after
 * My Bloody Valentine's "m b v" (2013). Nothing tinny or harsh: every sound is band-limited, filtered
 * warm and saturated softly. All integer math, as Felucca's audio is: the code that renders the demos on
 * a computer is the code the FM-1 runs. */
#pragma once
#include <stdint.h>

#define FS      44118                 /* the FM-1's I2S rate: 24 MHz / 544 = 44,117.6 Hz */
#define BLOCK   32                    /* samples per control tick: 1,378.7 ticks a second */
#define NVOICE  8
#define NCOPY   4                     /* copies of each note, like a guitar part tracked four times */

/* One patch, in units a person can tune by ear. Percentages are 0..100. */
typedef struct {
    const char *name;
    uint8_t  copies;                  /* 1..NCOPY */
    uint16_t spread;                  /* cents between the lowest and highest copy */
    uint16_t wobble, wobble_ms;       /* cents each copy wanders on its own, and how long one wander takes */
    uint16_t arm, arm_ms;             /* the shared tremolo arm: cents it bends down, and how long a bend takes */
    uint8_t  drive;                   /* soft saturation before the filter */
    uint8_t  air;                     /* breath noise through the same filter */
    uint16_t cutoff;                  /* low-pass at middle C, Hz */
    uint8_t  track;                   /* how far the cutoff follows the note (100 = all the way) */
    uint8_t  reso;
    uint8_t  bloom;                   /* how far the cutoff opens with the envelope */
    uint16_t attack, decay, release;  /* ms */
    uint8_t  sustain;
    uint8_t  verb;                    /* send to the reverb */
    uint16_t verb_time;               /* reverb decay to -60 dB, ms */
    uint16_t verb_damp;               /* reverb low-pass, Hz */
    uint8_t  level;
} Patch;

extern const Patch PATCHES[];
extern const int NPATCH;

/* album.c */
void album_init(void);
void album_patch(int p);
void album_note_on(int note, int vel);
void album_note_off(int note);
void album_render(int16_t *out, int frames);     /* interleaved stereo, frames a multiple of BLOCK */

/* ---- shared helpers ---- */

/* 2^(i/64) in Q30, i = 0..64 */
extern const uint32_t EXP2_T[65];

/* 2^(f / 65536) in Q30 for f in [0, 65536] */
static inline uint32_t exp2_frac(uint32_t f)
{
    uint32_t i = f >> 10, a = EXP2_T[i];
    if (i >= 64)
        return a;
    return a + (((EXP2_T[i + 1] - a) >> 4) * (f & 1023u) >> 6);
}

/* 2^(-x / 65536) in Q30, x >= 0 */
static inline uint32_t exp2_neg(uint32_t x)
{
    uint32_t n = (x >> 16) + 1u;
    return n >= 31u ? 0u : exp2_frac(65536u - (x & 0xFFFFu)) >> n;
}

/* the one-pole coefficient (Q16) that covers 63% of the way in t_ms at the control rate */
static inline int32_t k_ms(uint32_t t_ms)
{
    if (t_ms < 1u)
        t_ms = 1u;
    return (int32_t)((0x40000000u - exp2_neg(68579u / t_ms)) >> 14);
}

static inline uint32_t rnd(void)
{
    static uint32_t s = 0x2545F491u;
    s ^= s << 13; s ^= s >> 17; s ^= s << 5;
    return s;
}

/* smooth saturation: y = x - x^3 / 6.75, flat at |x| = 1.5; x and y Q15, nearly linear below half scale */
static inline int32_t soft(int32_t x)
{
    if (x >= 49152)
        return 32768;
    if (x <= -49152)
        return -32768;
    int32_t x2 = ((x >> 1) * (x >> 1)) >> 13;
    return x - (int32_t)(((int64_t)x2 * x * 4855) >> 30);      /* 4855 = 2^15 / 6.75 */
}
