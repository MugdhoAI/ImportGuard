import { copyFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const copyPairs = [
  ["src/vendor/threeui/shaders/threeui.css", "public/vendor/threeui/shaders/threeui.css"],
  ["src/vendor/threeui/shaders/fonts/fragment-mono.woff2", "public/vendor/threeui/shaders/fonts/fragment-mono.woff2"],
];

for (const [source, target] of copyPairs) {
  const targetPath = resolve(root, target);
  await mkdir(dirname(targetPath), { recursive: true });
  await copyFile(resolve(root, source), targetPath);
}

console.log("Prepared the unchanged ThreeUI stylesheet and its verified font asset.");
