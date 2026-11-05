// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue.core;

import java.io.ByteArrayOutputStream;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Locale;
import java.util.zip.CRC32;

/**
 * The FM-1 through an FM-1 Transporter (kurogedelic/FM-1-transporter, MIT): a XIAO RP2040 wired to the FM-1's USB
 * lines that forces the chip into its boot mode electrically (USB_KEY at power-on) and drives it as a USB host.
 * The phone talks to the Transporter's "data" serial channel in its text protocol (src/transporter_proto.h):
 *   ping, status, info, read ADDR LEN, wsec ADDR CRC32 + 4096 bytes, memw ADDR LEN CRC32 + bytes, jump ADDR ARG, runapp.
 * The Transporter build used here carries no JieLi loader (transporter/0001-host-provided-loader.patch): the phone
 * uploads wl82loader.bin with memw and starts it with jump. memw ciphers what it writes (the boot mode's RAM writes
 * go through jl_crc_cipher, per transfer), so each 512-byte block of the shipped, already ciphered blob is
 * deciphered here first: on the wire the chip gets exactly the shipped bytes.
 */
public final class Transporter implements FlashTarget {
    /** The serial link to the Transporter's data channel (Android: CDC-ACM over USB; tests: a simulator). */
    public interface Link {
        void write(byte[] b) throws RescueFail;

        /** Up to len bytes into buf at off; 0 on timeout. */
        int read(byte[] buf, int off, int len, int timeoutMs) throws RescueFail;
    }

    public static final int VID = 0x2E8A, PID = 0x000A;   // the Transporter's own USB identity (Pico SDK CDC)
    private static final int LOADER_ADDR = 0x1C02000, CHUNK = 0x10000;

    private final Link link;
    private final byte[] buf = new byte[16384];
    private int bufLen, bufPos;

    public Transporter(Link link) { this.link = link; }

    // ------------------------------------------------------------ the stream ---
    private int nextByte(long deadline) throws RescueFail {
        while (bufPos >= bufLen) {
            long left = deadline - System.currentTimeMillis();
            if (left <= 0) return -1;
            bufLen = link.read(buf, 0, buf.length, (int) Math.min(left, 1000));
            bufPos = 0;
        }
        return buf[bufPos++] & 0xFF;
    }

    String readLine(int timeoutMs) throws RescueFail {
        long deadline = System.currentTimeMillis() + timeoutMs;
        ByteArrayOutputStream s = new ByteArrayOutputStream();
        for (int c; (c = nextByte(deadline)) != '\n'; ) {
            if (c < 0) throw new RescueFail("the Transporter did not answer in time");
            if (c != '\r') s.write(c);
        }
        return s.toString(StandardCharsets.ISO_8859_1);
    }

    private byte[] readExact(int n, int timeoutMs) throws RescueFail {
        long deadline = System.currentTimeMillis() + timeoutMs;
        byte[] out = new byte[n];
        for (int i = 0; i < n; i++) {
            int c = nextByte(deadline);
            if (c < 0) throw new RescueFail("the Transporter stopped sending (" + i + " of " + n + " bytes)");
            out[i] = (byte) c;
        }
        return out;
    }

    private void drain() throws RescueFail {   // anything left over from an earlier, interrupted request
        bufPos = bufLen = 0;
        while (link.read(buf, 0, buf.length, 50) > 0) { }
        bufPos = bufLen = 0;
    }

    String request(String line, byte[] payload, int timeoutMs) throws RescueFail {
        drain();
        link.write((line + "\n").getBytes(StandardCharsets.ISO_8859_1));
        if (payload != null) link.write(payload);
        return readLine(timeoutMs);
    }

    private static long crc32(byte[] b) {
        CRC32 c = new CRC32();
        c.update(b);
        return c.getValue();
    }

    private static RescueFail err(String what, String reply) {
        return new RescueFail(what + ": the Transporter said \"" + reply + "\"");
    }

    // ------------------------------------------------------------ the Transporter itself ---
    /** ping: true if the data channel answers (it does even while the Transporter is still keying). */
    public boolean ping(int timeoutMs) {
        try { return "PONG".equals(request("ping", null, timeoutMs)); } catch (RescueFail e) { return false; }
    }

    /** status, as "uboot=1 v15=0 loader=0 loader_running=0"; uboot=1: the FM-1's boot mode is connected. */
    public String status() throws RescueFail {
        String r = request("status", null, 5000);
        if (!r.startsWith("OK")) throw err("status", r);
        return r.substring(2).trim();
    }

    public static boolean has(String status, String kv) { return (" " + status + " ").contains(" " + kv + " "); }

    /** Stock V15 running: the USB-MIDI soft key sends it to the boot mode, no keying needed. */
    public String softKey() throws RescueFail { return request("uboot", null, 10000); }

    /** Restart the Transporter in USB_KEY mode (it drops off USB and comes back). */
    public void rekey() throws RescueFail { link.write("rekey\n".getBytes(StandardCharsets.ISO_8859_1)); }

    // ------------------------------------------------------------ FlashTarget ---
    @Override public String identify() throws RescueFail {
        String st = status();
        if (!has(st, "uboot=1"))
            throw new RescueFail("the Transporter has not reached the FM-1's boot mode yet (" + st + ")");
        return "Transporter: the FM-1's boot mode is connected (" + st + ")";
    }

    @Override public void startLoader(byte[] blob) throws RescueFail {
        if (has(status(), "loader_running=1")) return;   // started in an earlier attempt on this connection
        for (int off = 0; off < blob.length; off += Uboot.IO) {
            byte[] block = Arrays.copyOfRange(blob, off, Math.min(off + Uboot.IO, blob.length));
            Jl.crcCipher(block);                          // undone by memw's own cipher: the shipped bytes arrive
            String r = request(String.format(Locale.US, "memw 0x%X %d %08X", LOADER_ADDR + off, block.length, crc32(block)), block, 10000);
            if (!r.equals("OK")) throw err("loading the flash loader", r);
        }
        String r = request(String.format(Locale.US, "jump 0x%X 1", LOADER_ADDR), null, 10000);
        if (!r.startsWith("OK")) throw err("starting the flash loader", r);
        if (!has(status(), "loader_running=1"))
            throw new RescueFail("the Transporter did not take the loader as running: its firmware needs the "
                    + "host-provided-loader patch (the FM-1 Rescue Transporter build)", true);
    }

    @Override public int[] chip() throws RescueFail {
        String r = request("info", null, 30000);   // OK key=980F type=3 id=856014
        if (!r.startsWith("OK")) throw err("chip check", r);
        int key = -1, type = -1, id = -1;
        for (String kv : r.substring(2).trim().split(" ")) {
            String[] p = kv.split("=");
            if (p.length != 2) continue;
            if (p[0].equals("key")) key = Integer.parseInt(p[1], 16);
            if (p[0].equals("type")) type = Integer.parseInt(p[1]);
            if (p[0].equals("id")) id = Integer.parseInt(p[1], 16);
        }
        return new int[] {key, type, id};
    }

    @Override public byte[] read(int addr, int n, Progress pr) throws RescueFail {
        byte[] out = new byte[n];
        for (int got = 0; got < n; ) {
            int k = Math.min(CHUNK, n - got);
            String r = request(String.format(Locale.US, "read 0x%X %d", addr + got, k), null, 30000);
            if (!r.equals("DATA " + k)) throw err("reading the flash", r);
            byte[] data = readExact(k, 30000);
            String end = readLine(10000);
            if (!end.equals(String.format(Locale.US, "END %08X", crc32(data))))
                throw new RescueFail(String.format("a flash read came back damaged at %#x (%s)", addr + got, end));
            System.arraycopy(data, 0, out, got, k);
            got += k;
            if (pr != null) pr.at(got, n);
        }
        return out;
    }

    @Override public void writeSector(int addr, byte[] data) throws RescueFail {
        if (addr < Uboot.WRITE_MIN || addr >= Fwsc.APP_END || addr % Uboot.SECTOR != 0 || data.length != Uboot.SECTOR)
            throw new RescueFail(String.format("refusing to write %#x (outside the application area)", addr), true);
        String r = request(String.format(Locale.US, "wsec 0x%X %08X", addr, crc32(data)), data, 30000);
        if (!r.equals("OK")) throw err(String.format("writing sector %#07x", addr), r);   // erased, written, read back there
    }

    @Override public void ping() throws RescueFail {
        if (!"PONG".equals(request("ping", null, 5000))) throw new RescueFail("the Transporter stopped answering");
    }

    @Override public void runApp() {
        try { request("runapp", null, 10000); } catch (RescueFail ignored) { }
    }
}
