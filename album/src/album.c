/* SPDX-License-Identifier: GPL-3.0-only */
/* ALBUM's sound: the GLIDE voice, after Kevin Shields' glide guitar on "m b v". Each note is NCOPY band-limited
 * saws, detuned a few cents apart, each wandering in pitch on its own; one shared tremolo arm bends every held
 * note down and back together, as one guitar would. Then soft saturation, a 3-pole low-pass that darkens the
 * high notes, a slow envelope, the reverb (verb.c) and a soft master clip.
 * Q formats: pitch in 1/16 cent (Q4), envelopes Q30, audio Q15 (filters Q14), one-pole coefficients Q16. */
#include "album.h"
#include "verb.h"

#define INC60     25469927u           /* phase step of middle C (261.63 Hz) at FS, in 2^32 per sample */
#define W_PER_HZ  76461               /* pi / FS in Q30 */
#define DAMP_OCT  13465               /* 2 pi / FS / ln 2: Q16 octaves per 1000 Hz */

const uint32_t EXP2_T[65] = {
    1073741824, 1085434106, 1097253708, 1109202018, 1121280436, 1133490379, 1145833280, 1158310587,
    1170923762, 1183674286, 1196563654, 1209593378, 1222764986, 1236080024, 1249540052, 1263146652,
    1276901417, 1290805962, 1304861917, 1319070932, 1333434672, 1347954824, 1362633090, 1377471191,
    1392470869, 1407633882, 1422962010, 1438457051, 1454120821, 1469955159, 1485961921, 1502142985,
    1518500250, 1535035634, 1551751076, 1568648537, 1585730000, 1602997467, 1620452965, 1638098541,
    1655936265, 1673968228, 1692196547, 1710623359, 1729250827, 1748081133, 1767116489, 1786359126,
    1805811301, 1825475297, 1845353420, 1865448001, 1885761398, 1906295993, 1927054196, 1948038440,
    1969251188, 1990694927, 2012372174, 2034285470, 2056437387, 2078830522, 2101467502, 2124350982,
    2147483648,
};

/* v * 2^(oct / 65536), oct within +-15 octaves */
static uint32_t exp2_mul(uint32_t v, int32_t oct)
{
    int32_t n = oct >> 16;                                   /* floor */
    uint64_t m = (uint64_t)v * exp2_frac((uint32_t)oct & 0xFFFFu);
    return (uint32_t)(m >> (30 - n));
}

/* a slow random walk through two one-poles: it drifts to a new point every `ms` or so, never jumps */
typedef struct { int32_t x, v, tgt, count; } Wander;

static void wander(Wander *w, int32_t lo, int32_t hi, uint32_t ms, int32_t k)
{
    if (--w->count <= 0) {
        int32_t ticks = (int32_t)(ms * 1379u / 1000u);
        w->count = ticks / 2 + (int32_t)(rnd() % (uint32_t)(ticks + 1));
        w->tgt = lo + (int32_t)(rnd() % (uint32_t)(hi - lo + 1));
    }
    w->v += (int32_t)(((int64_t)(w->tgt - w->v) * k) >> 16);
    w->x += (int32_t)(((int64_t)(w->v - w->x) * k) >> 16);
}

enum { OFF, ATTACK, DECAY, RELEASE };

typedef struct {
    uint8_t stage, note;
    uint32_t age;
    uint32_t ph[NCOPY], inc[NCOPY];
    Wander wob[NCOPY];
    int32_t env, amp;                  /* env Q30; amp Q15 (level and velocity) */
    int32_t e15;                       /* the envelope times amp at the end of the last block, Q15 */
    int32_t f, q, a;                   /* filter: SVF f Q14, damping Q12, one-pole Q14 */
    int32_t lp[2], bp[2], op[2];       /* per side */
    uint32_t noise;
} Voice;

static Voice V[NVOICE];
static const Patch *P;
static Wander arm;
static uint32_t clock;
/* per patch: copy c goes to side A (1), B (2) or both at half (3); offsets in Q4 cents; gains */
static uint8_t dst[NCOPY];
static int32_t spread_q4[NCOPY], dgain, post, air15, kw, ka;
static int32_t katk, kdec, krel, sus;

void album_patch(int p)
{
    static const uint8_t DST[NCOPY + 1][NCOPY] = { {0}, {3}, {1, 2}, {1, 2, 3}, {1, 2, 1, 2} };
    int n, c;
    P = &PATCHES[p < 0 ? 0 : p >= NPATCH ? NPATCH - 1 : p];
    n = P->copies < 1 ? 1 : P->copies > NCOPY ? NCOPY : P->copies;
    for (c = 0; c < NCOPY; c++) {
        dst[c] = c < n ? DST[n][c] : 0;
        spread_q4[c] = n > 1 ? (int32_t)P->spread * 16 * (2 * c - (n - 1)) / (2 * (n - 1)) : 0;
    }
    /* each side carries up to two copies (Q15 each); scale to one, then the drive pushes into soft() */
    dgain = (n > 1 ? 2048 : 4096) * (100 + 3 * P->drive) / 100;     /* Q12 */
    post = 32768 * 100 / (100 + 2 * P->drive);                         /* Q15: keeps the level as drive rises */
    air15 = P->air * 32768 / 100;
    kw = k_ms(P->wobble_ms / 3u);
    ka = k_ms(P->arm_ms / 3u);
    katk = k_ms(P->attack / 2u);       /* the attack aims past full, so it lands in about its time */
    kdec = k_ms(P->decay);
    krel = k_ms(P->release / 3u);      /* to -60 dB or so in about the release time */
    sus = (int32_t)((int64_t)P->sustain * 0x40000000 / 100);
    verb_set(P->verb_time, P->verb_damp);
}

void album_init(void)
{
    int i;
    for (i = 0; i < NVOICE; i++)
        V[i].stage = OFF, V[i].noise = 0x9E3779B9u * (uint32_t)(i + 1);
    verb_init();
    album_patch(0);
}

void album_note_on(int note, int vel)
{
    int i, best = 0;
    uint32_t oldest = 0;
    /* a free voice, else the oldest released one, else the oldest */
    for (i = 0; i < NVOICE; i++) {
        uint32_t age = clock - V[i].age + (V[i].stage == RELEASE ? 0x80000000u : 0u);
        if (V[i].stage == OFF) { best = i; break; }
        if (age >= oldest) oldest = age, best = i;
    }
    Voice *v = &V[best];
    if (v->stage == OFF) {
        int c;
        v->env = 0, v->e15 = 0;
        for (c = 0; c < 2; c++)
            v->lp[c] = v->bp[c] = v->op[c] = 0;
        for (c = 0; c < NCOPY; c++) {
            v->ph[c] = rnd();          /* free-running phases, as strings never start together */
            v->wob[c].x = v->wob[c].v = 0, v->wob[c].count = 0;
        }
    }
    v->note = (uint8_t)note;
    v->amp = (int32_t)((int64_t)P->level * 32768 / 100 * (64 + vel / 2) / 127);   /* half the level at velocity 0 */
    v->stage = ATTACK;
    v->age = clock;
}

void album_note_off(int note)
{
    int i;
    for (i = 0; i < NVOICE; i++)
        if (V[i].note == note && (V[i].stage == ATTACK || V[i].stage == DECAY))
            V[i].stage = RELEASE;
}

/* once per block: envelope, pitches, filter */
static void voice_tick(Voice *v)
{
    int c;
    int64_t d;
    switch (v->stage) {
    case ATTACK:
        d = (int64_t)0x50000000 - v->env;                   /* aims at 1.25 */
        v->env += (int32_t)((d * katk) >> 16);
        if (v->env >= 0x40000000)
            v->env = 0x40000000, v->stage = DECAY;
        break;
    case DECAY:
        v->env += (int32_t)(((int64_t)(sus - v->env) * kdec) >> 16);
        break;
    case RELEASE:
        v->env -= (int32_t)(((int64_t)v->env * krel) >> 16);
        if (v->env < (0x40000000 >> 12))                    /* -72 dB */
            v->env = 0, v->stage = OFF;
        break;
    }
    for (c = 0; c < NCOPY; c++) {
        if (!dst[c])
            continue;
        wander(&v->wob[c], -16 * P->wobble, 16 * P->wobble, P->wobble_ms, kw);
        int32_t q4 = (v->note - 60) * 1600 + spread_q4[c] + v->wob[c].x + arm.x;
        v->inc[c] = exp2_mul(INC60, q4 * 256 / 75);         /* Q4 cents to Q16 octaves */
    }
    /* cutoff: follows the note by `track`, opens by up to two octaves with the envelope (`bloom`) */
    int32_t oct = (v->note - 60) * 65536 / 12 * P->track / 100
                + (int32_t)(((int64_t)(v->env >> 14) * P->bloom * 2) / 100);
    uint32_t fc = exp2_mul(P->cutoff, oct);
    fc = fc < 30u ? 30u : fc > 6000u ? 6000u : fc;
    int32_t w = (int32_t)fc * W_PER_HZ;                     /* Q30 */
    int32_t w3 = (int32_t)(((((int64_t)w * w) >> 30) * w) >> 30);
    v->f = (w - w3 / 6) >> 15;                              /* 2 sin(w), Q14 */
    v->q = 8192 - P->reso * 7168 / 100;
    v->a = 16384 - (int32_t)(exp2_neg(fc * DAMP_OCT / 1000u) >> 16);
}

static void voice_render(Voice *v, int32_t *mix)
{
    int i, c;
    int32_t e0 = v->e15, e1 = (int32_t)(((int64_t)(v->env >> 15) * v->amp) >> 15);
    int32_t de = (e1 - e0) / BLOCK, e = e0;
    v->e15 = e1;
    for (i = 0; i < BLOCK; i++) {
        int32_t side[2] = { 0, 0 };
        for (c = 0; c < NCOPY; c++) {
            if (!dst[c])
                continue;
            uint32_t ph = v->ph[c] += v->inc[c], inc = v->inc[c], dv = inc >> 15;
            int32_t s = (int32_t)(ph >> 16) - 32768;          /* naive saw, Q15 */
            if (dv) {                                       /* polyBLEP: round off the step at the wrap */
                if (ph < inc) {
                    int32_t t = (int32_t)(ph / dv);
                    t = t > 32767 ? 32767 : t;
                    s -= t + t - ((t * t) >> 15) - 32768;
                } else if (ph > ~inc) {
                    int32_t t = -(int32_t)(~ph / dv);
                    t = t < -32767 ? -32767 : t;
                    s -= ((t * t) >> 15) + t + t + 32768;
                }
            }
            if (dst[c] == 3)
                side[0] += s >> 1, side[1] += s >> 1;
            else
                side[dst[c] - 1] += s;
        }
        for (c = 0; c < 2; c++) {
            int32_t x = soft((side[c] * dgain) >> 12);
            x = (x * post) >> 15;
            v->noise = v->noise * 1664525u + 1013904223u;
            x += (((int32_t)v->noise >> 16) * air15) >> 15;
            x >>= 1;                                        /* Q14 into the filter */
            v->lp[c] += (v->f * v->bp[c]) >> 14;
            int32_t hp = x - v->lp[c] - ((v->q * v->bp[c]) >> 12);
            v->bp[c] += (v->f * hp) >> 14;
            v->op[c] += ((v->lp[c] - v->op[c]) * v->a) >> 14;
            mix[2 * i + c] += (v->op[c] * (e >> 1)) >> 14;
        }
        e += de;
    }
}

void album_render(int16_t *out, int frames)
{
    static int32_t mix[2 * BLOCK], wet[2 * BLOCK], hp[2];
    int i, j;
    for (; frames >= BLOCK; frames -= BLOCK, out += 2 * BLOCK) {
        clock++;
        wander(&arm, -16 * P->arm, 0, P->arm_ms, ka);
        for (i = 0; i < 2 * BLOCK; i++)
            mix[i] = 0;
        for (j = 0; j < NVOICE; j++)
            if (V[j].stage != OFF) {
                voice_tick(&V[j]);
                voice_render(&V[j], mix);
            }
        verb_process(mix, wet, P->verb * 32768 / 100);
        for (i = 0; i < 2 * BLOCK; i++) {
            /* master: -6 dB, a 7 Hz high-pass for any offset (its state kept 10 bits finer), the soft clip */
            int32_t x = (mix[i] + wet[i]) >> 1;
            hp[i & 1] += (x * 1024 - hp[i & 1]) >> 10;
            int32_t y = soft(x - (hp[i & 1] >> 10));
            out[i] = (int16_t)(y > 32767 ? 32767 : y);
        }
    }
}
