# SPDX-License-Identifier: GPL-3.0-only
"""Run the built emulator in Chromium and check that two tabs can't replace each other's songs.

    python3 -m pip install playwright
    python3 -m playwright install chromium
    python3 web/emu/browser_save_test.py build/emu
"""
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import expect, sync_playwright

STORE = "felucca-emu-flash"
TIMEOUT = 15_000

# Listen alongside the page. A worklet flash frame tells us the settings write really happened,
# even in a tab that can't put it in localStorage.
WATCH_FLASH = """
window.flashFrames = 0;
const OriginalNode = window.AudioWorkletNode;
window.AudioWorkletNode = class extends OriginalNode {
  constructor(...args) {
    super(...args);
    this.port.addEventListener("message", ({data}) => {
      if (data.sectors) window.flashFrames++;
      if (data.leds) window.sweepDone = !data.anim;
    });
  }
};
"""


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def saved_flash(page):
    return page.evaluate("(key) => localStorage.getItem(key)", STORE)


def switch_on(page):
    page.bring_to_front()
    page.get_by_role("button", name="Switch on").click()
    expect(page.locator("#start")).to_be_hidden(timeout=TIMEOUT)
    page.wait_for_function("window.sweepDone", timeout=TIMEOUT)
    # Play a note first to skip the rest of the hello.
    page.keyboard.press("KeyZ", delay=80)


def check_first_note(page):
    # E4 is yellow in the first column on the WRITE screen (kid.c).
    page.wait_for_function(
        """() => {
          const [r, g, b] = document.querySelector("canvas").getContext("2d")
            .getImageData(56, 125, 1, 1).data;
          return r === 255 && g === 219 && b === 33;
        }""",
        timeout=TIMEOUT,
    )


def lower_volume(page):
    page.bring_to_front()
    frames = page.evaluate("window.flashFrames")
    page.keyboard.down("Digit7")  # HOME opens VOLUME after one second.
    page.wait_for_timeout(1300)
    page.keyboard.press("BracketLeft", delay=100)
    page.keyboard.up("Digit7")
    page.wait_for_function("(frames) => window.flashFrames > frames", arg=frames, timeout=TIMEOUT)


def check_saves(browser, url):
    with browser.new_context() as context:
        context.route("https://**", lambda route: route.abort())
        context.add_init_script(WATCH_FLASH)
        failed = context.new_page()
        failed.route(
            "**/felucca.wasm",
            lambda route: route.fulfill(body=b"broken", content_type="application/wasm"),
        )
        failed.goto(url)
        failed.get_by_role("button", name="Switch on").click()
        expect(failed.locator("#status")).to_contain_text("Could not start", timeout=TIMEOUT)

        owner = context.new_page()
        other = context.new_page()
        for page in (owner, other):
            page.goto(url)
            switch_on(page)

        owner.bring_to_front()
        previous = saved_flash(owner)
        owner.keyboard.press("Digit8", delay=80)  # SAVE opens WRITE.
        owner.keyboard.press("KeyM", delay=100)   # Put E4 into the song.
        check_first_note(owner)
        owner.wait_for_function(
            "([key, old]) => localStorage.getItem(key) !== old", arg=[STORE, previous], timeout=TIMEOUT
        )
        song = saved_flash(owner)

        lower_volume(other)
        assert saved_flash(other) == song, "The second tab's volume change replaced the first tab's song"
        expect(other.get_by_role("status")).to_contain_text("temporary")

        owner.close()
        other.reload()
        switch_on(other)
        other.keyboard.press("Digit8", delay=80)
        check_first_note(other)
        other.keyboard.press("Digit8", delay=80)
        lower_volume(other)
        other.wait_for_function(
            "([key, old]) => localStorage.getItem(key) !== old", arg=[STORE, song], timeout=TIMEOUT
        )
        song_with_volume = saved_flash(other)
        other.close()

        fallback = context.new_page()
        fallback.add_init_script("Object.defineProperty(navigator, 'locks', {value: undefined});")
        fallback.goto(url)
        switch_on(fallback)
        fallback.keyboard.press("Digit8", delay=80)
        check_first_note(fallback)
        fallback.keyboard.press("Digit8", delay=80)
        lower_volume(fallback)
        assert saved_flash(fallback) == song_with_volume, "A tab without Web Locks replaced the saved flash"
        expect(fallback.get_by_role("status")).to_contain_text("Changes last")


def main():
    emu = Path(sys.argv[1] if len(sys.argv) > 1 else "build/emu").resolve()
    handler = partial(QuietHandler, directory=emu)
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server, sync_playwright() as p:
        Thread(target=server.serve_forever, daemon=True).start()
        try:
            with p.chromium.launch() as browser:
                check_saves(browser, f"http://127.0.0.1:{server.server_port}/")
        finally:
            server.shutdown()
    print("Browser saves pass. A failed start lets go, and the song survives a handoff.")


if __name__ == "__main__":
    main()
