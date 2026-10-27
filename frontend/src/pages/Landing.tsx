import { PredictiveArcBackdrop } from "../components/PredictiveArcBackdrop";

export function Landing() {
  return (
    <main id="top" className="landing-page">
      <section className="hero-scene" aria-labelledby="hero-title">
        <PredictiveArcBackdrop />
        <div className="hero-shade" aria-hidden="true" />
        <header className="hero-header">
          <a className="wordmark" href="/" aria-label="ImportGuard home">
            <span className="wordmark-symbol" aria-hidden="true">IG</span>
            <span>ImportGuard</span>
          </a>
        </header>
        <div className="hero-copy">
          <h1 id="hero-title">Make every CSV import predictable.</h1>
          <p>Map unfamiliar columns, review every transformation, and export validated data without silent changes.</p>
          <div className="hero-actions">
            <a className="import-link" href="/app">Start an import <span aria-hidden="true">↗</span></a>
            <a className="how-link" href="#how">See how it works <span aria-hidden="true">↓</span></a>
          </div>
        </div>
        <a className="scene-scroll" href="#how">Explore the workflow <span aria-hidden="true">↓</span></a>
      </section>
      <section id="how" className="hero-first-followup" aria-labelledby="how-title">
        <h2 id="how-title">A reviewable path from file to export.</h2>
        <p>The full workflow is being connected here; your CSV tools remain available in the workspace.</p>
        <a href="/app">Open the workspace</a>
      </section>
    </main>
  );
}
