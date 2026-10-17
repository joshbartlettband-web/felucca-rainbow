// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue.core;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * One rescue session, from a connected boot mode to a restarted FM-1. Everything happens in one session: the FM-1
 * leaves the boot mode (and crashes again) as soon as the host lets it go. The policy is fm1_rescue.py's:
 *   1. INQUIRY must say WL82; JieLi's loader is started; the chip must be an FM-1's (key 980F, flash 856014, 1 MiB);
 *   2. the whole flash is read and handed to the app as a backup before anything is written;
 *   3. the head [0, 0x4000) (SPL, chip config) is never written, and must be the FM-1's known head;
 *   4. only the differing 4 KiB sectors of [0x4000, 0x93000) are written, high to low, each read back;
 *      device data above 0x93000 is never touched;
 *   5. a final full read must equal the expected image; then the firmware is started.
 */
public final class Rescue {
    /** sha256 of flash [0, 0x4000) of an FM-1 (equal to the official V15 package's head; a factory unit's too). */
    public static final String FM1_HEAD_SHA256 = "d9f43191777656de01c7bed4f9e9ba2e34e94832c5d2ed02c3fc7ab7a6d9bd67";

    public interface Listener {
        void say(String line);

        void progress(String what, int done, int total);

        /** The whole flash as read, before anything is written: keep it (a file the user can find). */
        void backup(byte[] flash) throws RescueFail;
    }

    public static final class Result {
        public boolean wrote, verified;
        public int differing;
    }

    private Rescue() {}

    public static Result run(Uboot dev, Fwsc pkg, byte[] loader, boolean write, Listener l) throws RescueFail {
        Result res = new Result();
        String[] iq = dev.inquiry();
        l.say("Device: " + iq[0] + " " + iq[1]);
        if (!"WL82".equals(iq[0]))
            throw new RescueFail("this is not the FM-1's boot mode (it says " + iq[0] + ")", true);
        if (!Uboot.LOADER_SHA256.equals(Fwsc.sha256(loader)))
            throw new RescueFail("the flash loader file is not the expected one", true);
        dev.startLoader(loader);
        int[] chip = dev.chip();
        l.say(String.format("Chip key %04X, flash type %d, flash id %06X", chip[0], chip[1], chip[2]));
        if (chip[0] != Uboot.CHIP_KEY || chip[1] != Uboot.FLASH_TYPE || chip[2] != Uboot.FLASH_ID)
            throw new RescueFail("this is not an FM-1's chip and flash (expected key 980F, type 3, id 856014). "
                    + "Nothing was written.", true);

        l.say("Reading the whole flash (the backup) ...");
        byte[] now = dev.read(0, Uboot.FLASH_SIZE, (d, n) -> l.progress("Reading", d, n));
        l.backup(now);
        dev.ping();

        String head = Fwsc.sha256(now, 0, Uboot.WRITE_MIN);
        boolean headOk = FM1_HEAD_SHA256.equals(head)
                || (pkg.isStockV15() && Arrays.equals(Arrays.copyOf(now, Uboot.WRITE_MIN), Arrays.copyOf(pkg.flash, Uboot.WRITE_MIN)));
        l.say(headOk ? "The protected start-up area is intact." : "The protected start-up area is NOT the usual FM-1 one (" + head.substring(0, 12) + "...).");

        List<Integer> diff = new ArrayList<>();
        for (int a = Uboot.WRITE_MIN; a < Fwsc.APP_END; a += Uboot.SECTOR)
            if (!Arrays.equals(Arrays.copyOfRange(now, a, a + Uboot.SECTOR), Arrays.copyOfRange(pkg.flash, a, a + Uboot.SECTOR)))
                diff.add(a);
        res.differing = diff.size();
        l.say(diff.size() + " of " + (Fwsc.APP_END - Uboot.WRITE_MIN) / Uboot.SECTOR
                + " firmware sectors differ from " + pkg.identity + ".");
        if (!headOk)
            throw new RescueFail("Not writing: the start-up area differs from every FM-1 seen so far. "
                    + "Share the backup file and this log with the community before going further.", true);
        if (!write) {
            l.say("Check passed. Nothing was written.");
            dev.ping();
            return res;
        }
        if (diff.isEmpty()) l.say("The firmware is already the chosen one: nothing to write.");

        // high to low: the firmware's start-up code (low in the application area) is the last thing replaced,
        // so a write cut short leaves a firmware that still crashes into the boot mode, where this can run again
        for (int i = diff.size() - 1, done = 0; i >= 0; i--, done++) {
            int a = diff.get(i);
            for (int attempt = 0; ; attempt++) {
                try {
                    dev.writeSector(a, Arrays.copyOfRange(pkg.flash, a, a + Uboot.SECTOR));
                    break;
                } catch (RescueFail e) {
                    if (e.fatal || attempt == 2) throw new RescueFail(e.getMessage() + ". The FM-1 is still in its boot mode: run the repair again.");
                }
            }
            l.progress("Writing", done + 1, diff.size());
        }
        res.wrote = !diff.isEmpty();

        l.say("Reading everything back ...");
        byte[] fin = dev.read(0, Uboot.FLASH_SIZE, (d, n) -> l.progress("Verifying", d, n));
        byte[] expect = now.clone();
        System.arraycopy(pkg.flash, Uboot.WRITE_MIN, expect, Uboot.WRITE_MIN, Fwsc.APP_END - Uboot.WRITE_MIN);
        if (!Arrays.equals(fin, expect)) {
            StringBuilder bad = new StringBuilder();
            for (int a = 0; a < Uboot.FLASH_SIZE; a += Uboot.SECTOR)
                if (!Arrays.equals(Arrays.copyOfRange(fin, a, a + Uboot.SECTOR), Arrays.copyOfRange(expect, a, a + Uboot.SECTOR)))
                    bad.append(String.format(" %#07x", a));
            throw new RescueFail("the final read differs in sectors" + bad + ". Run the repair again.");
        }
        res.verified = true;
        l.say("The flash now holds " + pkg.identity + ". Restarting the FM-1 ...");
        dev.runApp();
        return res;
    }
}
