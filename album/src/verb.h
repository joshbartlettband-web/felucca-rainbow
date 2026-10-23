/* SPDX-License-Identifier: GPL-3.0-only */
#pragma once
#include <stdint.h>

void verb_init(void);
void verb_set(uint32_t time_ms, uint32_t damp_hz);
/* in: one block of interleaved stereo (the dry mix); out: the reverb alone; send Q15 */
void verb_process(const int32_t *in, int32_t *out, int32_t send);
