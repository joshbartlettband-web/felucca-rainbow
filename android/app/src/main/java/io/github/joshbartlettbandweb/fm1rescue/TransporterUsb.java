// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue;

import android.hardware.usb.UsbConstants;
import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbDeviceConnection;
import android.hardware.usb.UsbEndpoint;
import android.hardware.usb.UsbInterface;
import android.hardware.usb.UsbManager;

import io.github.joshbartlettbandweb.fm1rescue.core.RescueFail;
import io.github.joshbartlettbandweb.fm1rescue.core.Transporter;

/**
 * The FM-1 Transporter (XIAO RP2040, 2E8A:000A) over USB: two CDC-ACM serial channels, interfaces 0/1 the console
 * (one-line diagnostics, shown in the app's log) and 2/3 the data channel (Transporter.Link). The Transporter only
 * sends on a channel whose DTR is set (tud_cdc_n_connected), so both get SET_CONTROL_LINE_STATE.
 */
final class TransporterUsb implements Transporter.Link, AutoCloseable {
    interface Console { void line(String s); }

    private final UsbDeviceConnection conn;
    private final UsbInterface dataItf, consoleItf;
    private final UsbEndpoint in, out, consoleIn;
    private volatile boolean open = true;

    private TransporterUsb(UsbDeviceConnection conn, UsbInterface dataItf, UsbEndpoint in, UsbEndpoint out,
                           UsbInterface consoleItf, UsbEndpoint consoleIn) {
        this.conn = conn;
        this.dataItf = dataItf;
        this.in = in;
        this.out = out;
        this.consoleItf = consoleItf;
        this.consoleIn = consoleIn;
    }

    private static UsbInterface byId(UsbDevice d, int id) {
        for (int i = 0; i < d.getInterfaceCount(); i++)
            if (d.getInterface(i).getId() == id && d.getInterface(i).getAlternateSetting() == 0) return d.getInterface(i);
        return null;
    }

    private static UsbEndpoint bulk(UsbInterface f, int dir) {
        for (int i = 0; f != null && i < f.getEndpointCount(); i++) {
            UsbEndpoint e = f.getEndpoint(i);
            if (e.getType() == UsbConstants.USB_ENDPOINT_XFER_BULK && e.getDirection() == dir) return e;
        }
        return null;
    }

    static TransporterUsb open(UsbManager m, UsbDevice d, Console console) throws RescueFail {
        UsbInterface data = byId(d, 3), cons = byId(d, 1);
        UsbEndpoint in = bulk(data, UsbConstants.USB_DIR_IN), out = bulk(data, UsbConstants.USB_DIR_OUT);
        if (in == null || out == null) throw new RescueFail("this does not look like an FM-1 Transporter (no data channel)");
        UsbDeviceConnection c = m.openDevice(d);
        if (c == null) throw new RescueFail("Android did not let the app open the Transporter (USB permission)");
        if (!c.claimInterface(data, true)) {
            c.close();
            throw new RescueFail("Android did not hand the Transporter over (claim failed)");
        }
        c.controlTransfer(0x21, 0x22, 0x0003, 2, null, 0, 1000);           // data channel: DTR + RTS
        UsbEndpoint consIn = bulk(cons, UsbConstants.USB_DIR_IN);
        boolean haveConsole = cons != null && consIn != null && c.claimInterface(cons, true);
        if (haveConsole) c.controlTransfer(0x21, 0x22, 0x0003, 0, null, 0, 1000);   // console: DTR + RTS
        TransporterUsb t = new TransporterUsb(c, data, in, out, haveConsole ? cons : null, haveConsole ? consIn : null);
        if (haveConsole && console != null) t.startConsole(console);
        return t;
    }

    private void startConsole(Console console) {
        Thread th = new Thread(() -> {
            byte[] b = new byte[512];
            StringBuilder line = new StringBuilder();
            while (open) {
                int n = conn.bulkTransfer(consoleIn, b, b.length, 500);
                for (int i = 0; i < n; i++) {
                    char ch = (char) (b[i] & 0xFF);
                    if (ch == '\r') continue;
                    if (ch != '\n') { line.append(ch); continue; }
                    if (line.length() > 0) console.line(line.toString());
                    line.setLength(0);
                }
            }
        }, "transporter-console");
        th.setDaemon(true);
        th.start();
    }

    @Override public void write(byte[] b) throws RescueFail {
        for (int off = 0; off < b.length; ) {
            int n = conn.bulkTransfer(out, b, off, Math.min(16384, b.length - off), 5000);
            if (n <= 0) throw new RescueFail("the Transporter stopped answering (USB send)");
            off += n;
        }
    }

    @Override public int read(byte[] buf, int off, int len, int timeoutMs) {
        int n = conn.bulkTransfer(in, buf, off, len, Math.max(1, timeoutMs));
        return Math.max(n, 0);
    }

    @Override public void close() {
        open = false;
        try { conn.releaseInterface(dataItf); } catch (Exception ignored) { }
        if (consoleItf != null) try { conn.releaseInterface(consoleItf); } catch (Exception ignored) { }
        conn.close();
    }
}
