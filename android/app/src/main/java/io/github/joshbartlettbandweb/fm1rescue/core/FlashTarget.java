// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue.core;

/**
 * An FM-1 in its chip's boot mode, reached either directly over USB (Uboot: the phone is the USB host) or through
 * an FM-1 Transporter (Transporter: a XIAO RP2040 wired to the FM-1's USB lines, driven over a serial link).
 * Rescue runs the same steps and checks on either.
 */
public interface FlashTarget {
    /** One line saying what answered; throws (fatal) if it is not the FM-1's boot mode. */
    String identify() throws RescueFail;

    /** Start JieLi's flash loader (wl82loader.bin, as shipped: already ciphered). */
    void startLoader(byte[] blob) throws RescueFail;

    /** {chip key, flash type, flash id}; an FM-1 is {980F, 3, 856014}. */
    int[] chip() throws RescueFail;

    interface Progress { void at(int done, int total); }

    byte[] read(int addr, int n, Progress pr) throws RescueFail;

    /** Erase, write and read back one 4 KiB sector of [0x4000, 0x93000); anything else is refused. */
    void writeSector(int addr, byte[] data) throws RescueFail;

    /** A harmless command, so the loader does not reset the chip while the app is busy elsewhere. */
    void ping() throws RescueFail;

    /** Leave the loader and start the firmware. */
    void runApp();
}
