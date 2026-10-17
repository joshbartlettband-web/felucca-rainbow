// SPDX-License-Identifier: GPL-3.0-only
package io.github.joshbartlettbandweb.fm1rescue;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.ContentValues;
import android.content.Intent;
import android.graphics.Typeface;
import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.provider.MediaStore;
import android.util.TypedValue;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.TextView;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import io.github.joshbartlettbandweb.fm1rescue.core.Fwsc;
import io.github.joshbartlettbandweb.fm1rescue.core.Rescue;
import io.github.joshbartlettbandweb.fm1rescue.core.RescueFail;
import io.github.joshbartlettbandweb.fm1rescue.core.Uboot;

/**
 * FM-1 Rescue: puts firmware back on an M-VAVE FM-1 that crashes at start-up and so sits in the chip's boot mode
 * (USB 4C4A:8057, "WL80UBOOT1.00"), from an Android phone with an OTG adapter. One screen: pick the firmware,
 * press Check or Repair, plug the FM-1 in. The rescue itself is core/Rescue.java.
 */
public class MainActivity extends Activity {
    private static final int PICK = 1, MAX_SESSIONS = 6;
    private static final String ACTION_PERMISSION = "io.github.joshbartlettbandweb.fm1rescue.USB_PERMISSION";

    private final Handler ui = new Handler(Looper.getMainLooper());
    private final ExecutorService io = Executors.newSingleThreadExecutor();
    private final Set<String> asked = new HashSet<>();
    private UsbManager usb;
    private TextView fwText, status, log;
    private Button checkBtn, repairBtn, stopBtn;
    private ProgressBar bar;
    private Fwsc firmware;
    private byte[] loader;
    private boolean waiting, running, writeMode;
    private int sessions;
    private File lastBackup;

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        usb = (UsbManager) getSystemService(USB_SERVICE);
        buildUi();
        say("FM-1 Rescue " + BuildConfig.VERSION_NAME + " on Android " + Build.VERSION.RELEASE + ", " + Build.MANUFACTURER + " " + Build.MODEL);
        File cachedV15 = new File(getFilesDir(), "FM-1.fwsc");
        if (cachedV15.exists()) useFirmwareFile(cachedV15);
        io.execute(this::fetchLoader);
    }

    @Override protected void onNewIntent(Intent intent) {   // the FM-1 attached and Android chose this app for it
        super.onNewIntent(intent);
        if (UsbManager.ACTION_USB_DEVICE_ATTACHED.equals(intent.getAction()) && waiting) poll.run();
    }

    // ------------------------------------------------------------------ the screen ---
    private int dp(int v) { return (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v, getResources().getDisplayMetrics()); }

    private TextView text(LinearLayout parent, String s, float sp, boolean bold) {
        TextView t = new TextView(this);
        t.setText(s);
        t.setTextSize(TypedValue.COMPLEX_UNIT_SP, sp);
        if (bold) t.setTypeface(Typeface.DEFAULT_BOLD);
        t.setPadding(0, dp(6), 0, dp(6));
        parent.addView(t);
        return t;
    }

    private Button button(LinearLayout parent, String s, View.OnClickListener l) {
        Button b = new Button(this);
        b.setText(s);
        b.setAllCaps(false);
        b.setOnClickListener(l);
        parent.addView(b, new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT));
        return b;
    }

    private void buildUi() {
        ScrollView sv = new ScrollView(this);
        LinearLayout col = new LinearLayout(this);
        col.setOrientation(LinearLayout.VERTICAL);
        col.setPadding(dp(16), dp(24), dp(16), dp(32));
        sv.addView(col);
        text(col, "FM-1 Rescue", 26, true);
        text(col, "For an FM-1 that stays black because its firmware crashes at start-up. After two failed starts the "
                + "FM-1 waits in its chip's own boot mode; this app reaches it there through an OTG adapter, backs up "
                + "the whole memory to your Downloads, and writes firmware back. The start-up area and your saved data "
                + "are never written.", 15, false);

        text(col, "1. The firmware to put on", 18, true);
        fwText = text(col, "None chosen yet. M-VAVE's official V15 is the safe choice: it is known to start. "
                + "You can put Rainbow mode back afterwards with the web installer.", 15, false);
        button(col, "Download M-VAVE's official V15", v -> io.execute(this::downloadV15));
        button(col, "Choose a .fwsc file on this phone", v -> {
            Intent i = new Intent(Intent.ACTION_OPEN_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("*/*");
            startActivityForResult(i, PICK);
        });

        text(col, "2. Connect and run", 18, true);
        text(col, "Press a button below, then plug the FM-1 into the OTG adapter and switch it on. When Android asks "
                + "whether to open FM-1 Rescue for the USB device, tick \"Always\" and tap OK: the FM-1 restarts every "
                + "few seconds until it is caught, and \"Always\" lets the app catch it at once.", 15, false);
        checkBtn = button(col, "Check only (back up, write nothing)", v -> arm(false));
        repairBtn = button(col, "Repair (back up, then write the firmware)", v -> arm(true));
        stopBtn = button(col, "Stop waiting", v -> stopWaiting("Stopped."));
        status = text(col, "", 16, true);
        bar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        bar.setMax(1000);
        col.addView(bar);

        text(col, "Log", 18, true);
        button(col, "Copy the log", v -> {
            ClipboardManager cm = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
            cm.setPrimaryClip(ClipData.newPlainText("FM-1 Rescue log", log.getText()));
            setStatus("Log copied: paste it where you ask for help.");
        });
        log = new TextView(this);
        log.setTypeface(Typeface.MONOSPACE);
        log.setTextSize(TypedValue.COMPLEX_UNIT_SP, 12);
        log.setTextIsSelectable(true);
        col.addView(log);
        setContentView(sv);
        refreshButtons();
    }

    private void refreshButtons() {
        boolean ready = firmware != null && loader != null && !waiting && !running;
        checkBtn.setEnabled(ready);
        repairBtn.setEnabled(ready);
        stopBtn.setEnabled(waiting);
    }

    private void say(String line) {
        ui.post(() -> log.append(new SimpleDateFormat("HH:mm:ss", Locale.US).format(new Date()) + "  " + line + "\n"));
    }

    private void setStatus(String s) { ui.post(() -> status.setText(s)); }

    // ------------------------------------------------------------------ the files ---
    private static byte[] get(String url) throws Exception {
        HttpURLConnection c = (HttpURLConnection) new URL(url).openConnection();
        c.setConnectTimeout(20000);
        c.setReadTimeout(60000);
        try (InputStream in = c.getInputStream()) {
            if (c.getResponseCode() != 200) throw new Exception("HTTP " + c.getResponseCode());
            ByteArrayOutputStream o = new ByteArrayOutputStream();
            byte[] buf = new byte[16384];
            for (int n; (n = in.read(buf)) > 0; ) o.write(buf, 0, n);
            return o.toByteArray();
        } finally {
            c.disconnect();
        }
    }

    private void fetchLoader() {
        File f = new File(getFilesDir(), "wl82loader.bin");
        try {
            byte[] b = f.exists() ? Files.readAllBytes(f.toPath()) : get(Uboot.LOADER_URL);
            if (!Uboot.LOADER_SHA256.equals(Fwsc.sha256(b))) throw new Exception("unexpected contents");
            if (!f.exists()) Files.write(f.toPath(), b);
            loader = b;
            say("JieLi's flash loader is ready (checked).");
        } catch (Exception e) {
            say("Could not get JieLi's flash loader (" + e.getMessage() + "). Check the internet connection and restart the app.");
        }
        ui.post(this::refreshButtons);
    }

    private void downloadV15() {
        setStatus("Downloading V15 ...");
        try {
            byte[] raw = get(Fwsc.STOCK_V15_URL);
            if (!Fwsc.STOCK_V15_SHA256.equals(Fwsc.sha256(raw)))
                throw new Exception("the downloaded file is not the expected V15");
            File f = new File(getFilesDir(), "FM-1.fwsc");
            Files.write(f.toPath(), raw);
            useFirmwareFile(f);
            setStatus("");
        } catch (Exception e) {
            say("V15 download failed: " + e.getMessage() + ". You can download FM-1.fwsc from m-vave.com (Download, "
                    + "PC Firmware) in the browser and choose it with the other button.");
            setStatus("V15 download failed.");
        }
    }

    private void useFirmwareFile(File f) {
        try { useFirmware(Files.readAllBytes(f.toPath())); }
        catch (Exception e) { say("Could not read " + f.getName() + ": " + e.getMessage()); }
    }

    private void useFirmware(byte[] raw) throws RescueFail {
        Fwsc p = Fwsc.parse(raw);
        if (!p.identity.startsWith("FM-1_"))
            throw new RescueFail("this package is for " + (p.identity.isEmpty() ? "another device" : p.identity) + ", not an FM-1", true);
        firmware = p;
        String what = p.isStockV15() ? "M-VAVE's official V15 (verified)"
                : p.isFelucca() ? p.identity + " (a Felucca build such as Rainbow mode). If the FM-1 crashed with this "
                + "build, put V15 on instead." : p.identity;
        say("Firmware: " + what + ", sha256 " + p.sha256.substring(0, 16) + "...");
        ui.post(() -> { fwText.setText("Chosen: " + what); refreshButtons(); });
    }

    @Override protected void onActivityResult(int req, int res, Intent data) {
        super.onActivityResult(req, res, data);
        if (req != PICK || res != RESULT_OK || data == null || data.getData() == null) return;
        Uri u = data.getData();
        io.execute(() -> {
            try (InputStream in = getContentResolver().openInputStream(u)) {
                ByteArrayOutputStream o = new ByteArrayOutputStream();
                byte[] buf = new byte[16384];
                for (int n; (n = in.read(buf)) > 0; ) o.write(buf, 0, n);
                useFirmware(o.toByteArray());
            } catch (Exception e) {
                say("That file cannot be used: " + e.getMessage());
            }
        });
    }

    /** Copy a backup to Downloads/FM-1 Rescue, where the user can find and share it. */
    private void publishBackup(File f) {
        try {
            ContentValues v = new ContentValues();
            v.put(MediaStore.MediaColumns.DISPLAY_NAME, f.getName());
            v.put(MediaStore.MediaColumns.MIME_TYPE, "application/octet-stream");
            v.put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/FM-1 Rescue");
            Uri u = getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, v);
            if (u == null) throw new Exception("no place in Downloads");
            try (OutputStream o = getContentResolver().openOutputStream(u)) { o.write(Files.readAllBytes(f.toPath())); }
            say("Backup saved: Downloads/FM-1 Rescue/" + f.getName());
        } catch (Exception e) {
            say("The backup stays inside the app (" + f.getName() + "): copying it to Downloads failed: " + e.getMessage());
        }
    }

    // ------------------------------------------------------------------ the rescue ---
    private void arm(boolean write) {
        writeMode = write;
        sessions = 0;
        asked.clear();
        waiting = true;
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        say(write ? "Repair armed: waiting for the FM-1 in its boot mode ..." : "Check armed: waiting for the FM-1 in its boot mode ...");
        setStatus("Plug the FM-1 in and switch it on.");
        refreshButtons();
        ui.post(poll);
    }

    private void stopWaiting(String why) {
        waiting = false;
        ui.removeCallbacks(poll);
        getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setStatus(why);
        refreshButtons();
    }

    private final Runnable poll = new Runnable() {
        @Override public void run() {
            ui.removeCallbacks(this);
            if (!waiting || running) return;
            for (UsbDevice d : usb.getDeviceList().values()) {
                if (d.getVendorId() != Uboot.VID || d.getProductId() != Uboot.PID) continue;
                if (usb.hasPermission(d)) {
                    startSession(d);
                    return;
                }
                if (asked.add(d.getDeviceName() + d.getDeviceId())) {
                    int flags = Build.VERSION.SDK_INT >= 31 ? PendingIntent.FLAG_MUTABLE : 0;
                    usb.requestPermission(d, PendingIntent.getBroadcast(MainActivity.this, 0,
                            new Intent(ACTION_PERMISSION).setPackage(getPackageName()), flags));
                    setStatus("Found it: allow FM-1 Rescue to use it (tick Always).");
                }
            }
            ui.postDelayed(this, 40);
        }
    };

    private void startSession(UsbDevice d) {
        running = true;
        sessions++;
        setStatus("Connected. Do not unplug the FM-1.");
        ui.post(this::refreshButtons);
        new Thread(() -> session(d), "rescue").start();
    }

    private void session(UsbDevice d) {
        boolean again = false;
        String end;
        try (UsbTransport t = UsbTransport.open(usb, d)) {
            Uboot dev = new Uboot(t);
            try { dev.inquiry(); } catch (RescueFail e) { t.resetRecovery(); }
            Rescue.Result r = Rescue.run(dev, firmware, loader, writeMode, new Rescue.Listener() {
                @Override public void say(String line) { MainActivity.this.say(line); }

                @Override public void progress(String what, int done, int total) {
                    ui.post(() -> { bar.setProgress((int) (1000L * done / total)); status.setText(what + " " + (100L * done / total) + "%"); });
                }

                @Override public void backup(byte[] flash) throws RescueFail {   // fast: inside the app; Downloads after
                    try {
                        File dir = new File(getFilesDir(), "backups");
                        dir.mkdirs();
                        File f = new File(dir, new SimpleDateFormat("'fm1-backup-'yyyyMMdd-HHmmss'.bin'", Locale.US).format(new Date()));
                        try (FileOutputStream o = new FileOutputStream(f)) { o.write(flash); }
                        lastBackup = f;
                        MainActivity.this.say("Backup taken (" + flash.length / 1024 + " KiB, sha256 " + Fwsc.sha256(flash).substring(0, 16) + "...)");
                    } catch (Exception e) {
                        throw new RescueFail("could not keep the backup (" + e.getMessage() + "): nothing was written", true);
                    }
                }
            });
            end = !writeMode ? "Check passed: nothing was written. The FM-1 will go back to its start-up loop."
                    : r.verified ? "Done: " + firmware.identity + " is on the FM-1 and it is restarting. Its screen should come on."
                    : "Finished.";
        } catch (RescueFail e) {
            say("Stopped: " + e.getMessage());
            again = !e.fatal && sessions < MAX_SESSIONS;
            end = e.fatal ? "Stopped. Copy the log and share it." : again ? "It dropped out; waiting for it to come back (try "
                    + (sessions + 1) + " of " + MAX_SESSIONS + ") ..." : "It kept dropping out. Copy the log and share it.";
        } catch (Exception e) {
            say("Stopped: " + e);
            again = sessions < MAX_SESSIONS;
            end = "Something went wrong; waiting for the FM-1 to come back ...";
        }
        if (lastBackup != null) { publishBackup(lastBackup); lastBackup = null; }
        say(end);
        final boolean retry = again;
        final String msg = end;
        ui.post(() -> {
            running = false;
            if (retry) { setStatus(msg); refreshButtons(); poll.run(); }
            else stopWaiting(msg);
        });
    }

    @Override protected void onDestroy() {
        waiting = false;
        ui.removeCallbacks(poll);
        io.shutdownNow();
        super.onDestroy();
    }
}
