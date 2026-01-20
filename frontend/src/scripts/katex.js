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
    // Render KaTeX math if library is available
    if (typeof katex !== "undefined") {
      katexMath();
    }
  });
}

// Auto-initialize when module is imported
init();

export { katexMath, onReady, init };
