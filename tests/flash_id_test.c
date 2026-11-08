/* SPDX-License-Identifier: GPL-3.0-only */
/* The FM-1's flash chip gate (firmware/hal/fm1_flash_map.h FL_JEDEC_OK, used by project.c persist_boot): both 1 MiB
 * parts the FM-1 has shipped with are accepted, so saves reach flash and the update command works on the new units
 * too; anything else stays RAM-only. (The SMK-37 Pro's list: smk_flash_test.c.) */
#include <stdint.h>
#include <stdio.h>
#include "fm1_flash_map.h"

static int bad;
static void check(const char *what, int ok) { printf("flash id: %-58s %s\n", what, ok ? "ok" : "FAIL"); bad += !ok; }

int main(void)
{
    check("0x856014 (Puya P25Q80, the FM-1 until 2026) accepted", FL_JEDEC_OK(0x856014u));
    check("0xB36014 (UCUN UC25HQ80, the 2026 units) accepted", FL_JEDEC_OK(0xB36014u));
    check("0x000000 (no answer) refused", !FL_JEDEC_OK(0x000000u));
    check("0xFFFFFF (bus idle) refused", !FL_JEDEC_OK(0xFFFFFFu));
    check("0x856015, 0xB36015 (near misses) refused", !FL_JEDEC_OK(0x856015u) && !FL_JEDEC_OK(0xB36015u));
    check("0xEB6014 (the SMK-37 Pro's part, not an FM-1's) refused", !FL_JEDEC_OK(0xEB6014u));
    return bad ? 1 : 0;
}
