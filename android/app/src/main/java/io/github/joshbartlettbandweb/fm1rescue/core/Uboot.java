// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue.core;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

/**
 * The FM-1's boot mode (ROM "UBOOT1.00", USB 4C4A:8057, mass storage bulk-only transport) and JieLi's flash loader
 * run from it. A port of fm1_rescue.py (charlesvestal/fm1-x0x, GPL-3.0); the protocol is FM-1-transporter's
 * docs/PROTOCOL.md (kurogedelic, MIT), verified on hardware there.
 */
public final class Uboot implements FlashTarget {
    public static final int VID = 0x4C4A, PID = 0x8057;
    public static final int FLASH_SIZE = 0x100000, WRITE_MIN = 0x4000, SECTOR = 0x1000, IO = 512;
    public static final int CHIP_KEY = 0x980F, FLASH_TYPE = 3, FLASH_ID = 0x856014;
    public static final String LOADER_URL = "https://raw.githubusercontent.com/kagaimiq/jl-uboot-tool/"
            + "c32b28e7a04f873f526ba929cb1bae9f05442fe9/data/loaderblobs/usb/wl82loader.bin";
    public static final String LOADER_SHA256 = "d41da6126760c9d66660bcc0cac8d27d221806c5e369a8036921efe68dca5376";
    static final int LOADER_ADDR = 0x1C02000, LOADER_ARG = 0x0001;

    // ROM UBOOT1.00
    static final int CMD_WRITE_MEMORY = 0xFB06, CMD_JUMP = 0xFB08;
    // the loader
    static final int CMD_ERASE_SECTOR = 0xFB01, CMD_WRITE_FLASH = 0xFB04, CMD_READ_FLASH = 0xFD05;
    static final int CMD_READ_KEY = 0xFC09, CMD_GET_ONLINE_DEVICE = 0xFC0A, CMD_RUN_APP = 0xFC0C;

    private static final int TIMEOUT = 5000;
    private final Transport t;
    private int tag = 1;

    public Uboot(Transport t) { this.t = t; }

    /** One command: CBW, an optional data phase (out or in), CSW. */
    byte[] xfer(byte[] cdb, byte[] dataOut, int nIn) throws RescueFail {
        int myTag = tag;
        tag = tag + 1;
        int length = dataOut != null ? dataOut.length : nIn;
        ByteBuffer cbw = ByteBuffer.allocate(31).order(ByteOrder.LITTLE_ENDIAN);
        cbw.put("USBC".getBytes(StandardCharsets.ISO_8859_1)).putInt(myTag).putInt(length)
                .put((byte) (nIn > 0 ? 0x80 : 0x00)).put((byte) 0).put((byte) cdb.length).put(cdb);
        out(cbw.array());
        byte[] got = new byte[0];
        if (dataOut != null && dataOut.length > 0) out(dataOut);
        else if (nIn > 0) got = in(nIn);
        byte[] csw = in(13);
        ByteBuffer c = ByteBuffer.wrap(csw).order(ByteOrder.LITTLE_ENDIAN);
        byte[] sig = Arrays.copyOfRange(csw, 0, 4);
        if (!Arrays.equals(sig, "USBS".getBytes(StandardCharsets.ISO_8859_1)) || c.getInt(4) != myTag)
            throw new RescueFail("the FM-1 answered out of step (bad status block)");
        if ((csw[12] & 0xFF) != 0) throw new RescueFail("the FM-1 refused a command (status " + (csw[12] & 0xFF) + ")");
        return got;
    }

    private void out(byte[] b) throws RescueFail {
        int n = t.bulkOut(b, b.length, TIMEOUT);
        if (n != b.length) throw new RescueFail("the FM-1 stopped answering (USB send)");
    }

    private byte[] in(int n) throws RescueFail {   // one transfer per phase, as fm1_rescue.py reads them
        byte[] b = new byte[n];
        int k = t.bulkIn(b, n, TIMEOUT);
        if (k < 0) throw new RescueFail("the FM-1 stopped answering (USB receive)");
        if (k != n) throw new RescueFail("the FM-1 sent " + k + " bytes where " + n + " were expected");
        return b;
    }

    static byte[] cdb(int cmd, byte[] args) {
        byte[] c = new byte[16];
        Arrays.fill(c, (byte) 0xFF);
        c[0] = (byte) (cmd >> 8);
        c[1] = (byte) cmd;
        System.arraycopy(args, 0, c, 2, args.length);
        return c;
    }

    static byte[] be(int... fields) {   // pairs: value, width (4 or 2), big-endian
        ByteBuffer b = ByteBuffer.allocate(16).order(ByteOrder.BIG_ENDIAN);
        for (int i = 0; i < fields.length; i += 2) {
            if (fields[i + 1] == 4) b.putInt(fields[i]);
            else b.putShort((short) fields[i]);
        }
        return Arrays.copyOf(b.array(), b.position());
    }

    @Override public String identify() throws RescueFail {
        String[] iq = inquiry();
        if (!"WL82".equals(iq[0]))
            throw new RescueFail("this is not the FM-1's boot mode (it says " + iq[0] + ")", true);
        return "Device: " + iq[0] + " " + iq[1];
    }

    /** SCSI INQUIRY: {vendor, product}; the boot mode says WL82 / UBOOT1.00. */
    public String[] inquiry() throws RescueFail {
        byte[] r = xfer(new byte[] {0x12, 0, 0, 0, 36, 0}, null, 36);
        return new String[] {new String(r, 8, 8, StandardCharsets.ISO_8859_1).trim(),
                new String(r, 16, 16, StandardCharsets.ISO_8859_1).trim()};
    }

    byte[] cmd(int cmd, byte[] args) throws RescueFail {
        byte[] r = xfer(cdb(cmd, args), null, 16);
        if (((r[0] & 0xFF) << 8 | (r[1] & 0xFF)) != cmd)
            throw new RescueFail(String.format("command %04X was answered as %02X%02X", cmd, r[0] & 0xFF, r[1] & 0xFF));
        return Arrays.copyOfRange(r, 2, 16);
    }

    void writeBlock(int cmd, int addr, byte[] data) throws RescueFail {
        int crc = Jl.crc16(data);
        byte[] a = be(addr, 4, data.length, 2);
        byte[] args = Arrays.copyOf(a, a.length + 3);
        args[a.length] = 0;
        args[a.length + 1] = (byte) crc;           // crc16 little-endian
        args[a.length + 2] = (byte) (crc >> 8);
        xfer(cdb(cmd, args), data, 0);
    }

    /** Load JieLi's flash loader (shipped already ciphered: sent as it is) into RAM and start it. */
    @Override public void startLoader(byte[] blob) throws RescueFail {
        for (int off = 0; off < blob.length; off += IO)
            writeBlock(CMD_WRITE_MEMORY, LOADER_ADDR + off, Arrays.copyOfRange(blob, off, Math.min(off + IO, blob.length)));
        cmd(CMD_JUMP, be(LOADER_ADDR, 4, LOADER_ARG, 2));
    }

    /** {chip key, flash type, flash id}; an FM-1 is {980F, 3, 856014}. */
    @Override public int[] chip() throws RescueFail {
        byte[] p = cmd(CMD_READ_KEY, be(0x00AC6900, 4));
        byte[] k = {p[5], p[4]};
        Jl.crcCipher(k);
        int key = (k[0] & 0xFF) | (k[1] & 0xFF) << 8;
        p = cmd(CMD_GET_ONLINE_DEVICE, new byte[0]);
        int id = (p[2] & 0xFF) | (p[3] & 0xFF) << 8 | (p[4] & 0xFF) << 16 | (p[5] & 0xFF) << 24;
        return new int[] {key, p[0] & 0xFF, id};
    }

    @Override public byte[] read(int addr, int n, Progress pr) throws RescueFail {
        byte[] out = new byte[n];
        for (int got = 0; got < n; ) {
            int k = Math.min(IO, n - got);
            byte[] b = xfer(cdb(CMD_READ_FLASH, be(addr + got, 4, k, 2)), null, k);
            System.arraycopy(b, 0, out, got, k);
            got += k;
            if (pr != null && (got % 0x10000 == 0 || got == n)) pr.at(got, n);
        }
        return out;
    }

    /** Erase, write and read back one 4 KiB sector of the application area; nothing else is ever written. */
    @Override public void writeSector(int addr, byte[] data) throws RescueFail {
        if (addr < WRITE_MIN || addr >= Fwsc.APP_END || addr % SECTOR != 0 || data.length != SECTOR)
            throw new RescueFail(String.format("refusing to write %#x (outside the application area)", addr), true);
        cmd(CMD_ERASE_SECTOR, be(addr, 4));
        for (int off = 0; off < SECTOR; off += IO)
            writeBlock(CMD_WRITE_FLASH, addr + off, Arrays.copyOfRange(data, off, off + IO));
        if (!Arrays.equals(read(addr, SECTOR, null), data))
            throw new RescueFail(String.format("sector %#07x did not read back as written", addr));
    }

    /** Leave the loader and start the firmware; the FM-1 may reset before it answers. */
    @Override public void runApp() {
        try { cmd(CMD_RUN_APP, be(1, 4)); } catch (RescueFail ignored) { }
    }

    /** Keep the loader from resetting the chip (it does after ~3 s without a command). */
    @Override public void ping() throws RescueFail { cmd(CMD_GET_ONLINE_DEVICE, new byte[0]); }
}
