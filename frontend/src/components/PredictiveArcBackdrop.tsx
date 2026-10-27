import { useEffect, useRef } from "react";
import {
  createPredictiveArcRenderer,
  PREDICTIVE_ARC_DEFAULTS,
} from "../vendor/threeui/shaders/predictive-arc/predictiveArcRenderer";

const OPTIONS = {
  ...PREDICTIVE_ARC_DEFAULTS,
  mode: "dark" as const,
  speed: 1,
  hue: 0,
  saturation: 1,
  brightness: 1,
};

export function PredictiveArcBackdrop() {
  const hostRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const host = hostRef.current;
    const canvas = canvasRef.current;
    if (!host || !canvas) return;

    const renderer = createPredictiveArcRenderer(canvas, () => OPTIONS);
    if (!renderer) return;

    let visible = true;
    let frame = 0;
    const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const draw = () => renderer.render();
    const stop = () => {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
    };
    const tick = () => {
      draw();
      frame = visible && !document.hidden && !motion.matches ? requestAnimationFrame(tick) : 0;
    };
    const start = () => {
      if (visible && !document.hidden && !motion.matches && !frame) frame = requestAnimationFrame(tick);
    };
    const resize = () => {
      const bounds = host.getBoundingClientRect();
      renderer.resize(bounds.width, bounds.height);
      draw();
      start();
    };
    const resizeObserver = new ResizeObserver(resize);
    const intersectionObserver = new IntersectionObserver(([entry]) => {
      visible = entry?.isIntersecting ?? true;
      if (visible) start();
      else stop();
    });
    const onVisibility = () => {
      if (document.hidden) stop();
      else start();
    };
    const onMotion = () => {
      if (motion.matches) {
        stop();
        draw();
      } else start();
    };

    resizeObserver.observe(host);
    intersectionObserver.observe(host);
    document.addEventListener("visibilitychange", onVisibility);
    motion.addEventListener("change", onMotion);
    resize();

    return () => {
      stop();
      resizeObserver.disconnect();
      intersectionObserver.disconnect();
      document.removeEventListener("visibilitychange", onVisibility);
      motion.removeEventListener("change", onMotion);
    };
  }, []);

  return (
    <div className="arc-backdrop" ref={hostRef} aria-hidden="true">
      <canvas ref={canvasRef} />
    </div>
  );
}
