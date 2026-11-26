// Draws frames of world.html in headless Chromium: node render.mjs FROM TO OUTDIR [W H] (frame numbers at 30 fps)
import { createRequire } from "module";
const { chromium } = createRequire(import.meta.url)("playwright");
import fs from "fs";
const [from, to, out, w = 1920, h = 1080, port = 8765] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
const page = await browser.newPage({ viewport: { width: +w, height: +h } });
page.on("pageerror", (e) => console.error("page error:", e.message));
page.on("console", (m) => { if (m.type() === "error") console.error("console:", m.text()); });
await page.goto(`http://127.0.0.1:${port}/${process.env.PAGE || "world.html"}?w=${w}&h=${h}`);
await page.waitForFunction(() => window.ready === true, null, { timeout: 120000 });
const t0 = Date.now();
for (let f = +from; f < +to; f++) {
  const b64 = await page.evaluate((t) => { window.renderAt(t); return document.querySelector("canvas").toDataURL("image/jpeg", 0.93).slice(23); }, f / 30);
  fs.writeFileSync(`${out}/f${String(f).padStart(5, "0")}.jpg`, Buffer.from(b64, "base64"));
}
console.log(`${to - from} frames in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
await browser.close();
