import fs from "fs";
const [w, outp] = process.argv.slice(2);
const { instance } = await WebAssembly.instantiate(fs.readFileSync(w), {}); const ex = instance.exports, mem = ex.memory;
ex._initialize(); ex.web_nor_erase(); ex.web_boot(); ex.web_master(1023);
const render = (ms) => { const n = Math.round(ms * 44.1); for (let k = 0; k < n; k += 128) ex.web_render(Math.min(128, n - k)); };
const grab = () => { const fb = new Uint16Array(mem.buffer, ex.web_screen(), 240 * 240), b = Buffer.alloc(240 * 56 * 3);
  for (let i = 0; i < 240 * 56; i++) { const v0 = fb[184 * 240 + i], v = ((v0 & 255) << 8) | (v0 >> 8); b[i * 3] = (v >> 11) << 3; b[i * 3 + 1] = ((v >> 5) & 63) << 2; b[i * 3 + 2] = (v & 31) << 3; } return b; };
const shots = [];
render(3000); ex.web_keys(1); render(100); ex.web_keys(0); render(1500);
for (let i = 0; i < 5; i++) { ex.web_enc(1, 1); render(100); } render(8000);
for (let s = 0; s < 34; s++) { shots.push(grab()); ex.web_buttons(1 << 9); render(80); ex.web_buttons(0); render(300); }
const cols = 4, rows = Math.ceil(shots.length / cols), all = Buffer.alloc(240 * cols * 56 * rows * 3);
shots.forEach((s, k) => { const ox = (k % cols) * 240, oy = Math.floor(k / cols) * 56; for (let y = 0; y < 56; y++) s.copy(all, ((oy + y) * 240 * cols + ox) * 3, y * 240 * 3, (y + 1) * 240 * 3); });
fs.writeFileSync(outp, Buffer.concat([Buffer.from(`P6 ${240 * cols} ${56 * rows} 255\n`), all]));
