import { createRequire } from "module";
const { chromium } = createRequire(import.meta.url)("playwright");
import fs from "fs";
const [out, w, h, ...ts] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
const page = await browser.newPage({ viewport: { width: +w, height: +h } });
page.on("pageerror", (e) => console.error("page error:", e.message));
page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") console.error("console:", m.text()); });
let t1 = Date.now();
await page.goto(`http://127.0.0.1:8765/world.html?w=${w}&h=${h}`);
await page.waitForFunction(() => window.ready === true, null, { timeout: 120000 });
console.log(`ready in ${Date.now() - t1} ms`);
for (const t of ts) {
  t1 = Date.now();
  const b64 = await page.evaluate((t) => { window.renderAt(t); return document.querySelector("canvas").toDataURL("image/jpeg", 0.9).slice(23); }, +t);
  fs.writeFileSync(`${out}/t${t}.jpg`, Buffer.from(b64, "base64"));
  console.log(`t=${t}: ${Date.now() - t1} ms`);
}
await browser.close();
