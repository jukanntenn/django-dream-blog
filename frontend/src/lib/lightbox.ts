/**
 * Image Lightbox Module
 * Provides click-to-enlarge functionality for images in prose content
 */

let overlay: HTMLElement | null = null;
let overlayImage: HTMLImageElement | null = null;
let closeButton: HTMLButtonElement | null = null;
let originalScrollPosition = 0;

/**
 * Create the lightbox overlay DOM structure
 */
function createOverlay(): HTMLElement {
  const overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Image viewer');

  // Close button
  const closeBtn = document.createElement('button');
  closeBtn.className = 'lightbox-close';
  closeBtn.setAttribute('aria-label', 'Close');
  closeBtn.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  `;

  // Image element
  const img = document.createElement('img');
  img.className = 'lightbox-image';
  img.alt = '';

  overlay.appendChild(closeBtn);
  overlay.appendChild(img);

  return overlay;
}

/**
 * Open lightbox with the specified image source
 */
function openLightbox(src: string, alt: string): void {
  if (!overlay || !overlayImage) return;

  // Save scroll position
  originalScrollPosition = window.pageYOffset;

  // Set image source
  overlayImage.src = src;
  overlayImage.alt = alt || 'Enlarged image';

  // Show overlay
  overlay?.classList.add('lightbox-overlay--open');
  document.body.classList.add('lightbox-open');

  // Focus close button for accessibility
  closeButton?.focus();
}

/**
 * Close the lightbox
 */
function closeLightbox(): void {
  if (!overlay) return;

  overlay.classList.remove('lightbox-overlay--open');
  document.body.classList.remove('lightbox-open');

  // Restore scroll position
  window.scrollTo(0, originalScrollPosition);

  // Clear image source after transition
  setTimeout(() => {
    if (overlayImage) {
      overlayImage.src = '';
      overlayImage.alt = '';
    }
  }, 200);
}

/**
 * Handle image click event
 */
function handleImageClick(event: Event): void {
  const target = event.target as HTMLElement;
  const img = target.closest('img') as HTMLImageElement;

  if (!img || !img.src) return;

  // Only handle images inside prose content
  const proseContainer = img.closest('.prose');
  if (!proseContainer) return;

  event.preventDefault();
  openLightbox(img.src, img.alt);
}

/**
 * Handle keyboard events
 */
function handleKeyDown(event: KeyboardEvent): void {
  if (event.key === 'Escape') {
    closeLightbox();
  }
}

/**
 * Handle overlay click (close when clicking outside image)
 */
function handleOverlayClick(event: Event): void {
  if (event.target === overlay) {
    closeLightbox();
  }
}

/**
 * Initialize the lightbox functionality
 */
export function initLightbox(): void {
  // Create overlay on first call
  if (!overlay) {
    overlay = createOverlay();
    overlayImage = overlay.querySelector('.lightbox-image') as HTMLImageElement;
    closeButton = overlay.querySelector('.lightbox-close') as HTMLButtonElement;

    // Append to body
    document.body.appendChild(overlay);

    // Event listeners for overlay
    closeButton?.addEventListener('click', closeLightbox);
    overlay.addEventListener('click', handleOverlayClick);
    document.addEventListener('keydown', handleKeyDown);
  }

  // Use event delegation for image clicks
  document.addEventListener('click', handleImageClick);
}
