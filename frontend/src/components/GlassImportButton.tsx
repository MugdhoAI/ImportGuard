import { useEffect, useRef, useState } from "react";
import glassSource from "../vendor/threeui/shaders/glass-ai-button/sources/glass-ai-button.html?raw";

const CLICK_HANDLER = "activate.addEventListener('click',()=>{if(handledDown){handledDown=false;return;}replay();});";
const IMPORT_HANDLER = "activate.addEventListener('click',()=>{if(handledDown)handledDown=false;document.querySelector('#status').textContent='Opening the import workspace';window.parent.postMessage({type:'importguard:start-import'},'*');});";
const SOURCE_ACTIVATE_LABEL = 'aria-label="GPT 6 Sol — activate the galaxy"';
const IMPORT_ACTIVATE_LABEL = 'aria-label="Start an import"';
const SOURCE_BRAND_DRAW = "lc.fillText('GPT 6 Sol',508,130);";
const IMPORT_BRAND_DRAW = "lc.fillText('',508,130);";
const SOURCE_RESIZE_CAMERA = "camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();camera.position.z=8.65*Math.max(1,1.77778/camera.aspect);camera.position.y=-camera.position.z*.155;camera.lookAt(0,-.12,0);";
const CTA_RESIZE_CAMERA = "camera.aspect=Math.min(innerWidth/innerHeight,2.2);camera.updateProjectionMatrix();camera.position.z=4.1*Math.max(1,1.77778/camera.aspect);camera.position.y=-camera.position.z*.155;camera.lookAt(0,-.12,0);";

export function makeImportGuardGlassDocument(source = glassSource) {
  const replacements: Array<[string, string]> = [
    ["<title>GPT 6 Sol — Glass Galaxy</title>", "<title>ImportGuard — Start an import</title>"],
    [SOURCE_ACTIVATE_LABEL, IMPORT_ACTIVATE_LABEL],
    [SOURCE_BRAND_DRAW, IMPORT_BRAND_DRAW],
    ["document.querySelector('#status').textContent='GPT 6 Sol — particle burst';", "document.querySelector('#status').textContent='Opening the import workspace';"],
    [CLICK_HANDLER, IMPORT_HANDLER],
    ["html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#a8b0bd}", "html,body{margin:0;width:100%;height:100%;overflow:hidden;background:transparent}"],
    ["#activate:focus-visible{outline:1.5px solid #fff;outline-offset:12px}", "#activate:focus-visible{outline:3px solid #fff;outline-offset:0}"],
    ["#controls{position:fixed;right:22px;bottom:20px;display:flex;gap:8px;opacity:0;transition:opacity .3s}", "#controls{display:none}"],
    ["alpha:false,powerPreference:'high-performance'", "alpha:true,powerPreference:'high-performance'"],
    ["scene.background=new THREE.Color('#a8b0bd')", "scene.background=null"],
    [SOURCE_RESIZE_CAMERA, CTA_RESIZE_CAMERA],
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

// The source canvas and its native hit target form one button. This adapter
// brands the rendered label and forwards that button's activation to /app.
export function GlassImportButton() {
  const frameRef = useRef<HTMLIFrameElement>(null);
  const [webglAvailable, setWebglAvailable] = useState<boolean | null>(null);

  useEffect(() => {
    const onMessage = (event: MessageEvent) => {
      if (event.source !== frameRef.current?.contentWindow) return;
      if (event.data?.type === "importguard:start-import") {
        window.location.assign("/app");
        return;
      }
      if (event.data?.type !== "importguard:glass-status" || typeof event.data.webgl !== "boolean") return;
      setWebglAvailable(event.data.webgl);
    };
    window.addEventListener("message", onMessage);
    return () => window.removeEventListener("message", onMessage);
  }, []);

  return (
    <div className={`glass-import-shell${webglAvailable === false ? " is-fallback" : ""}`}>
      {webglAvailable !== false && (
        <>
        <iframe
          ref={frameRef}
          className="glass-import-frame"
          title="ImportGuard import action"
          srcDoc={ADAPTED_DOCUMENT}
          sandbox="allow-scripts"
          loading="eager"
        />
        <span className="glass-import-label" aria-hidden="true"><span className="glass-import-mark">IG</span><span>Start an import</span></span>
        </>
      )}
      {webglAvailable === false && <a className="glass-import-fallback" href="/app"><span className="glass-import-mark" aria-hidden="true">IG</span><span>Start an import</span></a>}
    </div>
  );
}
