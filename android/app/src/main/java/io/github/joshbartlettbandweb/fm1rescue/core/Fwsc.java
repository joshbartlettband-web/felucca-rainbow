// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue.core;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

/**
 * An FM-1 update package (.fwsc): its identity and its type-0 "flash" entry, which is raw flash [0, 0x93000).
 * Layout as tools/fm1pkg_make.py writes it and as fm1_rescue.py reads it: the logical image is the file without
 * the marker byte after each of its first 20 0x2F-byte blocks; it starts with a 0x40-byte header and a list of
 * 0x50-byte entries, each ENC'd from key 0xFFFF.
 */
public final class Fwsc {
    public static final int APP_END = 0x93000;
    /** M-VAVE's official FM-1 V15 (FM-1.fwsc). */
    public static final String STOCK_V15_SHA256 = "db1642b2b6fa5c2cccb11ffd13878068bb28601678d3644049f99dc40e7edb8a";
    public static final String STOCK_V15_URL = "https://yms-file-store.oss-cn-hongkong.aliyuncs.com/software/firmware/FM-1.fwsc";

    public final String sha256;
    public final String identity;   // FM-1_015 (stock V15), FM-1_9xx (Felucca, Rainbow mode), ...
    public final byte[] flash;      // raw flash [0, APP_END)

    private Fwsc(String sha256, String identity, byte[] flash) {
        this.sha256 = sha256;
        this.identity = identity;
        this.flash = flash;
    }

    public boolean isStockV15() { return STOCK_V15_SHA256.equals(sha256); }

    /** Felucca builds (Rainbow mode included) say FM-1_9xx. */
    public boolean isFelucca() { return identity.matches("FM-1_9\\d\\d"); }

    public static Fwsc parse(byte[] raw) throws RescueFail {
        if (raw.length < 20 * 0x30 + 0x40)
            throw new RescueFail("this file is too small to be an FM-1 package", true);
        StringBuilder id = new StringBuilder();
        for (int i = 0; i < 20; i++) {
            int m = raw[i * 0x30 + 0x2F] & 0xFF;
            if (m != 0x7D) id.append((char) ((m - i - 1) & 0xFF));
        }
        byte[] logical = new byte[raw.length - 20];
        for (int i = 0; i < 20; i++) System.arraycopy(raw, i * 0x30, logical, i * 0x2F, 0x2F);
        System.arraycopy(raw, 20 * 0x30, logical, 20 * 0x2F, raw.length - 20 * 0x30);
        byte[] hdr = new byte[0x40];
        System.arraycopy(logical, 0, hdr, 0, 0x40);
        Jl.enc(hdr, 0, 0x40, 0xFFFF);
        ByteBuffer h = ByteBuffer.wrap(hdr).order(ByteOrder.LITTLE_ENDIAN);
        int n = h.getShort(8) & 0xFFFF;
        if (!"AC791N".equals(new String(hdr, 16, 6, StandardCharsets.ISO_8859_1)) || n <= 0 || n >= 16)
            throw new RescueFail("not an FM-1 package (its header does not name the FM-1's chip)", true);
        for (int i = 0; i < n; i++) {
            int at = 0x40 + i * 0x50;
            if (at + 0x50 > logical.length) break;
            byte[] e = new byte[0x50];
            System.arraycopy(logical, at, e, 0, 0x50);
            Jl.enc(e, 0, 0x50, 0xFFFF);
            ByteBuffer b = ByteBuffer.wrap(e).order(ByteOrder.LITTLE_ENDIAN);
            int typ = b.getShort(0) & 0xFFFF, dcrc = b.getShort(4) & 0xFFFF;
            long off = b.getInt(8) & 0xFFFFFFFFL, size = b.getInt(12) & 0xFFFFFFFFL;
            if (typ != 0) continue;
            if (off + size > logical.length)
                throw new RescueFail("the package is cut short (its flash entry runs past the end)", true);
            byte[] data = new byte[(int) size];
            System.arraycopy(logical, (int) off, data, 0, (int) size);
            if (Jl.crc16(data) != dcrc) throw new RescueFail("the package's flash entry is damaged (bad CRC)", true);
            if (data.length != APP_END)
                throw new RescueFail(String.format("the package's flash entry is %d bytes, an FM-1's is %d", data.length, APP_END), true);
            return new Fwsc(sha256(raw), id.toString(), data);
        }
        throw new RescueFail("the package has no flash entry", true);
    }

    public static String sha256(byte[] b) { return sha256(b, 0, b.length); }

    public static String sha256(byte[] b, int off, int len) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            md.update(b, off, len);
            StringBuilder s = new StringBuilder();
            for (byte x : md.digest()) s.append(String.format("%02x", x & 0xFF));
            return s.toString();
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }
}
