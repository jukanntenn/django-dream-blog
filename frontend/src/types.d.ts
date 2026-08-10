/**
 * Shared ambient types for lazily-loaded CDN libraries (KaTeX, Mermaid).
 */
interface Window {
  katex?: {
    render: (
      math: string,
      element: HTMLElement,
      options?: { throwOnError?: boolean; displayMode?: boolean },
    ) => void;
  };
  mermaid?: {
    init: (
      options?: { startOnLoad?: boolean; securityLevel?: string },
      nodes?: Element | Element[],
    ) => void;
  };
  __katexLoadingPromise?: Promise<void>;
  __mermaidLoadingPromise?: Promise<void>;
}
