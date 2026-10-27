import { useEffect, useRef } from "react";
import { AnimatedTopDock } from "../vendor/threeui/shaders/animated-top-dock/AnimatedTopDock";

const DOCK_LINKS = [
  { label: "How", href: "#how" },
  { label: "Workflow", href: "#workflow" },
  { label: "Import", href: "/app" },
  { label: "Privacy", href: "/privacy" },
  { label: "Guide", href: "#guide" },
] as const;

function goTo(href: string) {
  if (!href.startsWith("#")) {
    window.location.assign(href);
    return;
  }
  const target = document.querySelector(href);
  if (!target) return;
  window.history.pushState(null, "", href);
  target.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
}

export function ImportGuardDock() {
  const hostRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const host = hostRef.current;
    const nav = host?.querySelector("nav");
    if (!host || !nav) return;
    nav.setAttribute("aria-label", "ImportGuard navigation");
    const buttons = [...nav.querySelectorAll<HTMLButtonElement>("button[data-dock-item]")];
    if (buttons.length !== DOCK_LINKS.length + 1) throw new Error("Unexpected Sable dock item count; update its ImportGuard navigation adapter.");

    const [home, ...links] = buttons;
    home.setAttribute("aria-label", "Home");
    home.dataset.importguardHref = "#top";
    links.forEach((button, index) => {
      const label = button.querySelector<HTMLElement>("span:last-child");
      const link = DOCK_LINKS[index];
      if (!label) throw new Error("Sable dock item label is missing; update its ImportGuard adapter.");
      button.setAttribute("aria-label", link.label);
      button.dataset.importguardHref = link.href;
      label.textContent = link.label;
    });

    const navigate = (event: MouseEvent) => {
      const button = (event.target as Element | null)?.closest<HTMLButtonElement>("button[data-importguard-href]");
      const href = button?.dataset.importguardHref;
      if (href) goTo(href);
    };
    nav.addEventListener("click", navigate, true);
    return () => nav.removeEventListener("click", navigate, true);
  }, []);

  return (
    <>
      <div className="dock-mount" ref={hostRef}>
        <AnimatedTopDock variant="sable" proximity={122} spring={0.19} damping={0.7} widthGrowth={17} heightGrowth={16} drop={3.5} />
      </div>
    </>
  );
}
