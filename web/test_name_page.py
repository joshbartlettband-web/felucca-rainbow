"""The installer's name box against a fake FM-1 on WebMIDI (Playwright, Chromium).

Run with python3 web/test_name_page.py web OUT.png.
"""

import importlib.util
import json
import sys
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

web, png = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
spec = importlib.util.spec_from_file_location("ms", web / "make_site.py")
assert spec is not None and spec.loader is not None
ms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ms)
html = (web / "index_pkg.html").read_text(encoding="utf-8")
lib = "\n".join(
    ms.strip_module((web / f).read_text(encoding="utf-8"))
    for f in ("fm1pkg.js", "fm1ota.js", "fm1backup.js")
)
html = html.replace("/*LIB*/", lib).replace(
    "/*META*/",
    json.dumps({"version": "9.8-rb", "product": "FM-1_900", "pkg": "fixture.fwsc"}),
)
page_path = png.with_suffix(".html")
page_path.write_text(html, encoding="utf-8")

MOCK = """
window.sentNames = [];
window.rejectName = false;
const fixture = new Uint8Array(20 * 48);
for (let i = 0; i < 20; i++) {
  fixture[i * 48 + 47] = i < 8 ? "FM-1_900".charCodeAt(i) + i + 1 : 0x7d;
}
const fetchReal = window.fetch.bind(window);
window.fetch = (url, options) => url === "fixture.fwsc"
  ? Promise.resolve(new Response(fixture)) : fetchReal(url, options);
navigator.requestMIDIAccess = async () => {
  const input = { name: "Melodee", state: "connected", onmidimessage: null };
  const output = {
    name: "Melodee",
    state: "connected",
    send(data) {
      window.sentNames.push(Array.from(data));
      if (data[4] !== 50) return;
      const name = data.slice(5, 15);
      const ok = !window.rejectName && name.every(c => c === 32 || (c >= 65 && c <= 90));
      const reply = [0xF0, 0x7D, 0x46, 0x4C, 50, ok ? 0 : 1, ...name, 0xF7];
      queueMicrotask(() => input.onmidimessage?.({ data: Uint8Array.from(reply) }));
    }
  };
  return { inputs: new Map([["i", input]]), outputs: new Map([["o", output]]) };
};
"""


def name_packet(name):
    return [0xF0, 0x7D, 0x46, 0x4C, 50, *name.ljust(10).encode("ascii"), 0xF7]


with sync_playwright() as p:
    chromium = Path("/opt/pw-browsers/chromium")
    browser = p.chromium.launch(executable_path=chromium if chromium.is_file() else None)
    page = browser.new_page(locale="en-US", viewport={"width": 420, "height": 900})
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.add_init_script(MOCK)
    page.goto(page_path.as_uri())
    expect(page.locator("#go")).to_be_enabled()
    name_box, send, status = (page.locator(sel) for sel in ("#kid-name", "#name-go", "#status"))

    name_box.fill("maya-2 lee")
    expect(name_box).to_have_value("MAYA LEE")
    send.click()
    expect(status).to_have_text("Saved. From the next power-on it says hello to MAYA LEE!")

    name_box.fill("")
    send.click()
    expect(status).to_have_text("Cleared. The hello goes back to HI!")

    page.evaluate("window.rejectName = true")
    name_box.fill("SAM")
    send.click()
    expect(status).to_have_text("Letters A to Z and spaces only.")
    assert page.evaluate("window.sentNames") == [name_packet(name) for name in ("MAYA LEE", "", "SAM")]
    assert not errors, errors
    page.screenshot(path=png, full_page=True)
    browser.close()

print("installer name: normalized, saved, cleared and rejected")
