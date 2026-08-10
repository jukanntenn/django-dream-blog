/**
 * Code Copy Module
 * Adds copy buttons to code blocks in prose content
 */

const COPIED_FEEDBACK_DURATION = 2000; // ms

/**
 * Create the copy button element
 */
function createCopyButton(): HTMLButtonElement {
  const button = document.createElement('button');
  button.className = 'code-copy-btn';
  button.setAttribute('type', 'button');
  button.setAttribute('aria-label', 'Copy code');

  button.innerHTML = `
    <svg class="code-copy-icon icon-copy" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
    </svg>
    <svg class="code-copy-icon icon-check code-copy-icon--hidden" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
  `;

  return button;
}

/**
 * Get code text from a code block
 */
function getCodeText(codeBlock: HTMLElement): string {
  // Try to find code element within pre or highlight block
  const codeElement = codeBlock.querySelector('code');

  if (codeElement) {
    return codeElement.textContent || '';
  }

  // Fallback to block's text content
  return codeBlock.textContent || '';
}

/**
 * Handle copy button click
 */
async function handleCopy(event: Event): Promise<void> {
  const button = event.currentTarget as HTMLButtonElement;
  const codeBlock = button.closest('pre, .highlight') as HTMLElement;

  if (!codeBlock) return;

  const codeText = getCodeText(codeBlock);

  if (!codeText) return;

  try {
    await navigator.clipboard.writeText(codeText);

    // Show copied state
    button.classList.add('code-copy-btn--copied');
    const iconCopy = button.querySelector('.icon-copy') as HTMLElement;
    const iconCheck = button.querySelector('.icon-check') as HTMLElement;

    if (iconCopy) iconCopy.classList.add('code-copy-icon--hidden');
    if (iconCheck) iconCheck.classList.remove('code-copy-icon--hidden');

    // Reset after delay
    setTimeout(() => {
      button.classList.remove('code-copy-btn--copied');
      if (iconCopy) iconCopy.classList.remove('code-copy-icon--hidden');
      if (iconCheck) iconCheck.classList.add('code-copy-icon--hidden');
    }, COPIED_FEEDBACK_DURATION);

  } catch (error) {
    // Clipboard not available or permission denied - silently fail
    console.warn('Copy to clipboard failed:', error);
  }
}

/**
 * Check if clipboard API is available
 */
function isClipboardAvailable(): boolean {
  return (
    typeof navigator !== 'undefined' &&
    navigator.clipboard &&
    typeof navigator.clipboard.writeText === 'function'
  );
}

/**
 * Add copy button to a code block
 */
function addCopyButton(codeBlock: HTMLElement): void {
  // Skip if already has button
  if (codeBlock.querySelector('.code-copy-btn')) return;

  // Make sure code block has relative positioning
  const computedStyle = window.getComputedStyle(codeBlock);
  if (computedStyle.position === 'static') {
    (codeBlock as any).style.position = 'relative';
  }

  const button = createCopyButton();
  button.addEventListener('click', handleCopy);
  codeBlock.appendChild(button);
}

/**
 * Process all code blocks in prose containers
 */
function processCodeBlocks(): void {
  const proseContainers = document.querySelectorAll('.prose');

  proseContainers.forEach((container) => {
    // Find all pre elements
    const preElements = container.querySelectorAll('pre');
    preElements.forEach((pre) => addCopyButton(pre as HTMLElement));

    // Find all highlight blocks (Pygments output)
    const highlightElements = container.querySelectorAll('.highlight');
    highlightElements.forEach((highlight) => addCopyButton(highlight as HTMLElement));
  });
}

/**
 * Set up MutationObserver for dynamic content
 */
function setupMutationObserver(): void {
  const observer = new MutationObserver((entries) => {
    let shouldProcess = false;

    entries.forEach((entry) => {
      entry.addedNodes.forEach((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          const element = node as Element;
          // Check if added node contains prose content
          if (
            element.classList?.contains('prose') ||
            element.querySelector?.('.prose')
          ) {
            shouldProcess = true;
          }
        }
      });
    });

    if (shouldProcess) {
      // Debounce slightly
      setTimeout(processCodeBlocks, 100);
    }
  });

  // Observe the entire body for changes
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
}

/**
 * Initialize the code copy functionality
 */
export function initCodeCopy(): void {
  if (!isClipboardAvailable()) {
    console.info('Clipboard API not available, code copy buttons disabled');
    return;
  }

  // Process existing code blocks
  processCodeBlocks();

  // Set up observer for dynamic content
  setupMutationObserver();
}
