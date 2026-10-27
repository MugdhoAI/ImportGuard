import { describe, expect, it } from "vitest";
import { makeImportGuardGlassDocument } from "./GlassImportButton";

describe("ImportGuard glass CTA adapter", () => {
  it("preserves the canvas source while exposing the product label and working navigation", () => {
    const adapted = makeImportGuardGlassDocument();
    expect(adapted).toContain('aria-label="Start an import"');
    expect(adapted).toContain("fillText('Start an import',508,130)");
    expect(adapted).toContain("window.parent.postMessage({type:'importguard:start-import'},'*')");
    expect(adapted).not.toContain("GPT 6 Sol");
  });

  it("rejects an unexpected canonical source before silently adapting it", () => {
    expect(() => makeImportGuardGlassDocument("<html><body></body></html>")).toThrow(/source changed/);
  });
});
