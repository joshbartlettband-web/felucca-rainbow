// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue;

import android.hardware.usb.UsbConstants;
import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbDeviceConnection;
import android.hardware.usb.UsbEndpoint;
import android.hardware.usb.UsbInterface;
import android.hardware.usb.UsbManager;

import io.github.joshbartlettbandweb.fm1rescue.core.RescueFail;
import io.github.joshbartlettbandweb.fm1rescue.core.Transport;

/** The boot mode's mass storage interface, taken from Android's own USB storage driver (claimInterface force). */
final class UsbTransport implements Transport, AutoCloseable {
    private final UsbDeviceConnection conn;
    private final UsbInterface intf;
    private final UsbEndpoint in, out;

    private UsbTransport(UsbDeviceConnection conn, UsbInterface intf, UsbEndpoint in, UsbEndpoint out) {
        this.conn = conn;
        this.intf = intf;
        this.in = in;
        this.out = out;
    }

    static UsbTransport open(UsbManager m, UsbDevice d) throws RescueFail {
        if (d.getInterfaceCount() == 0) throw new RescueFail("the FM-1 shows no USB interface yet");
        UsbInterface intf = d.getInterface(0);
        for (int i = 0; i < d.getInterfaceCount(); i++)
            if (d.getInterface(i).getInterfaceClass() == UsbConstants.USB_CLASS_MASS_STORAGE) { intf = d.getInterface(i); break; }
        UsbEndpoint in = null, out = null;
        for (int i = 0; i < intf.getEndpointCount(); i++) {
            UsbEndpoint e = intf.getEndpoint(i);
            if (e.getType() != UsbConstants.USB_ENDPOINT_XFER_BULK) continue;
            if (e.getDirection() == UsbConstants.USB_DIR_IN) in = e; else out = e;
        }
        if (in == null || out == null) throw new RescueFail("the FM-1's boot mode shows no bulk endpoints");
        UsbDeviceConnection c = m.openDevice(d);
        if (c == null) throw new RescueFail("Android did not let the app open the FM-1 (USB permission)");
        if (!c.claimInterface(intf, true)) {   // force: detach Android's storage driver, which would upset it
            c.close();
            throw new RescueFail("Android did not hand the FM-1 over (claim failed)");
        }
        return new UsbTransport(c, intf, in, out);
    }

    @Override public int bulkOut(byte[] data, int len, int timeoutMs) { return conn.bulkTransfer(out, data, len, timeoutMs); }

    @Override public int bulkIn(byte[] buf, int len, int timeoutMs) { return conn.bulkTransfer(in, buf, len, timeoutMs); }

    @Override public void resetRecovery() {
        conn.controlTransfer(0x21, 0xFF, 0, intf.getId(), null, 0, 2000);              // bulk-only mass storage reset
        for (UsbEndpoint e : new UsbEndpoint[] {in, out})                               // CLEAR_FEATURE(ENDPOINT_HALT)
            conn.controlTransfer(0x02, 0x01, 0, e.getAddress(), null, 0, 2000);
    }

    @Override public void close() {
        try { conn.releaseInterface(intf); } catch (Exception ignored) { }
        conn.close();
    }
}
