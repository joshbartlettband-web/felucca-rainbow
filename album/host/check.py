# SPDX-License-Identifier: GPL-3.0-only
"""Numbers for a rendered patch: how loud, and how much of it sits up where sounds turn tinny or harsh.
Ears decide; this only catches the obvious. Usage: python3 check.py wing.wav"""
import sys
import wave

import numpy as np

w = wave.open(sys.argv[1])
fs = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").reshape(-1, 2).astype(np.float64) / 32768
m = x.mean(axis=1)

peak = np.abs(x).max()
rms = np.sqrt((x ** 2).mean())
print(f"peak {20 * np.log10(peak):.1f} dBFS, rms {20 * np.log10(rms):.1f} dBFS, "
      f"samples at full scale: {(np.abs(x) >= 32767 / 32768).sum()}")

# the share of the energy in each band, over the whole render (Welch-style average of 8192-point frames)
n = 8192
win = np.hanning(n)
frames = [m[i:i + n] * win for i in range(0, len(m) - n, n // 2)]
p = np.mean([np.abs(np.fft.rfft(f)) ** 2 for f in frames], axis=0)
f = np.fft.rfftfreq(n, 1 / fs)
tot = p.sum()
for lo, hi in [(20, 250), (250, 1000), (1000, 3000), (3000, 6000), (6000, 10000), (10000, fs / 2)]:
    s = p[(f >= lo) & (f < hi)].sum() / tot
    print(f"{lo:>6.0f}-{hi:<6.0f} Hz  {10 * np.log10(max(s, 1e-12)):6.1f} dB")
# the 2-5 kHz band is where ears are most sensitive and harshness lives
print(f"left/right correlation {np.corrcoef(x[:, 0], x[:, 1])[0, 1]:.2f}")
