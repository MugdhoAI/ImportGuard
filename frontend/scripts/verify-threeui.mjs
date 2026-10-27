import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const vendorRoot = join(root, "src", "vendor", "threeui");
const fontUrl = "https://raw.githubusercontent.com/MengTo/threeui/main/src/shaders/fonts/fragment-mono.woff2";
const pinned = new Map([
  ["src/shaders/predictive-arc/PredictiveArcCollection.tsx", "b77a845ab2fa8e8ef8d9b6812d71efe6f320d865d97ec97b2e15253b5950fd63"],
  ["src/shaders/predictive-arc/PredictiveArcCanvas.tsx", "ebaa5a1b1f785c7772aaedc2b195318fd63bd9c3e5e5d8e175600968b245dae7"],
  ["src/shaders/predictive-arc/predictiveArcRenderer.ts", "fc08c66b13c4a8173c8a88845926b72266d1b1a4fc345c84f44ee61fbfaba92b"],
  ["src/shaders/glass-ai-button/GlassAiButton.tsx", "1a11cd583e856d3be328a0192be4d77184607c64721f3fb646bd6d61436b2104"],
  ["src/shaders/glass-ai-button/sources/glass-ai-button.html", "a484571de316c05ab7fbd2da82da5e028ee1ffe0bd169449fb8a3c7801abd81e"],
  ["src/shaders/animated-top-dock/AnimatedTopDock.tsx", "50ddbba7ebc81565f42bd14dda34efb45e7b18c1aa47e97f196256ffedb4478f"],
  ["src/shaders/animated-top-dock/topDockController.ts", "506ab23d4d42cf1b5bc89131e7714586ee107381bb18d9b0302766e9a1dee2bd"],
  ["src/shaders/animated-top-dock/retroPixelField.ts", "54f0469be51dfce2da7ce37c952d42c583cc7996794bf96d1ea0b2bb35d94115"],
  ["src/shaders/animated-top-dock/glassParticleField.ts", "bc9f07ae6da33b28f82303ea937095806f8e3a2ab08bd1301ae8457aaf0c3464"],
  ["src/shaders/threeui.css", "efe4447139f1358dd8e9be68edf6fa46cbefbd1de423a4d6c439ca61d2c8eccf"],
]);
const hash = (value) => createHash("sha256").update(value).digest("hex");
const files = [];

for (const bundleName of ["predictive-arc", "glass-ai-button", "animated-top-dock"]) {
  const response = await fetch(`https://threeui.com/source-code/${bundleName}.json`);
  if (!response.ok) throw new Error(`${bundleName}: HTTP ${response.status}`);
  const bundle = await response.json();
  for (const file of bundle.files) {
    const localPath = join(vendorRoot, ...file.path.replace(/^src\//, "").split("/"));
    const local = await readFile(localPath);
    const localHash = hash(local);
    const canonicalHash = hash(file.code);
    if (canonicalHash !== file.sha256 || localHash !== canonicalHash) {
      throw new Error(`${file.path}: local or manifest SHA-256 mismatch`);
    }
    const expected = pinned.get(file.path);
    if (expected && expected !== localHash) throw new Error(`${file.path}: supplied SHA-256 mismatch`);
    files.push({ bundle: bundleName, path: file.path, bytes: local.length, sha256: localHash });
  }
}

for (const [path, expected] of pinned) {
  if (!files.some((file) => file.path === path)) throw new Error(`${path}: missing from canonical bundles`);
  if (path === "src/shaders/threeui.css") continue;
}

const fontResponse = await fetch(fontUrl);
if (!fontResponse.ok) throw new Error(`Fragment Mono: HTTP ${fontResponse.status}`);
const font = Buffer.from(await fontResponse.arrayBuffer());
const fontHash = hash(font);
if (fontHash !== "4f4dc27f4a770c0d02fde800daa836c8adc0d1e423b28da74baaf0d1cc3ab96c") {
  throw new Error(`Fragment Mono: SHA-256 mismatch (${fontHash})`);
}
const localFont = await readFile(join(vendorRoot, "shaders", "fonts", "fragment-mono.woff2"));
if (hash(localFont) !== fontHash) throw new Error("Local Fragment Mono asset differs from the verified ThreeUI source.");

const record = {
  verifiedAt: new Date().toISOString(),
  bundles: ["predictive-arc", "glass-ai-button", "animated-top-dock"],
  files,
  font: { path: "src/shaders/fonts/fragment-mono.woff2", bytes: font.length, sha256: fontHash, source: fontUrl },
};
await writeFile(join(vendorRoot, "VERIFICATION.json"), `${JSON.stringify(record, null, 2)}\n`);
console.log(`Verified ${files.length} source files and Fragment Mono (${font.length} bytes).`);
