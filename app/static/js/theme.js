(() => {
  const root = document.documentElement;
  const update = () => {
    const light = root.dataset.theme === "light";
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.textContent = `Switch to ${light ? "dark" : "light"} theme`;
      button.setAttribute("aria-label", `Switch to ${light ? "dark" : "light"} theme`);
      button.setAttribute("aria-pressed", String(light));
    });
  };
  document.addEventListener("click", (event) => {
    if (!event.target.closest("[data-theme-toggle]")) return;
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    try { localStorage.setItem("importguard-theme", next); } catch { /* storage may be disabled */ }
    update();
  });
  update();
})();
