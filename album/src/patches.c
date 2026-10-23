/* SPDX-License-Identifier: GPL-3.0-only */
/* The twelve patches, one per photo. Tune these by ear on a real FM-1, on headphones first. */
#include "album.h"

const Patch PATCHES[] = {
    /* 1. WING: the wing over the cloud deck (Pixel 9a, October 10, 2026). Blue going white, bright but
     * soft, almost no contrast: slow and airy, a long arm bend, a little cabin hush (air), a long room. */
    { .name = "WING", .copies = 4, .spread = 14, .wobble = 7, .wobble_ms = 1800, .arm = 24, .arm_ms = 3200,
      .drive = 25, .air = 10, .cutoff = 1300, .track = 45, .reso = 10, .bloom = 35,
      .attack = 900, .decay = 3000, .release = 2600, .sustain = 80,
      .verb = 55, .verb_time = 5200, .verb_damp = 3200, .level = 70 },
};
const int NPATCH = sizeof PATCHES / sizeof PATCHES[0];
