import "vite/modulepreload-polyfill";
import "./index.js";
import "./friendly.css";
import "./index.css";
import "./search";
import { initNavbarBlur } from './navbar-blur';

initNavbarBlur();

// Mobile menu dropdown
function initMobileMenu(): void {
  const trigger = document.getElementById('mobile-menu-trigger');
  const menu = document.getElementById('mobile-menu');

  if (!trigger || !menu) return;

  trigger.addEventListener('click', () => {
    const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
    trigger.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
    menu.setAttribute('aria-hidden', isExpanded ? 'true' : 'false');
    menu.classList.toggle('hidden');
  });

  // Close menu when clicking outside
  document.addEventListener('click', (event) => {
    const isClickInside = trigger?.contains(event.target as Node) || menu?.contains(event.target as Node);
    if (!isClickInside && !menu.classList.contains('hidden')) {
      trigger.setAttribute('aria-expanded', 'false');
      menu.setAttribute('aria-hidden', 'true');
      menu.classList.add('hidden');
    }
  });

  // Close menu on escape key
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !menu.classList.contains('hidden')) {
      trigger.setAttribute('aria-expanded', 'false');
      menu.setAttribute('aria-hidden', 'true');
      menu.classList.add('hidden');
      trigger.focus();
    }
  });
}

initMobileMenu();
