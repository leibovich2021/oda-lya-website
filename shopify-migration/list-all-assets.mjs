/**
 * Lists every image/video under project for Shopify Files upload checklist.
 * Run: node shopify-migration/list-all-assets.mjs
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");

const exts = new Set([".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".webm", ".mov"]);

function walk(dir, base = "") {
  const out = [];
  for (const name of fs.readdirSync(dir, { withFileTypes: true })) {
    const rel = path.join(base, name.name);
    const full = path.join(dir, name.name);
    if (name.isDirectory()) out.push(...walk(full, rel));
    else if (exts.has(path.extname(name.name).toLowerCase())) out.push(rel.split(path.sep).join("/"));
  }
  return out.sort();
}

const images = walk(path.join(root, "image"));
const videos = fs.existsSync(path.join(root, "video")) ? walk(path.join(root, "video")) : [];
const rootMedia = ["your-image.jpg"].filter((f) => fs.existsSync(path.join(root, f)));

const all = [...new Set([...rootMedia, ...images, ...videos])];
const outPath = path.join(__dirname, "all-assets-for-shopify.txt");
fs.writeFileSync(outPath, all.join("\n"), "utf8");
console.log(`Wrote ${outPath} (${all.length} files)`);
