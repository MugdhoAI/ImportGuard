import assert from "node:assert/strict";
import { existsSync, mkdirSync, unlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { resolve } from "node:path";
import { unzipSync } from "fflate";
import puppeteer from "puppeteer-core";

const origin = process.env.IMPORTGUARD_URL ?? "http://127.0.0.1:8000";
const executablePath = process.env.CHROME_PATH ?? "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
assert(existsSync(executablePath), `Chrome not found at ${executablePath}; set CHROME_PATH.`);
const browser = await puppeteer.launch({ executablePath, headless: true, args: ["--no-sandbox", "--disable-dev-shm-usage"] });
const errors = [];
const recipePath = resolve(tmpdir(), `importguard-browser-recipe-${process.pid}.json`);
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
page.on("pageerror", error => errors.push(error.message));
page.on("console", msg => { if (msg.type() === "error") errors.push(msg.text()); });

try {
  await page.goto(origin, { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".animated-top-dock__nav button[data-importguard-href]");
  assert.equal(await page.$eval("h1", element => element.innerText), "Make every CSV import predictable.");
  assert.equal(await page.$eval(".glass-import-frame", element => element.title), "ImportGuard import action");
  const dockItems = await page.$$eval(".dock-mount [data-importguard-href]", buttons => buttons.map(button => [button.getAttribute("aria-label"), button.dataset.importguardHref]));
  assert.deepEqual(dockItems.map(([label]) => label), ["Home", "How", "Workflow", "Import", "Privacy", "Guide"]);
  const navRect = await page.$eval(".animated-top-dock__nav", element => { const r = element.getBoundingClientRect(); return { x: r.x, width: r.width }; });
  const windowWidth = await page.evaluate(() => innerWidth);
  assert(Math.abs(navRect.x + navRect.width / 2 - windowWidth / 2) < 2, "Sable dock is horizontally centered");
  for (let i = 0; i < 9; i++) await page.keyboard.press("Tab");
  assert.equal(await page.evaluate(() => document.activeElement?.className), "glass-import-frame", "CTA remains keyboard reachable after the dock");
  const ctaFrame = await (await page.$(".glass-import-frame")).contentFrame();
  assert.equal(await ctaFrame.evaluate(() => document.activeElement?.id), "activate", "Keyboard focus reaches the CTA native button");
  assert.notEqual(await ctaFrame.$eval("#activate", element => getComputedStyle(element).outlineStyle), "none", "CTA shows keyboard focus");
  await page.keyboard.down("Shift"); await page.keyboard.press("Tab"); await page.keyboard.up("Shift");
  await page.click('[data-importguard-href="#how"]'); assert.equal(await page.evaluate(() => location.hash), "#how");
  await page.click('[data-importguard-href="#workflow"]'); assert.equal(await page.evaluate(() => location.hash), "#workflow");
  await page.click('[data-importguard-href="#guide"]'); assert.equal(await page.evaluate(() => location.hash), "#guide");
  await page.click('[data-importguard-href="#top"]'); assert.equal(await page.evaluate(() => location.hash), "#top");
  await page.click('[data-importguard-href="/privacy"]'); await page.waitForFunction(() => location.pathname === "/privacy");
  await page.goto(origin, { waitUntil: "domcontentloaded" });
  await page.click('[data-importguard-href="/app"]'); await page.waitForFunction(() => location.pathname === "/app");
  await page.goto(origin, { waitUntil: "domcontentloaded" });

  await page.click("#workflow");
  await page.click(".sample-button");
  await page.waitForSelector(".sample-summary");
  assert((await page.$eval(".sample-message", element => element.innerText)).includes("3 data rows"));
  await page.select("select[aria-label='Source column for student_id']", "Reg No");
  await page.select("select[aria-label='Source column for payment_status']", "Payment");
  await page.click(".sample-approval input");
  await page.evaluate(() => {
    const create = URL.createObjectURL.bind(URL);
    URL.createObjectURL = blob => { window.__sampleDownload = blob; return create(blob); };
  });
  await page.click(".sample-review .sample-button");
  await page.waitForFunction(() => document.querySelector(".sample-message")?.textContent?.includes("2 accepted, 1 rejected"));
  const samplePackage = await page.evaluate(async () => [...new Uint8Array(await window.__sampleDownload.arrayBuffer())]);
  assert.deepEqual(Object.keys(unzipSync(new Uint8Array(samplePackage))).sort(), ["accepted.csv", "recipe.json", "rejected.csv", "report.json"]);
  const processed = await page.evaluate(async () => {
    const [csvResponse, schemaResponse] = await Promise.all([fetch("/examples/registrations.csv"), fetch("/examples/registrations_schema.json")]);
    const csv = await csvResponse.blob(); const schema = await schemaResponse.json();
    const form = new FormData(); form.append("file", new File([csv], "registrations.csv", { type: "text/csv" }));
    form.append("schema_data", JSON.stringify(schema));
    form.append("mappings_json", JSON.stringify([
      { source_column: "Reg No", target_field: "student_id", operation: "identity", needs_review: false },
      { source_column: "Full Name", target_field: "full_name", operation: "identity", needs_review: false },
      { source_column: "Email", target_field: "email", operation: "identity", needs_review: false },
      { source_column: "Payment", target_field: "payment_status", operation: "identity", needs_review: false },
    ]));
    const response = await fetch("/api/process", { method: "POST", body: form });
    return { ok: response.ok, bytes: [...new Uint8Array(await response.arrayBuffer())] };
  });
  assert.equal(processed.ok, true);
  const archiveBytes = new Uint8Array(processed.bytes);
  const archive = unzipSync(archiveBytes);
  assert.deepEqual(Object.keys(archive).sort(), ["accepted.csv", "recipe.json", "rejected.csv", "report.json"]);
  assert.match(new TextDecoder().decode(archive["accepted.csv"]), /00127/);
  assert.match(new TextDecoder().decode(archive["rejected.csv"]), /maybe/);

  const replay = await page.evaluate(async recipeBytes => {
    const [csvResponse] = await Promise.all([fetch("/examples/registrations.csv")]);
    const data = new FormData();
    data.append("file", new File([await csvResponse.blob()], "registrations.csv", { type: "text/csv" }));
    data.append("recipe_file", new File([new Uint8Array(recipeBytes)], "recipe.json", { type: "application/json" }));
    const response = await fetch("/api/replay", { method: "POST", body: data });
    return { ok: response.ok, detail: response.ok ? "" : await response.text(), accepted: response.headers.get("X-Accepted-Rows"), rejected: response.headers.get("X-Rejected-Rows"), zip: response.ok ? [...new Uint8Array(await response.arrayBuffer())] : [] };
  }, [...archive["recipe.json"]]);
  assert.equal(replay.ok, true, `Recipe replay failed: ${replay.detail}`); assert.equal(replay.accepted, "2"); assert.equal(replay.rejected, "1");
  assert.deepEqual(Object.keys(unzipSync(new Uint8Array(replay.zip))).sort(), Object.keys(archive).sort());

  await page.click(".glass-import-shell");
  await page.waitForFunction(() => location.pathname === "/app");
  await page.waitForFunction(() => document.readyState === "complete");
  assert(await page.$("#csvFile"));
  assert(await page.$("[data-theme-toggle]"));
  await page.addScriptTag({ path: resolve("node_modules/axe-core/axe.min.js") });
  const workspaceDarkAxe = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] } })).violations.map(item => ({ id: item.id, nodes: item.nodes.map(node => node.target) })));
  assert.deepEqual(workspaceDarkAxe, [], `Dark workspace axe violations: ${JSON.stringify(workspaceDarkAxe)}`);
  const screenshotDir = resolve("../docs/visual-qa"); mkdirSync(screenshotDir, { recursive: true });
  await page.screenshot({ path: resolve(screenshotDir, "workspace-dark-1440.png"), fullPage: true });
  await page.click("[data-theme-toggle]");
  assert.equal(await page.$eval("html", element => element.dataset.theme), "light");
  await page.reload({ waitUntil: "domcontentloaded" });
  assert.equal(await page.$eval("html", element => element.dataset.theme), "light");
  await page.addScriptTag({ path: resolve("node_modules/axe-core/axe.min.js") });
  const workspaceAxe = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] } })).violations.map(item => ({ id: item.id, nodes: item.nodes.map(node => node.target) })));
  assert.deepEqual(workspaceAxe, [], `Workspace axe violations: ${JSON.stringify(workspaceAxe)}`);
  await page.screenshot({ path: resolve(screenshotDir, "workspace-light-1440.png"), fullPage: true });

  // Drive the existing workspace controls through profile, local suggestions,
  // manual correction, approval, process, and the recipe replay file chooser.
  await page.evaluate(() => {
    const create = URL.createObjectURL.bind(URL);
    URL.createObjectURL = blob => { window.__importguardLastDownload = blob; return create(blob); };
  });
  await page.click("#exampleButton");
  await page.waitForFunction(() => !document.querySelector("#profileSummary").hidden);
  await page.click("#localSuggest");
  await page.waitForFunction(() => document.querySelectorAll("#mappingTable select").length === 8);
  await page.select('select[aria-label="Source column for student_id"]', "Reg No");
  await page.select('select[aria-label="Source column for payment_status"]', "Payment");
  await page.click("#approveMappings");
  await page.click("#processButton");
  await page.waitForFunction(() => document.querySelector("#resultSummary")?.textContent?.includes("2") && !document.querySelector("#resultSummary").hidden);
  let workspaceArchiveBytes = await page.evaluate(async () => [...new Uint8Array(await window.__importguardLastDownload.arrayBuffer())]);
  const workspaceArchive = unzipSync(new Uint8Array(workspaceArchiveBytes));
  assert.deepEqual(Object.keys(workspaceArchive).sort(), ["accepted.csv", "recipe.json", "rejected.csv", "report.json"]);
  writeFileSync(recipePath, workspaceArchive["recipe.json"]);
  await (await page.$("#recipeFile")).uploadFile(recipePath);
  const csvChooserPromise = page.waitForFileChooser();
  await page.click("#replayButton");
  const csvChooser = await csvChooserPromise;
  await csvChooser.accept([resolve("../examples/registrations.csv")]);
  await page.waitForFunction(() => document.querySelector("#replayMessage")?.textContent?.includes("2 accepted, 1 rejected"));
  workspaceArchiveBytes = await page.evaluate(async () => [...new Uint8Array(await window.__importguardLastDownload.arrayBuffer())]);
  assert.deepEqual(Object.keys(unzipSync(new Uint8Array(workspaceArchiveBytes))).sort(), Object.keys(workspaceArchive).sort());
  await page.goto(`${origin}/privacy`, { waitUntil: "domcontentloaded" });
  assert(await page.$("[data-theme-toggle]"));
  assert.equal(await page.$eval("html", element => element.dataset.theme), "light");
  await page.addScriptTag({ path: resolve("node_modules/axe-core/axe.min.js") });
  const privacyAxe = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] } })).violations.map(item => ({ id: item.id, nodes: item.nodes.map(node => node.target) })));
  assert.deepEqual(privacyAxe, [], `Privacy axe violations: ${JSON.stringify(privacyAxe)}`);
  await page.click("[data-theme-toggle]");
  await page.reload({ waitUntil: "domcontentloaded" });
  await page.addScriptTag({ path: resolve("node_modules/axe-core/axe.min.js") });
  const privacyDarkAxe = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] } })).violations.map(item => ({ id: item.id, nodes: item.nodes.map(node => node.target) })));
  assert.deepEqual(privacyDarkAxe, [], `Dark privacy axe violations: ${JSON.stringify(privacyDarkAxe)}`);
  await page.goto(origin, { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".theme-toggle");
  await page.addScriptTag({ path: resolve("node_modules/axe-core/axe.min.js") });
  const axeResult = await page.evaluate(async () => {
    const result = await axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] } });
    return result.violations.map(item => ({ id: item.id, impact: item.impact, nodes: item.nodes.map(node => node.target) }));
  });
  assert.deepEqual(axeResult, [], `Landing axe violations: ${JSON.stringify(axeResult)}`);
  assert.equal(await page.$eval("html", element => element.dataset.theme), "dark");
  await page.screenshot({ path: resolve(screenshotDir, "landing-repair-dark-1440.png"), fullPage: true });
  await page.click(".theme-toggle");
  await page.waitForFunction(() => document.documentElement.dataset.theme === "light");
  assert.equal(await page.$eval("html", element => element.dataset.theme), "light");
  assert.equal(await page.evaluate(() => localStorage.getItem("importguard-theme")), "light");
  const lightLandingAxe = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] } })).violations.map(item => ({ id: item.id, nodes: item.nodes.map(node => node.target) })));
  assert.deepEqual(lightLandingAxe, [], `Light landing axe violations: ${JSON.stringify(lightLandingAxe)}`);
  await page.screenshot({ path: resolve(screenshotDir, "landing-repair-light-1440.png"), fullPage: true });
  await page.reload({ waitUntil: "domcontentloaded" });
  await page.waitForSelector(".theme-toggle");
  assert.equal(await page.$eval("html", element => element.dataset.theme), "light", "Landing theme persists across reload");
  await page.click(".theme-toggle");
  await page.waitForFunction(() => document.documentElement.dataset.theme === "dark");
  assert.equal(await page.$eval("html", element => element.dataset.theme), "dark");

  for (const width of [1920, 1440, 1280, 1024, 768, 430, 390, 360]) {
    const viewportHeight = width <= 600 ? 844 : 900;
    await page.setViewport({ width, height: viewportHeight });
    await page.goto(origin, { waitUntil: "domcontentloaded" });
    await page.waitForSelector(".hero-copy h1");
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    assert.equal(overflow, false, `Horizontal overflow at ${width}px`);
    const dock = await page.$eval(".animated-top-dock__nav", element => {
      const rect = element.getBoundingClientRect();
      return { left: rect.left, right: rect.right, bottom: rect.bottom };
    });
    assert(dock.left >= 0 && dock.right <= width, `Animated dock fits the ${width}px viewport`);
    if (width <= 600) assert(dock.bottom <= viewportHeight, `Animated dock stays inside the ${width}px mobile viewport`);
    await page.screenshot({ path: resolve(screenshotDir, `redesign-${width}-viewport.png`) });
    if (width === 1440 || width === 390) await page.screenshot({ path: resolve(screenshotDir, `redesign-${width}.png`), fullPage: true });
  }
  await page.click('.dock-mount [data-importguard-href="/privacy"]');
  await page.waitForFunction(() => location.pathname === "/privacy");

  const fallbackPage = await browser.newPage();
  await fallbackPage.setViewport({ width: 1440, height: 900 });
  await fallbackPage.evaluateOnNewDocument(() => {
    const getContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(type, ...args) {
      return type === "webgl" || type === "webgl2" ? null : getContext.call(this, type, ...args);
    };
  });
  await fallbackPage.goto(origin, { waitUntil: "domcontentloaded" });
  await fallbackPage.waitForSelector(".glass-import-fallback");
  const fallbackText = await fallbackPage.$eval(".glass-import-fallback", element => element.textContent);
  assert.match(fallbackText, /Start an import/);
  assert.match(fallbackText, /IG/);
  await fallbackPage.click(".glass-import-fallback");
  await fallbackPage.waitForFunction(() => location.pathname === "/app");
  await fallbackPage.close();

  const motionPage = await browser.newPage();
  await motionPage.setViewport({ width: 1440, height: 900 });
  await motionPage.emulateMediaFeatures([{ name: "prefers-reduced-motion", value: "reduce" }]);
  await motionPage.goto(origin, { waitUntil: "domcontentloaded" });
  await motionPage.waitForSelector(".arc-backdrop canvas");
  assert.equal(await motionPage.evaluate(() => matchMedia("(prefers-reduced-motion: reduce)").matches), true);
  const stillFrame = await motionPage.$eval(".arc-backdrop canvas", canvas => canvas.toDataURL());
  await new Promise(resolve => setTimeout(resolve, 400));
  assert.equal(await motionPage.$eval(".arc-backdrop canvas", canvas => canvas.toDataURL()), stillFrame, "Predictive Arc remains visible and still under reduced motion");
  await motionPage.close();

  assert.deepEqual(errors, [], `Browser errors: ${errors.join(" | ")}`);
  console.log("Browser flow passed: sample and workspace profile/mapping/export/replay, Glass CTA and WebGL fallback, Sable navigation, persisted themes, dark/light axe scans, reduced motion, and 8 viewport widths.");
} finally {
  if (existsSync(recipePath)) unlinkSync(recipePath);
  await browser.close();
}
