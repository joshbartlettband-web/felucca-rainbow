# FM-1 Rescue (Android)

An Android app that puts firmware back on an M-VAVE FM-1 whose firmware crashes at start-up, with only a phone and
an OTG adapter. No computer, Transporter or soldering.

## When it applies

After two failed starts, Felucca and Rainbow mode, X0X and others send the FM-1 to its chip's own boot mode, the
mask-ROM "UBOOT1.00". The screen stays black, with no lights and no sound. On USB the FM-1 is then **4C4A:8057**,
"WL80UBOOT1.00", a mass-storage device with no files on it. A phone may call it a "generic USB device". The web
installer cannot reach it: it only talks USB-MIDI, and Chrome does not let web pages use mass-storage devices.
[usb-check.html](../landing/usb-check.html) on the site shows which state an FM-1 is in.

An FM-1 that shows up as "Felucca Update" (1209:0002) does not need this app: the web installer finishes the install.

## What it does

The same steps and checks as [fm1_rescue.py](https://github.com/charlesvestal/fm1-x0x/blob/main/tools/fm1_rescue.py)
(charlesvestal/fm1-x0x, GPL-3.0), over the protocol documented and checked on real hardware by
[FM-1-transporter](https://github.com/kurogedelic/FM-1-transporter/blob/main/docs/PROTOCOL.md) (kurogedelic, MIT):

1. It catches the FM-1 in its boot mode and takes it from Android's storage driver. Android's probing would
   otherwise make it restart into the crash.
2. It loads JieLi's flash loader (`wl82loader.bin` from kagaimiq/jl-uboot-tool, downloaded and checked against
   its sha256) and checks that the chip and flash are an FM-1's: key 980F, flash 856014.
3. It reads the whole 1 MiB flash and saves it to `Downloads/FM-1 Rescue/` before anything is written.
4. It never writes the start-up area `[0, 0x4000)`, and requires it to be the known FM-1 start-up area. It never
   touches saved data above `0x93000`.
5. It writes only the 4 KiB sectors of `[0x4000, 0x93000)` that differ from the chosen firmware, high to low,
   reading each one back. Then it reads everything back and starts the firmware.

**Check only** does steps 1 to 4 and writes nothing. If the FM-1 drops out mid-way, the app waits for it to come
back and starts again (up to 6 tries). Writing again is safe, because only differing sectors are written.

## The firmware to put on

M-VAVE's official V15 (`FM-1.fwsc`, sha256 `db1642b2…`) is the default and the safe choice: it is known to start.
The app downloads it from M-VAVE's own server, or you can pick a downloaded copy. A Felucca or Rainbow mode package
(`felucca-*.fwsc`, identity FM-1_9xx) also works, but do not choose the build that crashed. Rainbow mode can go back
on afterwards with the web installer, from a running V15.

## Using it

1. Install the APK from the `fm1-rescue-test` prerelease. Android asks you to allow installing from the browser.
2. Open FM-1 Rescue. Choose **Download M-VAVE's official V15**, then **Repair**, or **Check only** first.
3. Plug the FM-1 into the phone through an OTG adapter (USB-C plug to USB-A socket) and a USB-A to USB-C data cable,
   and switch it on.
4. When Android asks whether to open FM-1 Rescue for the USB device, tick **Always** and tap OK.
5. Wait for "Done", and keep the cable still. **Copy the log** gives a report to share if something goes wrong.

## Building and testing

- The GitHub workflow `.github/workflows/fm1-rescue.yml` builds the APK and publishes the prerelease.
- `core-test/SimTest.java` runs the rescue core, in plain Java, against a simulated FM-1 boot mode: check only,
  repair, repeat, a drop mid-write and a second session, the wrong chip, an unknown start-up area, a damaged package.
  Pass a real 1 MiB FM-1 flash dump as the second argument for the full run. Without one, only the start-up area
  refusal can be checked.

```
cd android/core-test
javac --release 17 -d build $(find ../app/src/main/java -path '*core*' -name '*.java') SimTest.java
java -cp build SimTest wl82loader.bin [fm1-flash-dump.bin]
```

Use at your own risk; this is an independent fan project, not made or endorsed by M-VAVE.
