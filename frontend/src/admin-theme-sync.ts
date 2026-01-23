/**
 * Synchronizes Django admin's data-theme attribute with frontend's .dark/.light classes
 * Ensures Tailwind dark: variants work in admin markdown preview
 */
(function () {
  'use strict';

  function syncTailwindClass(): void {
    const html = document.documentElement;
    const adminTheme = html.dataset.theme || 'auto';

    html.classList.remove('dark', 'light');

    if (adminTheme === 'dark') {
      html.classList.add('dark');
    } else if (adminTheme === 'light') {
      html.classList.add('light');
    } else if (adminTheme === 'auto') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      html.classList.add(prefersDark ? 'dark' : 'light');
    }
  }

  function setupSystemThemeListener(): void {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', () => {
        if (document.documentElement.dataset.theme === 'auto') {
          syncTailwindClass();
        }
      });
    } else if (mediaQuery.addListener) {
      // Legacy browser support
      mediaQuery.addListener(() => {
        if (document.documentElement.dataset.theme === 'auto') {
          syncTailwindClass();
        }
      });
    }
  }

  function setupThemeObserver(): void {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' &&
            mutation.attributeName === 'data-theme') {
          syncTailwindClass();
        }
      });
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme']
    });
  }

  function init(): void {
    // Set up observer first to catch any future changes
    setupThemeObserver();
    setupSystemThemeListener();

    // Sync immediately to apply current theme
    syncTailwindClass();

    // Re-sync on window load to ensure we run after Django's theme.js
    window.addEventListener('load', () => {
      syncTailwindClass();
    });
  }

  // Run immediately, don't wait for DOMContentLoaded
  // We need to catch data-theme changes as early as possible
  init();
})();
