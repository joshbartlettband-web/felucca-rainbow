"""The installer's name box against a fake FM-1 on WebMIDI (Playwright, Chromium):
  python3 web/test_name_page.py web OUT.png   -> prints what it typed, sent and said"""
import sys, json, re, importlib.util
from pathlib import Path
from playwright.sync_api import sync_playwright
web, png = Path(sys.argv[1]), sys.argv[2]
spec = importlib.util.spec_from_file_location("ms", web / "make_site.py"); ms = importlib.util.module_from_spec(spec); spec.loader.exec_module(ms)
html = (web / "index_pkg.html").read_text(encoding="utf-8")
lib = "\n".join(ms.strip_module((web / f).read_text(encoding="utf-8")) for f in ("fm1pkg.js", "fm1ota.js", "fm1backup.js") if (web / f).exists())
html = html.replace("/*LIB*/", lib).replace("/*META*/", json.dumps({"version": "test", "product": "FM-1_9999", "pkg": "nope.fwsc"}))
page_path = Path(png).with_suffix(".html"); page_path.write_text(html, encoding="utf-8")
MOCK = """
window.__sent = [];
navigator.requestMIDIAccess = async () => {
  const input = { name: "Melodee", state: "connected", onmidimessage: null };
  const output = { name: "Melodee", state: "connected", send(d) {
    window.__sent.push(Array.from(d));
    if (d[4] === 50) { const name = d.slice(5, 15); const ok = name.every((c) => c === 32 || (c >= 65 && c <= 90));
      setTimeout(() => input.onmidimessage && input.onmidimessage({ data: Uint8Array.from([0xF0, 0x7D, 0x46, 0x4C, 50, ok ? 0 : 1, ...(ok ? name : Array(10).fill(32)), 0xF7]) }), 20); } } };
  return { inputs: new Map([["i", input]]), outputs: new Map([["o", output]]) };
};"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium" if Path("/opt/pw-browsers/chromium").is_file() else None)
    pg = b.new_page(viewport={"width": 420, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(MOCK)
    pg.goto(page_path.as_uri()); pg.wait_for_timeout(500)
    pg.fill("#kid-name", "maya-2 lee"); v = pg.input_value("#kid-name")
    pg.click("#name-go"); pg.wait_for_timeout(300)
    st = pg.text_content("#status"); sent = pg.evaluate("window.__sent")
    pg.fill("#kid-name", ""); pg.click("#name-go"); pg.wait_for_timeout(300); st2 = pg.text_content("#status")
    pg.screenshot(path=png, full_page=True)
    print("typed ->", repr(v)); print("status:", st); print("sent:", sent[0] if sent else None); print("cleared:", st2); print("errors:", errs)
    b.close()
