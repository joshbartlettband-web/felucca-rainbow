// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue.core;

/** The two bulk endpoints of the boot mode's mass storage interface (Android: UsbDeviceConnection; tests: a simulator). */
public interface Transport {
    /** Send len bytes; returns the count sent, or a negative number on error. */
    int bulkOut(byte[] data, int len, int timeoutMs);

    /** Receive up to len bytes into buf; returns the count, or a negative number on error. */
    int bulkIn(byte[] buf, int len, int timeoutMs);

    /** Bulk-only mass storage reset and clearing both halts (after a stall); errors ignored. */
    void resetRecovery();
}
