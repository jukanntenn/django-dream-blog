/**
 * Renders KaTeX math expressions in the document.
 * Processes elements with class "arithmatex" and renders them using KaTeX
 * (loaded lazily from CDN on first use).
 */
import { onReady } from "./dom-ready";

function katexMath(): void {
  const maths = document.querySelectorAll<HTMLElement>(".arithmatex");

  maths.forEach((mathElem) => {
    const tex = mathElem.textContent || "";

    if (tex.startsWith("\\(") && tex.endsWith("\\)")) {
      window.katex?.render(tex.slice(2, -2), mathElem, { displayMode: false });
    } else if (tex.startsWith("\\[") && tex.endsWith("\\]")) {
      window.katex?.render(tex.slice(2, -2), mathElem, { displayMode: true });
    }
  });
}

function loadKatex(): Promise<void> {
  if (window.katex) return Promise.resolve();
  if (window.__katexLoadingPromise) return window.__katexLoadingPromise;
  window.__katexLoadingPromise = new Promise<void>((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.8/katex.min.js";
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load KaTeX"));
    document.head.appendChild(script);
  });
  return window.__katexLoadingPromise;
}

onReady(() => {
  if (!document.querySelector(".arithmatex")) return;
  loadKatex()
    .then(() => katexMath())
    .catch(() => {});
});
