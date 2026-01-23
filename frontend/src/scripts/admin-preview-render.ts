/**
 * Dynamic rendering for KaTeX math and Mermaid diagrams in admin markdown preview
 *
 * Uses MutationObserver to detect when preview content changes and renders
 * KaTeX math expressions and Mermaid diagrams on-the-fly.
 */

export {};

declare global {
  interface Window {
    katex?: {
      render: (
        math: string,
        element: HTMLElement,
        options?: { throwOnError?: boolean; displayMode?: boolean }
      ) => void;
    };
    mermaid?: {
      init: (
        options?: { startOnLoad?: boolean; securityLevel?: string },
        nodes?: Element | Element[]
      ) => void;
      run?: never; // Not available in Mermaid 9.x
    };
  }
}

interface RenderState {
  katexLoaded: boolean;
  katexCssLoaded: boolean;
  mermaidLoaded: boolean;
  mermaidInitialized: boolean;
}

const state: RenderState = {
  katexLoaded: false,
  katexCssLoaded: false,
  mermaidLoaded: false,
  mermaidInitialized: false,
};

/**
 * Load KaTeX library from CDN
 */
function loadKaTeX(): Promise<void> {
  if (state.katexLoaded && state.katexCssLoaded) {
    return Promise.resolve();
  }

  const cssPromise = state.katexCssLoaded
    ? Promise.resolve()
    : new Promise<void>((resolve, reject) => {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.8/katex.min.css';
        link.onload = () => {
          state.katexCssLoaded = true;
          resolve();
        };
        link.onerror = () => reject(new Error('Failed to load KaTeX CSS'));
        document.head.appendChild(link);
      });

  const jsPromise = state.katexLoaded
    ? Promise.resolve()
    : new Promise<void>((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'https://cdn.bootcdn.net/ajax/libs/KaTeX/0.16.8/katex.min.js';
        script.onload = () => {
          state.katexLoaded = true;
          resolve();
        };
        script.onerror = () => reject(new Error('Failed to load KaTeX JS'));
        document.head.appendChild(script);
      });

  return Promise.all([cssPromise, jsPromise]).then(() => {});
}

/**
 * Load Mermaid library from CDN
 */
function loadMermaid(): Promise<void> {
  if (state.mermaidLoaded) {
    return Promise.resolve();
  }

  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/mermaid@9.4.0/dist/mermaid.min.js';
    script.onload = () => {
      state.mermaidLoaded = true;
      resolve();
    };
    script.onerror = () => reject(new Error('Failed to load Mermaid'));
    document.head.appendChild(script);
  });
}

/**
 * Initialize Mermaid with safe configuration
 */
function initMermaid(): void {
  if (!state.mermaidLoaded || state.mermaidInitialized || !window.mermaid) {
    return;
  }

  try {
    window.mermaid.init({
      startOnLoad: false,
      securityLevel: 'loose',
    });
    state.mermaidInitialized = true;
  } catch (error) {
    console.error('Failed to initialize Mermaid:', error);
  }
}

/**
 * Render KaTeX math expressions in a container
 */
function renderKaTeX(container: HTMLElement): void {
  if (!state.katexLoaded || !window.katex) {
    return;
  }

  // Find all .arithmatex elements
  const mathElements = container.querySelectorAll('.arithmatex');
  mathElements.forEach((element) => {
    // Skip already rendered elements (check for katex class)
    if (element.classList.contains('katex') || element.querySelector('.katex')) {
      return;
    }

    const tex = (element as HTMLElement).textContent || (element as HTMLElement).innerText || '';

    // Check for inline math: \( ... \)
    if (tex.startsWith('\\(') && tex.endsWith('\\)')) {
      try {
        window.katex!.render(tex.slice(2, -2), element as HTMLElement, {
          throwOnError: false,
          displayMode: false,
        });
      } catch (error) {
        console.error('KaTeX render error:', error);
      }
    }
    // Check for display math: \[ ... \]
    else if (tex.startsWith('\\[') && tex.endsWith('\\]')) {
      try {
        window.katex!.render(tex.slice(2, -2), element as HTMLElement, {
          throwOnError: false,
          displayMode: true,
        });
      } catch (error) {
        console.error('KaTeX render error:', error);
      }
    }
  });
}

/**
 * Render Mermaid diagrams in a container
 */
function renderMermaid(container: HTMLElement): void {
  if (!state.mermaidLoaded) {
    return;
  }

  // Initialize Mermaid if not already done
  initMermaid();

  // Find all .mermaid elements that haven't been processed yet
  const mermaidElements = container.querySelectorAll<HTMLElement>('.mermaid:not([data-processed])');
  if (mermaidElements.length === 0) {
    return;
  }

  try {
    // Mermaid 9.4 API: init(options, nodes)
    window.mermaid!.init(undefined, Array.from(mermaidElements));
  } catch (error) {
    console.error('Mermaid render error:', error);
  }
}

/**
 * Render all math and diagrams in a preview container
 */
function renderPreviewContent(previewEl: HTMLElement): void {
  try {
    // Render KaTeX (synchronous, fast)
    renderKaTeX(previewEl);

    // Render Mermaid (synchronous in Mermaid 9.x)
    renderMermaid(previewEl);
  } catch (error) {
    console.error('Preview rendering error:', error);
  }
}

/**
 * Debounce function to limit rendering frequency
 */
function debounce<T extends (...args: any[]) => any>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  return function (this: any, ...args: Parameters<T>) {
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}

/**
 * Set up MutationObserver to detect preview content changes
 */
function setupPreviewObserver(): void {
  // Find all preview elements with data-md-preview attribute
  const previewElements = document.querySelectorAll('[data-md-preview]');

  if (previewElements.length === 0) {
    console.debug('No preview elements found with [data-md-preview]');
    return;
  }

  // Debounced render function
  const debouncedRender = debounce(async (previewEl: HTMLElement) => {
    // Only load libraries when actually needed
    const hasMath = previewEl.querySelector('.arithmatex') !== null;
    const hasMermaid = previewEl.querySelector('.mermaid') !== null;

    if (!hasMath && !hasMermaid) {
      return;
    }

    try {
      if (hasMath) {
        await loadKaTeX();
      }
      if (hasMermaid) {
        await loadMermaid();
      }

      renderPreviewContent(previewEl);
    } catch (error) {
      console.error('Failed to render preview content:', error);
    }
  }, 100);

  // Set up observer for each preview element
  previewElements.forEach((previewEl) => {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList' || mutation.type === 'characterData') {
          debouncedRender(previewEl as HTMLElement);
          return;
        }
      });
    });

    observer.observe(previewEl, {
      childList: true,
      subtree: true,
      characterData: true,
    });

    // Initial render for existing content
    debouncedRender(previewEl as HTMLElement);
  });
}

/**
 * Initialize the admin preview rendering system
 */
function init(): void {
  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupPreviewObserver);
  } else {
    // DOM is already ready, set up immediately
    setupPreviewObserver();
  }

  // Also try again after a short delay in case markdown_field loads later
  setTimeout(setupPreviewObserver, 500);
}

// Run initialization
init();
