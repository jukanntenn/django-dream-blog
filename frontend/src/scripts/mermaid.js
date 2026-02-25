function loadMermaid() {
  if (window.mermaid) return Promise.resolve();
  if (window.__mermaidLoadingPromise) return window.__mermaidLoadingPromise;
  window.__mermaidLoadingPromise = new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://unpkg.com/mermaid@9.4.0/dist/mermaid.min.js";
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load Mermaid"));
    document.head.appendChild(script);
  });
  return window.__mermaidLoadingPromise;
}

function init() {
  if (!document.querySelector(".mermaid")) return;

  loadMermaid()
    .then(() => {
      if (!window.mermaid) return;
      try {
        window.mermaid.init({
          startOnLoad: false,
          securityLevel: "loose",
        });
      } catch {}

      const nodes = Array.from(
        document.querySelectorAll(".mermaid:not([data-processed])"),
      );
      if (!nodes.length) return;
      try {
        window.mermaid.init(undefined, nodes);
      } catch {}
    })
    .catch(() => {});
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
