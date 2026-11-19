// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue.core;

/** JieLi checksums and ciphers used by the FM-1's boot mode and its packages (ports of fm1_rescue.py). */
public final class Jl {
    private Jl() {}

    /** CRC-16/XMODEM: poly 0x1021, no reflection, starting from crc. */
    public static int crc16(byte[] p, int off, int len, int crc) {
        for (int i = 0; i < len; i++) {
            crc ^= (p[off + i] & 0xFF) << 8;
            for (int b = 0; b < 8; b++)
                crc = (crc & 0x8000) != 0 ? ((crc << 1) ^ 0x1021) & 0xFFFF : (crc << 1) & 0xFFFF;
        }
        return crc;
    }

    public static int crc16(byte[] p) { return crc16(p, 0, p.length, 0); }

    private static final byte[] MAGIC = {(byte) 0xC3, (byte) 0xCF, (byte) 0xC0, (byte) 0xE8, (byte) 0xCE, (byte) 0xD2,
            (byte) 0xB0, (byte) 0xAE, (byte) 0xC4, (byte) 0xE3, (byte) 0xA3, (byte) 0xAC, (byte) 0xD3, (byte) 0xF1,
            (byte) 0xC1, (byte) 0xD6};

    /** JieLi's CrcDecode cipher, key 0xFFFFFFFF, in place (the boot mode's chip key answer). */
    public static void crcCipher(byte[] buf) {
        int crc = crc16(new byte[] {(byte) 0xFF, (byte) 0xFF}, 0, 2, 0xFFFF);
        for (int i = 0; i < buf.length; i++) {
            crc = crc16(MAGIC, i % 16, 1, crc);
            buf[i] ^= (byte) crc;
        }
    }

    /** JieLi ENC stream cipher, in place (package header and entries), starting from key. */
    public static void enc(byte[] buf, int off, int len, int key) {
        for (int i = 0; i < len; i++) {
            buf[off + i] ^= (byte) key;
            key = ((key << 1) ^ ((key & 0x8000) != 0 ? 0x1021 : 0)) & 0xFFFF;
        }
    }
}
