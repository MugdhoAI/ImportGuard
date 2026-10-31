import { useState } from "react";
import { GlassImportButton } from "../components/GlassImportButton";
import { ImportGuardDock } from "../components/ImportGuardDock";
import { PredictiveArcBackdrop } from "../components/PredictiveArcBackdrop";
import { ThemeToggle } from "../components/ThemeToggle";

type Preview = { headers: string[]; columns: { name: string; empty_count: number }[]; row_count: number };
type Mapping = { source_column: string | null; target_field: string; operation: string; needs_review: boolean };
type Target = { name: string; type: string; required: boolean };

export function Landing() {
  const [preview, setPreview] = useState<Preview | null>(null);
  const [schema, setSchema] = useState<Target[]>([]);
  const [mappings, setMappings] = useState<Mapping[]>([]);
  const [approved, setApproved] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  async function loadSample() {
    setBusy(true); setMessage("Loading the bundled synthetic registration CSV…"); setApproved(false);
    try {
      const [csvResponse, schemaResponse] = await Promise.all([
        fetch("/examples/registrations.csv"), fetch("/examples/registrations_schema.json"),
      ]);
      if (!csvResponse.ok || !schemaResponse.ok) throw new Error("The bundled example could not be loaded.");
      const csv = await csvResponse.blob();
      const nextSchema: Target[] = await schemaResponse.json();
      const file = new File([csv], "registrations.csv", { type: "text/csv" });
      const form = new FormData(); form.append("file", file);
      const profileResponse = await fetch("/api/profile", { method: "POST", body: form });
      const result: Preview = await profileResponse.json();
      if (!profileResponse.ok) throw new Error("The example CSV could not be profiled.");
      const mappingForm = new FormData(); mappingForm.append("file", file);
      mappingForm.append("schema_data", JSON.stringify(nextSchema)); mappingForm.append("mode", "local");
      const mappingResponse = await fetch("/api/suggest-mappings", { method: "POST", body: mappingForm });
      const mappingResult = await mappingResponse.json();
      if (!mappingResponse.ok) throw new Error("Local suggestions could not be generated.");
      setPreview(result); setSchema(nextSchema); setMappings(mappingResult.mappings);
      setMessage(`Real sample profiled: ${result.row_count} data rows and ${result.headers.length} columns. Review the local suggestions below.`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "The sample could not be processed.");
    } finally { setBusy(false); }
  }

  function updateMapping(target_field: string, source_column: string) {
    setMappings(current => current.map(mapping => mapping.target_field === target_field
      ? { ...mapping, source_column: source_column || null, needs_review: true } : mapping));
    setApproved(false);
  }

  async function processSample() {
    if (!approved) return;
    setBusy(true); setMessage("Validating the real sample with the reviewed mapping…");
    try {
      const response = await fetch("/examples/registrations.csv");
      const file = new File([await response.blob()], "registrations.csv", { type: "text/csv" });
      const form = new FormData(); form.append("file", file); form.append("schema_data", JSON.stringify(schema));
      form.append("mappings_json", JSON.stringify(mappings.map(mapping => ({ ...mapping, needs_review: false }))));
      const result = await fetch("/api/process", { method: "POST", body: form });
      if (!result.ok) { const error = await result.json(); throw new Error(error.detail || "Validation failed."); }
      const packageBlob = await result.blob();
      const url = URL.createObjectURL(packageBlob); const link = document.createElement("a");
      link.href = url; link.download = "importguard-sample-export.zip"; document.body.append(link); link.click(); link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
      setMessage(`Sample processed: ${result.headers.get("X-Accepted-Rows")} accepted, ${result.headers.get("X-Rejected-Rows")} rejected. The real export package was downloaded.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Sample processing failed."); }
    finally { setBusy(false); }
  }

  return (
    <main id="top" className="landing-page">
      <section className="hero-scene" aria-labelledby="hero-title">
        <PredictiveArcBackdrop /><div className="hero-shade" aria-hidden="true" />
        <header className="hero-header">
          <a className="wordmark" href="/"><span className="wordmark-symbol" aria-hidden="true">IG</span><span>ImportGuard</span></a>
          <ThemeToggle />
        </header>
        <ImportGuardDock />
        <div className="hero-copy">
          <h1 id="hero-title">Make every CSV import predictable.</h1>
          <p>Map unfamiliar columns, review every transformation, and export validated data without silent changes.</p>
          <div className="hero-actions"><GlassImportButton /><a className="how-link" href="#how">See the workflow <span aria-hidden="true">↓</span></a></div>
        </div>
      </section>
      <section id="how" className="workflow-section" aria-labelledby="how-title">
        <div className="section-intro"><h2 id="how-title">Keep every decision in view.</h2><p>ImportGuard profiles CSVs and suggests local header matches. Approve mappings before validation.</p></div>
        <div className="workflow-steps">
          <article><span>01</span><h3>Profile the file</h3><p>Inspect headers, empty cells, and row counts before choosing a schema.</p></article>
          <article><span>02</span><h3>Review the mapping</h3><p>Select source columns and safe transformations; approve every mapping.</p></article>
          <article><span>03</span><h3>Validate and export</h3><p>Export accepted and rejected CSVs, validation reasons, a report, and replayable recipe.</p></article>
        </div>
      </section>
      <section id="workflow" className="sample-section" aria-labelledby="sample-title">
        <div className="sample-copy"><h2 id="sample-title">Review a real sample run.</h2><p>Run the bundled synthetic fixture locally. No Meta request is made.</p><button className="sample-button" type="button" onClick={loadSample} disabled={busy}>{busy ? "Working…" : preview ? "Reload synthetic sample" : "Load synthetic sample"}</button></div>
        <div className="sample-review" aria-live="polite">
          {!preview ? <p className="sample-empty">Load the fixture to review editable local mapping suggestions.</p> : <>
            <p className="sample-summary">{preview.row_count} rows <span>·</span> {preview.headers.length} source columns</p>
            <div className="sample-mappings">{schema.map(field => { const mapping = mappings.find(item => item.target_field === field.name); return <label key={field.name}><span>{field.name}{field.required ? " *" : ""}</span><select aria-label={`Source column for ${field.name}`} value={mapping?.source_column ?? ""} onChange={event => updateMapping(field.name, event.target.value)}><option value="">Unmapped</option>{preview.headers.map(header => <option key={header} value={header}>{header}</option>)}</select></label>; })}</div>
            <label className="sample-approval"><input type="checkbox" checked={approved} onChange={event => setApproved(event.target.checked)} /> I reviewed and approve these mappings</label>
            <button className="sample-button" type="button" disabled={!approved || busy} onClick={processSample}>Validate and export</button>
          </>}
          <p className="sample-message" role="status">{message}</p>
        </div>
      </section>
      <section id="guide" className="replay-section" aria-labelledby="replay-title"><div><h2 id="replay-title">Keep the recipe with the result.</h2><p>Each export package includes accepted.csv, rejected.csv, a validation report, and a recipe you can replay in the workspace.</p></div><a href="/app">Open the workspace <span aria-hidden="true">↗</span></a></section>
      <footer className="landing-footer"><a className="wordmark" href="#top"><span className="wordmark-symbol" aria-hidden="true">IG</span><span>ImportGuard</span></a><p>CSV profiling, validation, and replay in one local workspace.</p><a href="/privacy">Privacy and data handling</a></footer>
    </main>
  );
}
