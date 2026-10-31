import { describe, expect, it } from "vitest";
import { makeImportGuardGlassDocument } from "./GlassImportButton";

describe("ImportGuard glass CTA adapter", () => {
  it("preserves the glass scene while branding its native action for ImportGuard", () => {
    const adapted = makeImportGuardGlassDocument();
    expect(adapted).toContain('aria-label="Start an import"');
    expect(adapted).toContain("fillText('',508,130)");
    expect(adapted).toContain("window.parent.postMessage({type:'importguard:start-import'},'*')");
    expect(adapted).not.toContain("GPT 6 Sol");
    expect(adapted).toContain("camera.aspect=Math.min(innerWidth/innerHeight,2.2)");
  });

  it("rejects an unexpected canonical source before silently adapting it", () => {
    expect(() => makeImportGuardGlassDocument("<html><body></body></html>")).toThrow(/source changed/);
  });
});
