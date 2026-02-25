/**
 * Renders KaTeX math expressions in the document.
 * Processes elements with class "arithmatex" and renders them using KaTeX.
 */
function katexMath() {
  const maths = document.querySelectorAll(".arithmatex");

  maths.forEach((mathElem) => {
    const tex = mathElem.textContent || mathElem.innerText || "";

    if (tex.startsWith("\\(") && tex.endsWith("\\)")) {
      // Inline math: \( ... \)
      if (typeof katex !== "undefined") {
        katex.render(tex.slice(2, -2), mathElem, { displayMode: false });
      }
    } else if (tex.startsWith("\\[") && tex.endsWith("\\]")) {
      // Display math: \[ ... \]
      if (typeof katex !== "undefined") {
        katex.render(tex.slice(2, -2), mathElem, { displayMode: true });
      }
    }
  });
}

function loadKatex() {
  if (typeof katex !== "undefined") return Promise.resolve();
  if (window.__katexLoadingPromise) return window.__katexLoadingPromise;
  window.__katexLoadingPromise = new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.8/katex.min.js";
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load KaTeX"));
    document.head.appendChild(script);
  });
  return window.__katexLoadingPromise;
}

/**
 * Registers a callback to run when the DOM is ready.
 * Handles both modern browsers and legacy IE support.
 */
function onReady(fn) {
  if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", fn);
  } else {
    // Legacy IE support
    document.addEventListener("onreadystatechange", function () {
      if (document.readyState === "interactive") {
        fn();
      }
    });
  }
}

/**
 * Initialize KaTeX rendering when DOM is ready.
 */
function init() {
  onReady(function () {
    if (!document.querySelector(".arithmatex")) return;
    loadKatex()
      .then(() => {
        if (typeof katex !== "undefined") katexMath();
      })
      .catch(() => {});
  });
}

// Auto-initialize when module is imported
init();

export { katexMath, onReady, init };
