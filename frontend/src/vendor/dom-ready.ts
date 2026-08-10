/**
 * Registers a callback to run when the DOM is ready.
 */
export function onReady(fn: () => void): void {
  document.addEventListener("DOMContentLoaded", fn);
}
