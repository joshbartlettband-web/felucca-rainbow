// SPDX-License-Identifier: GPL-3.0-only
// Host test of the rescue core (android/app/src/main/java/.../core) against a simulated FM-1 boot mode:
// the same bulk-only framing and commands as the real one (FM-1-transporter docs/PROTOCOL.md).
//   javac --release 17 -d build $(find ../app/src/main/java -path '*core*' -name '*.java') SimTest.java
//   java -cp build SimTest LOADER.bin [FLASH_DUMP.bin]
// LOADER.bin: wl82loader.bin (sha256 d41da612...). FLASH_DUMP.bin: a real FM-1 flash (1 MiB) to start from; without
// it the start-up area is made up and the head check is exercised through a stock-V15 stand-in.

import io.github.joshbartlettbandweb.fm1rescue.core.*;

import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class SimTest {
    static int failures = 0;

    static void check(boolean ok, String what) {
        System.out.println((ok ? "ok   " : "FAIL ") + what);
        if (!ok) failures++;
    }

    /** The boot mode of an FM-1, then JieLi's loader once it is jumped to. */
    static final class SimFm1 implements Transport {
        final byte[] flash;
        final byte[] loaderSha;
        final int key, flashId;
        final ByteArrayOutputStream ram = new ByteArrayOutputStream();
        boolean loader = false, ranApp = false, dead = false;
        int commands = 0, dropAfter = Integer.MAX_VALUE;
        final List<String> illegalWrites = new ArrayList<>();
        int sectorsWritten = 0;
        // the transfer state
        ByteBuffer cbw;
        byte[] pendingIn, csw;
        int expectOut = 0;

        SimFm1(byte[] flash, int key, int flashId) {
            this.flash = flash;
            this.key = key;
            this.flashId = flashId;
            this.loaderSha = null;
        }

        @Override public void resetRecovery() { pendingIn = null; csw = null; expectOut = 0; }

        @Override public int bulkOut(byte[] d, int len, int timeoutMs) {
            if (dead) return -1;
            if (expectOut > 0) {                                   // the data phase of a write command
                if (len != expectOut) return -1;
                byte[] data = Arrays.copyOf(d, len);
                expectOut = 0;
                csw = status(dataOut(data));
                return len;
            }
            if (len != 31 || d[0] != 'U' || d[1] != 'S' || d[2] != 'B' || d[3] != 'C') return -1;
            if (++commands > dropAfter) { dead = true; return -1; }
            cbw = ByteBuffer.wrap(Arrays.copyOf(d, 31)).order(ByteOrder.LITTLE_ENDIAN);
            int length = cbw.getInt(8);
            boolean in = (d[12] & 0x80) != 0;
            byte[] cdb = Arrays.copyOfRange(d, 15, 15 + (d[14] & 0xFF));
            if (!in && length > 0) { expectOut = length; return len; }
            byte[] r = command(cdb, length);
            if (r == null) { pendingIn = in && length > 0 ? new byte[length] : null; csw = status(false); }
            else { pendingIn = in && length > 0 ? r : null; csw = status(true); }
            return len;
        }

        @Override public int bulkIn(byte[] buf, int len, int timeoutMs) {
            if (dead) return -1;
            byte[] src = pendingIn != null ? pendingIn : csw;
            if (src == null) return -1;
            if (pendingIn != null) pendingIn = null; else csw = null;
            int n = Math.min(len, src.length);
            System.arraycopy(src, 0, buf, 0, n);
            return n;
        }

        byte[] status(boolean ok) {
            ByteBuffer s = ByteBuffer.allocate(13).order(ByteOrder.LITTLE_ENDIAN);
            s.put("USBS".getBytes(StandardCharsets.ISO_8859_1)).putInt(cbw.getInt(4)).putInt(0).put((byte) (ok ? 0 : 1));
            return s.array();
        }

        static int u32(byte[] c, int at) { return (c[at] & 0xFF) << 24 | (c[at + 1] & 0xFF) << 16 | (c[at + 2] & 0xFF) << 8 | (c[at + 3] & 0xFF); }
        static int u16(byte[] c, int at) { return (c[at] & 0xFF) << 8 | (c[at + 1] & 0xFF); }

        byte[] echo(byte[] cdb, byte[] payload) {
            byte[] r = new byte[16];
            r[0] = cdb[0];
            r[1] = cdb[1];
            if (payload != null) System.arraycopy(payload, 0, r, 2, Math.min(14, payload.length));
            return r;
        }

        byte[] command(byte[] cdb, int length) {
            if (cdb[0] == 0x12) {                                   // INQUIRY
                byte[] r = new byte[36];
                System.arraycopy("WL82    ".getBytes(StandardCharsets.ISO_8859_1), 0, r, 8, 8);
                System.arraycopy("UBOOT1.00       ".getBytes(StandardCharsets.ISO_8859_1), 0, r, 16, 16);
                return r;
            }
            int cmd = u16(cdb, 0);
            switch (cmd) {
                case 0xFB08: {                                      // JUMP
                    byte[] blob = ram.toByteArray();
                    if (u32(cdb, 2) != 0x1C02000 || !Uboot.LOADER_SHA256.equals(Fwsc.sha256(blob))) return null;
                    loader = true;
                    return echo(cdb, null);
                }
                case 0xFC09: {                                      // READ_KEY: the answer deciphers to the key
                    if (!loader) return null;
                    byte[] ks = {0, 0};
                    Jl.crcCipher(ks);                               // the keystream
                    byte[] p = new byte[14];
                    p[5] = (byte) ((key & 0xFF) ^ (ks[0] & 0xFF));
                    p[4] = (byte) (((key >> 8) & 0xFF) ^ (ks[1] & 0xFF));
                    return echo(cdb, p);
                }
                case 0xFC0A: {                                      // GET_ONLINE_DEVICE
                    if (!loader) return null;
                    byte[] p = new byte[14];
                    p[0] = 3;
                    p[2] = (byte) flashId; p[3] = (byte) (flashId >> 8); p[4] = (byte) (flashId >> 16); p[5] = (byte) (flashId >> 24);
                    return echo(cdb, p);
                }
                case 0xFD05: {                                      // READ_FLASH
                    if (!loader) return null;
                    int a = u32(cdb, 2), n = u16(cdb, 6);
                    if (n != length || a < 0 || a + n > flash.length) return null;
                    return Arrays.copyOfRange(flash, a, a + n);
                }
                case 0xFB01: {                                      // ERASE_SECTOR
                    if (!loader) return null;
                    int a = u32(cdb, 2);
                    if (a < 0x4000 || a >= 0x93000) illegalWrites.add(String.format("erase %#x", a));
                    Arrays.fill(flash, a, a + 0x1000, (byte) 0xFF);
                    sectorsWritten++;
                    return echo(cdb, null);
                }
                case 0xFC0C:                                        // RUN_APP
                    ranApp = true;
                    return echo(cdb, null);
                default:
                    return null;
            }
        }

        byte[] lastCdb() { return Arrays.copyOfRange(cbw.array(), 15, 31); }

        boolean dataOut(byte[] data) {
            byte[] cdb = lastCdb();
            int cmd = u16(cdb, 0), a = u32(cdb, 2), n = u16(cdb, 6);
            int crc = (cdb[9] & 0xFF) | (cdb[10] & 0xFF) << 8;
            if (n != data.length || Jl.crc16(data) != crc || cdb[8] != 0) return false;
            if (cmd == 0xFB06) {                                    // WRITE_MEMORY (ROM)
                if (a != 0x1C02000 + ram.size()) return false;
                ram.write(data, 0, data.length);
                return true;
            }
            if (cmd == 0xFB04 && loader) {                          // WRITE_FLASH: NOR, bits only go to 0
                if (a < 0x4000 || a >= 0x93000) illegalWrites.add(String.format("write %#x", a));
                for (int i = 0; i < n; i++) flash[a + i] &= data[i];
                return true;
            }
            return false;
        }
    }

    /** An .fwsc holding flash image img (APP_END bytes) and identity id, in fm1pkg_make.py's layout. */
    static byte[] makePackage(byte[] img, String id) {
        int nEntries = 1, dataOff = 0x40 + 0x50 * nEntries;
        byte[] logical = new byte[dataOff + img.length];
        byte[] hdr = new byte[0x40];
        hdr[8] = (byte) nEntries;
        System.arraycopy("AC791N".getBytes(StandardCharsets.ISO_8859_1), 0, hdr, 16, 6);
        Jl.enc(hdr, 0, 0x40, 0xFFFF);
        System.arraycopy(hdr, 0, logical, 0, 0x40);
        ByteBuffer e = ByteBuffer.allocate(0x50).order(ByteOrder.LITTLE_ENDIAN);
        e.putShort((short) 0).putShort((short) 0).putShort((short) Jl.crc16(img)).putShort((short) 0).putInt(dataOff).putInt(img.length);
        byte[] eb = e.array();
        Jl.enc(eb, 0, 0x50, 0xFFFF);
        System.arraycopy(eb, 0, logical, 0x40, 0x50);
        System.arraycopy(img, 0, logical, dataOff, img.length);
        byte[] raw = new byte[logical.length + 20];
        for (int i = 0; i < 20; i++) {
            System.arraycopy(logical, i * 0x2F, raw, i * 0x30, 0x2F);
            raw[i * 0x30 + 0x2F] = (byte) (i < id.length() ? (id.charAt(i) + i + 1) & 0xFF : 0x7D);
        }
        System.arraycopy(logical, 20 * 0x2F, raw, 20 * 0x30, logical.length - 20 * 0x2F);
        return raw;
    }

    static final class Log implements Rescue.Listener {
        byte[] backup;
        final StringBuilder text = new StringBuilder();
        @Override public void say(String line) { text.append(line).append('\n'); }
        @Override public void progress(String what, int done, int total) { }
        @Override public void backup(byte[] flash) { backup = flash.clone(); }
    }

    public static void main(String[] args) throws Exception {
        byte[] loader = Files.readAllBytes(Path.of(args[0]));
        Random rng = new Random(1);
        byte[] device = new byte[Uboot.FLASH_SIZE];
        boolean realHead = args.length > 1;
        if (realHead) device = Files.readAllBytes(Path.of(args[1]));
        else rng.nextBytes(device);
        check(device.length == Uboot.FLASH_SIZE, "device flash is 1 MiB");

        // the firmware to put on: the device's own image with 12 sectors changed (and a different head in the
        // package, as Felucca packages have: the head is never written)
        byte[] img = Arrays.copyOf(device, Fwsc.APP_END);
        int[] changed = {0x4000, 0x5000, 0x10000, 0x23000, 0x40000, 0x55000, 0x60000, 0x7F000, 0x80000, 0x8A000, 0x91000, 0x92000};
        for (int a : changed) for (int i = 0; i < 0x1000; i++) img[a + i] = (byte) rng.nextInt();
        byte[] felHead = img.clone();
        for (int i = 0; i < 0x4000; i++) felHead[i] = (byte) (i * 7);
        byte[] pkgRaw = makePackage(felHead, "FM-1_904");
        Files.write(Path.of("synthetic.fwsc"), pkgRaw);
        Fwsc pkg = Fwsc.parse(pkgRaw);
        check("FM-1_904".equals(pkg.identity) && pkg.isFelucca() && !pkg.isStockV15(), "package identity read (FM-1_904)");
        check(Arrays.equals(pkg.flash, felHead), "package flash entry read back exactly");

        if (!realHead) {   // no real dump: make the device head the known FM-1 head impossible; test the refusal only
            SimFm1 sim = new SimFm1(device.clone(), 0x980F, 0x856014);
            Log log = new Log();
            try { Rescue.run(new Uboot(sim), pkg, loader, true, log); check(false, "head mismatch refused"); }
            catch (RescueFail e) { check(e.fatal && sim.sectorsWritten == 0, "unknown start-up area: refused, nothing written"); }
            check(log.backup != null && Arrays.equals(log.backup, device), "backup taken before the refusal");
            System.out.println(failures == 0 ? "\nALL PASSED (head refusal only; pass a real dump for the full run)" : "\n" + failures + " FAILED");
            System.exit(failures == 0 ? 0 : 1);
        }

        // 1. check only: backup, nothing written, firmware not started
        SimFm1 sim = new SimFm1(device.clone(), 0x980F, 0x856014);
        Log log = new Log();
        Rescue.Result r = Rescue.run(new Uboot(sim), pkg, loader, false, log);
        check(!r.wrote && sim.sectorsWritten == 0 && Arrays.equals(sim.flash, device), "check only: nothing written");
        check(Arrays.equals(log.backup, device), "check only: the backup is the whole flash");
        check(r.differing == changed.length, "check only: " + r.differing + " differing sectors found (" + changed.length + " expected)");

        // 2. repair: only the changed sectors, never the head or device data, verified, firmware started
        sim = new SimFm1(device.clone(), 0x980F, 0x856014);
        log = new Log();
        r = Rescue.run(new Uboot(sim), pkg, loader, true, log);
        byte[] expect = device.clone();
        System.arraycopy(img, 0x4000, expect, 0x4000, Fwsc.APP_END - 0x4000);
        check(r.wrote && r.verified && sim.ranApp, "repair: written, verified, firmware started");
        check(Arrays.equals(sim.flash, expect), "repair: flash = new application + the device's own head and data");
        check(sim.sectorsWritten == changed.length, "repair: wrote " + sim.sectorsWritten + " sectors, only the differing ones");
        check(sim.illegalWrites.isEmpty(), "repair: nothing written outside [0x4000, 0x93000) " + sim.illegalWrites);

        // 3. repeat on the repaired unit: nothing to write
        SimFm1 repaired = new SimFm1(sim.flash, 0x980F, 0x856014);   // a new boot-mode session on the repaired flash
        r = Rescue.run(new Uboot(repaired), pkg, loader, true, new Log());
        check(!r.wrote && r.verified && repaired.sectorsWritten == 0, "repair again: nothing to write, still verified");

        // 4. unplugged mid-write, then a second session finishes it
        sim = new SimFm1(device.clone(), 0x980F, 0x856014);
        sim.dropAfter = 2100 + 17 * 5 + 3;   // inquiry, loader (48), chip (2), read (2048), ping; then 17 per sector: in sector 6
        try { Rescue.run(new Uboot(sim), pkg, loader, true, new Log()); check(false, "drop detected"); }
        catch (RescueFail e) { check(!e.fatal, "dropped mid-way: a retryable failure (" + e.getMessage() + ")"); }
        int partly = sim.sectorsWritten;
        SimFm1 again = new SimFm1(sim.flash, 0x980F, 0x856014);   // the same flash, a new boot-mode session
        r = Rescue.run(new Uboot(again), pkg, loader, true, new Log());
        check(partly > 0 && partly < changed.length, "dropped after " + partly + " of " + changed.length + " sectors");
        check(r.verified && Arrays.equals(again.flash, expect), "second session finished and verified");
        check(again.illegalWrites.isEmpty() && sim.illegalWrites.isEmpty(), "no write outside the application area in either session");

        // 5. not an FM-1's chip: refused before reading
        sim = new SimFm1(device.clone(), 0x1234, 0x856014);
        log = new Log();
        try { Rescue.run(new Uboot(sim), pkg, loader, true, log); check(false, "wrong chip refused"); }
        catch (RescueFail e) { check(e.fatal && log.backup == null && sim.sectorsWritten == 0, "wrong chip key: refused, nothing read or written"); }

        // 6. an unknown start-up area: backup kept, nothing written
        byte[] odd = device.clone();
        odd[0x100] ^= 1;
        sim = new SimFm1(odd, 0x980F, 0x856014);
        log = new Log();
        try { Rescue.run(new Uboot(sim), pkg, loader, true, log); check(false, "odd head refused"); }
        catch (RescueFail e) { check(e.fatal && log.backup != null && sim.sectorsWritten == 0, "unknown start-up area: refused after the backup, nothing written"); }

        // 7. a damaged package is refused at once
        byte[] bad = pkgRaw.clone();
        bad[bad.length - 5000] ^= 0x40;
        try { Fwsc.parse(bad); check(false, "damaged package refused"); }
        catch (RescueFail e) { check(e.fatal, "damaged package refused (" + e.getMessage() + ")"); }

        System.out.println(failures == 0 ? "\nALL PASSED" : "\n" + failures + " FAILED");
        System.exit(failures == 0 ? 0 : 1);
    }
}
