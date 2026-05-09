/**
 * Reads index.html sellable products + adds custom frame packages from orders flow.
 * Run: node shopify-migration/build-products-csv.mjs
 * Output: shopify-migration/products-import.csv (UTF-8, for Shopify Admin → Import)
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");

function escapeCsv(val) {
  if (val == null || val === "") return "";
  const s = String(val);
  if (/[",\n\r]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
  return s;
}

function handleFromSku(sku) {
  return String(sku)
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, "-")
    .replace(/^-|-$/g, "");
}

function tagsForSku(sku) {
  const u = sku.toUpperCase();
  if (u.startsWith("JEWEL")) return "תכשיטים,קריסטלים";
  if (u.startsWith("CRYSTAL")) return "קריסטלים,אבנים";
  if (u.startsWith("FRAME") || u.startsWith("GIFT") || u.startsWith("SPECIAL") || u.startsWith("ENERGY"))
    return "מסגרות,מארזים";
  if (u.startsWith("ORDER")) return "הזמנה-אישית,מסגרות";
  return "כללי";
}

function typeForSku(sku) {
  const u = sku.toUpperCase();
  if (u.startsWith("JEWEL")) return "תכשיט";
  if (u.startsWith("CRYSTAL")) return "קריסטל";
  if (u.startsWith("ORDER")) return "שירות / הזמנה אישית";
  return "מסגרת ועיצוב";
}

function parseIndexProducts(html) {
  const re =
    /data-sku="([^"]*)"\s+data-name="([^"]*)"\s+data-price="([^"]*)"\s+data-currency="([^"]*)"\s+data-image="([^"]*)"/g;
  const out = [];
  let m;
  while ((m = re.exec(html)) !== null) {
    out.push({
      sku: m[1],
      title: m[2],
      price: m[3],
      image: decodeURIComponent(m[5].replace(/\+/g, " ")),
    });
  }
  return out;
}

const extraPackages = [
  {
    sku: "ORDER-SINGLE",
    title: "מסגרת יחידה — הזמנה אישית",
    price: "300",
    body: "<p>מסגרת עץ איכותית בגודל לבחירה, קריסטל ראשי + חיזוק משלים, פענוח מסר אישי מודפס. יש לתאם פרטים בוואטסאפ לפני רכישה.</p>",
  },
  {
    sku: "ORDER-PAIR",
    title: "סט זוגי — מסגרות בהזמנה אישית",
    price: "549",
    body: "<p>שתי מסגרות בהתאמה הדדית, קריסטלים מעצימים לכל אחד, פענוח זוגי + מסר אישי לכל אחד.</p>",
  },
  {
    sku: "ORDER-FAMILY",
    title: "אוסף משפחתי — מסגרות בהזמנה אישית",
    price: "699",
    body: "<p>שלוש מסגרות בהתאמה משפחתית, בחירת קריסטלים לכל בן משפחה, מסר משפחתי מאחד + פענוח אישי.</p>",
  },
];

const vendor = "לבנה אודהליה";
const indexHtml = fs.readFileSync(path.join(root, "index.html"), "utf8");
const fromIndex = parseIndexProducts(indexHtml);

const headers = [
  "Handle",
  "Title",
  "Body (HTML)",
  "Vendor",
  "Type",
  "Tags",
  "Published",
  "Option1 Name",
  "Option1 Value",
  "Variant SKU",
  "Variant Inventory Tracker",
  "Variant Inventory Qty",
  "Variant Inventory Policy",
  "Variant Fulfillment Service",
  "Variant Price",
  "Variant Requires Shipping",
  "Variant Taxable",
  "Image Src",
  "Image Alt Text",
];

const lines = [headers.map(escapeCsv).join(",")];

for (const p of fromIndex) {
  const h = handleFromSku(p.sku);
  const row = [
    h,
    p.title,
    "",
    vendor,
    typeForSku(p.sku),
    tagsForSku(p.sku),
    "TRUE",
    "Title",
    "Default Title",
    p.sku,
    "shopify",
    "10",
    "deny",
    "manual",
    p.price,
    "TRUE",
    "TRUE",
    "",
    p.title,
  ];
  lines.push(row.map(escapeCsv).join(","));
}

for (const p of extraPackages) {
  const h = handleFromSku(p.sku);
  const row = [
    h,
    p.title,
    p.body,
    vendor,
    typeForSku(p.sku),
    tagsForSku(p.sku),
    "TRUE",
    "Title",
    "Default Title",
    p.sku,
    "shopify",
    "10",
    "deny",
    "manual",
    p.price,
    "TRUE",
    "TRUE",
    "",
    p.title,
  ];
  lines.push(row.map(escapeCsv).join(","));
}

const outPath = path.join(__dirname, "products-import.csv");
fs.writeFileSync(outPath, "\uFEFF" + lines.join("\n"), "utf8");

const manifest = {
  generated: new Date().toISOString(),
  productCount: fromIndex.length + extraPackages.length,
  localImagesReferenced: [...new Set(fromIndex.map((p) => p.image))],
  note: "Upload these files under Shopify Settings → Files, then paste URLs into products or re-export CSV with Image Src.",
};

fs.writeFileSync(
  path.join(__dirname, "asset-manifest.json"),
  JSON.stringify(manifest, null, 2),
  "utf8"
);

console.log(`Wrote ${outPath} (${manifest.productCount} products)`);
console.log(`Wrote asset-manifest.json (${manifest.localImagesReferenced.length} unique product images)`);
