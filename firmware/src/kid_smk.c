/* SPDX-License-Identifier: GPL-3.0-only
 * SMK-37 port: Copyright (C) 2026 M. Geisler (makkuro) */
/* The SMK-37 build: Rainbow mode (kid.c) on the SMK-37 (BOARD_SMK37). Included by kid.c, before its input.
 *   keys F3..G5  the FM-1's 27 keys, as in kid.c; fixed velocity (seq.c key_vel)
 *   outer keys   C3..E3 and G#5..C6: more notes on the friend's track (seq.c ext_keys_block); the friend hops,
 *                the band shows the note's letter
 *   pads         the 16 white keys F3..G5 (low row bottom), each in its note's colour: dim at rest, bright while held
 *                or while FOLLOW, GUESS or CHORDS light the key
 *   faders 1..4  BIG / SMALL, DAY / NIGHT, ECHO, WIGGLE (as KNOB 1..4); a fader takes over once it moves
 *   pitch wheel  a slide of +-2 semitones (seq.c smk_wheels_block: the channel's bend range)
 *   mod wheel    adds to WIGGLE
 *   KNOB BANK    a surprise friend (as HOME tapped); FADER BANK the next sky (as REC); < > the friend before / after
 *   K1           MASTER, never above the grown-ups' VOLUME (kid_master)
 * No menu is reachable from the toy; HOME held 1 s and HOME + SAVE held 3 s stay the grown-ups' (kid.c). */

static int8_t kid_outer = -1;                  /* the outer key whose letter shows (fm1_in.keys: C3 = 0), -1 none */
static uint32_t kid_outer_ms;
#define KID_OUTER_PC(now) (kid_outer >= 0 && (now) - kid_outer_ms < 900u && !drum_track(&trk[0]) ?                            (int32_t)((48u + (uint32_t)kid_outer) % 12u) : -1)

static uint8_t kid_mwig;                        /* the mod wheel's WIGGLE, 0..8 (added to KNOB 4's) */
#define KID_WIG ((uint8_t)(kid.wiggle + kid_mwig > 8u ? 8u : kid.wiggle + kid_mwig))

/* < / >: the friend before / after, as a PRESETS turn (kid_input) */
static int32_t kid_smk_lr;
#define KID_PRESET_TURN() (panel_enc(EN_PRESET) + kid_smk_lr)

static void kid_hint(uint32_t h);
static void kid_size(int32_t d);
static void kid_knobs(void);
static void kid_friend(uint32_t f);
static void kw_stamp(uint32_t fr);

/* K1 is a virtual MASTER pot (smk_input.h smk_master, 24 a detent): kept at the VOLUME's cap, so turning down acts at
 * once (master.c: master = pot^2 / 256) */
static void kid_smk_master_cap(int32_t cap)
{
    while (smk_master > 0 && (smk_master * smk_master) >> 8 > cap)
        smk_master--;
}

/* the spare buttons, the faders, the mod wheel and the outer keys; pressed: this frame's button edges. 1 if the child
 * touched something (the hello makes way) */
static int kid_smk_input(uint32_t pressed)
{
    static uint8_t last[4] = {0xFF, 0xFF, 0xFF, 0xFF};
    static uint64_t keys0;
    enum { OUTER = 0x1Fu };
    uint64_t outer = (uint64_t)OUTER | (uint64_t)OUTER << 32, kd;
    uint32_t i, mw;
    int any = 0;
    kid_smk_lr = 0;
    if (((pressed >> SMK_BTN_RIGHT) & 1u) && smk_btn_free(SMK_BTN_RIGHT))
        kid_smk_lr = 1;
    else if (((pressed >> SMK_BTN_LEFT) & 1u) && smk_btn_free(SMK_BTN_LEFT))
        kid_smk_lr = -1;
    if (((pressed >> SMK_BTN_KNOB_BANK) & 1u) && smk_btn_free(SMK_BTN_KNOB_BANK)) {   /* a surprise friend */
        any = 1;
        if (kw.on) {                              /* (WRITE: the friend to write with) */
            kid.fr = (uint8_t)((kid.fr + 1u + rng() % (KID_N - 1u)) % KID_N);
            kw_stamp(kid.fr);
        } else {
            kid_friend(kid.fr + 1u + rng() % (KID_N - 1u));
        }
        kid.party_ms = fm1_ms | 1u;
    }
    if (((pressed >> SMK_BTN_FADER_BANK) & 1u) && smk_btn_free(SMK_BTN_FADER_BANK) && !kw.on) {   /* the next sky */
        any = 1;
        kid.scene = (uint8_t)((kid.scene + 1u) % KS_COUNT);
        kid.full = 1;
        kid.party_ms = fm1_ms | 1u;
        kid.hop_ms = fm1_ms;
    }
    for (i = 0; i < 4u; i++) {                    /* the faders: a fader takes over once it moves */
        uint32_t v = fm1_in.fader[i];
        if (last[i] == 0xFF || fm1_in.frames < 200u) {   /* (the first readings settle) */
            last[i] = (uint8_t)v;
            continue;
        }
        if (v == last[i])
            continue;
        last[i] = (uint8_t)v;
        any = 1;
        if (i == 0u) {                            /* BIG / SMALL: low notes at the bottom, a big friend */
            if (!kw.on) {
                kid_size((int32_t)(v * 5u / 128u) - 2 - kid.oct);
                kid.acc = 0;
            }
        } else if (i == 1u) {                     /* DAY / NIGHT */
            uint32_t n = v * 9u / 128u;
            if (n != kid.night) {
                kid.night = (uint8_t)n;
                kid.full = 1;
            }
            kid_knobs();
            kid_hint(KH_NIGHT);
        } else if (!kw.on) {                      /* ECHO, WIGGLE */
            *(i == 2u ? &kid.echo : &kid.wiggle) = (uint8_t)(v * 9u / 128u);
            kid_knobs();
            kid_hint(i == 2u ? KH_ECHO : KH_WIGGLE);
        }
    }
    mw = ((uint32_t)smk_modw * 8u + 63u) / 127u;  /* the mod wheel: more WIGGLE */
    if (mw != kid_mwig) {
        if (mw > kid_mwig)
            any = 1;
        kid_mwig = (uint8_t)mw;
        kid_knobs();
        if (mw)
            kid_hint(KH_WIGGLE);
    }
    kd = fm1_in.keys & outer & ~keys0;            /* an outer key: the friend hops (seq.c plays it) */
    keys0 = fm1_in.keys & outer;
    if (kd) {                                     /* (and its letter, as a key's) */
        any = 1;
        kid.hop_ms = fm1_ms;
        for (i = 63u; !((kd >> i) & 1u); i--)
            ;
        kid_outer = (int8_t)i;
        kid_outer_ms = fm1_ms;
        kid.key = -1;
    }
    return any;
}

/* the button LEDs (on / off on the SMK) and the pads: the white keys in their notes' colours (KID_NOTE_COL), dim at rest,
 * bright while held or lit (kid_lit_mask: FOLLOW's next key, GUESS's hint, CHORDS' chord) */
static uint32_t kid_lit_mask(uint32_t now);
static void kid_smk_leds(void)
{
    uint8_t nl[LED_BUF] = {0};
    uint32_t k, c, lit = kid_lit_mask(fm1_ms);
    for (k = 0; k < KX_COUNT; k++)
        led_put(nl, panel.btn[KID_FX_BTN[k]], (kid.fx >> k) & 1u);
    led_put(nl, panel.btn[B_ARP], kid.arp && !kw.on);
    led_put(nl, panel.btn[B_SAVE], kw.on);        /* (WRITE: SAVE lit) */
    led_put(nl, panel.btn[B_PLAY], song.playing);
    for (c = 0; c < SMK_NLED; c++)
        fm1_led[c] = nl[c];
    if ((int32_t)(fm1_ms - padled_hold_until) < 0)      /* (console padtest has them) */
        return;
    for (c = 0; c < SMK_NPAD; c++) {
        uint32_t key = SMK_WHITE_NOTE[c], col = KID_NOTE_COL[(53u + key) % 12u];
        uint32_t lv = ((fm1_in.notes | lit) >> key) & 1u ? 160u : 12u;
        uint32_t r = (col >> 11) << 3, g = ((col >> 5) & 0x3Fu) << 2, b = (col & 0x1Fu) << 3;
        padled_set(SMK_PAD_OF_WHITE(c), (uint8_t)(r * lv >> 8), (uint8_t)(g * lv >> 8), (uint8_t)(b * lv >> 8));
    }
}
