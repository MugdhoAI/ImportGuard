import { useEffect, useRef, useState } from "react";
import glassSource from "../vendor/threeui/shaders/glass-ai-button/sources/glass-ai-button.html?raw";

const CLICK_HANDLER = "activate.addEventListener('click',()=>{if(handledDown){handledDown=false;return;}replay();});";
const IMPORT_HANDLER = "activate.addEventListener('click',()=>{if(handledDown)handledDown=false;document.querySelector('#status').textContent='Opening the import workspace';window.parent.postMessage({type:'importguard:start-import'},'*');});";

export function makeImportGuardGlassDocument(source = glassSource) {
  const replacements: Array<[string, string]> = [
    ["<title>GPT 6 Sol — Glass Galaxy</title>", "<title>ImportGuard — Start an import</title>"],
    ['aria-label="GPT 6 Sol — activate the galaxy"', 'aria-label="Start an import"'],
    ["lc.fillText('GPT 6 Sol',508,130);", "lc.fillText('Start an import',508,130);"],
    ["document.querySelector('#status').textContent='GPT 6 Sol — particle burst';", "document.querySelector('#status').textContent='Opening the import workspace';"],
    [CLICK_HANDLER, IMPORT_HANDLER],
    ["</style>", "#activate{width:90%;height:52px}\n</style>"],
  ];

  let adapted = source;
  for (const [original, replacement] of replacements) {
    if (!adapted.includes(original)) throw new Error("The verified GlassAiButton source changed; review the adapter before updating it.");
    adapted = adapted.replace(original, replacement);
  }

  const readyMessage = `<script>(()=>{const c=document.createElement('canvas');let webgl=false;try{webgl=!!c.getContext('webgl2');c.getContext('webgl2')?.getExtension('WEBGL_lose_context')?.loseContext()}catch{}window.parent.postMessage({type:'importguard:glass-status',webgl},'*')})();</script>`;
  return adapted.replace("</body>", `${readyMessage}</body>`);
}

const ADAPTED_DOCUMENT = makeImportGuardGlassDocument();

// The canonical canvas scene stays inside its source document. A native link
// overlays the canvas so ImportGuard owns keyboard, accessible naming, and the
// actual /app navigation. This product adapter does not modify vendor files.
export function GlassImportButton() {
  const frameRef = useRef<HTMLIFrameElement>(null);
  const [webglAvailable, setWebglAvailable] = useState<boolean | null>(null);

  useEffect(() => {
    const onMessage = (event: MessageEvent) => {
      if (event.source !== frameRef.current?.contentWindow) return;
      if (event.data?.type !== "importguard:glass-status" || typeof event.data.webgl !== "boolean") return;
      setWebglAvailable(event.data.webgl);
    };
    window.addEventListener("message", onMessage);
    return () => window.removeEventListener("message", onMessage);
  }, []);

  return (
    <div className={`glass-import-shell${webglAvailable === false ? " is-fallback" : ""}`}>
      {webglAvailable !== false && (
        <iframe
          ref={frameRef}
          className="glass-import-frame"
          title="Start an import"
          aria-hidden="true"
          tabIndex={-1}
          srcDoc={ADAPTED_DOCUMENT}
          sandbox="allow-scripts"
          loading="eager"
        />
      )}
      {webglAvailable !== false && <a className="glass-import-action" href="/app">Start an import <span aria-hidden="true">↗</span></a>}
      {webglAvailable === false && <a className="glass-import-fallback" href="/app">Start an import <span aria-hidden="true">↗</span></a>}
    </div>
  );
}
