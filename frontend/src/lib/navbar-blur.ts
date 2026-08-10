/**
 * Navbar blur effect on scroll
 * Adds backdrop-blur when user scrolls past a threshold
 */

const SCROLL_THRESHOLD = 10; // pixels
const BLUR_CLASS = 'backdrop-blur-md';

export function initNavbarBlur(): void {
  const navbar = document.querySelector('[data-blur-nav]');
  if (!navbar) return;

  const updateBlur = () => {
    if (window.scrollY > SCROLL_THRESHOLD) {
      navbar.classList.add(BLUR_CLASS);
    } else {
      navbar.classList.remove(BLUR_CLASS);
    }
  };

  // Initial check for pages loaded while scrolled
  updateBlur();

  // Listen for scroll events
  window.addEventListener('scroll', updateBlur, { passive: true });
}
