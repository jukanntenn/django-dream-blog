# UX Features Design: Image Lightbox & Code Copy

**Date:** 2026-02-28
**Author:** Design Discussion
**Status:** Approved

## Overview

Implement two user experience enhancements for blog content using vanilla JavaScript:

1. **Image Lightbox** - Click images to view in a modal overlay
2. **Code Block Copy Button** - One-click copy for code blocks

## Requirements

### Image Lightbox
- Click any image in `.prose` content to open in modal
- Modal should be centered with semi-transparent backdrop
- Close via: Close button, clicking outside image, or ESC key
- Prevent body scroll when modal is open
- Support for dynamically loaded content

### Code Copy Button
- Add copy button to all `<pre>` and `.highlight` code blocks
- Copy code text to clipboard on click
- Visual feedback (icon change) for 2 seconds after copy
- Hide button if Clipboard API unavailable
- Support for dynamically loaded content

### Scope
- Apply to all prose content (posts, tutorials, columns)
- Use vanilla JavaScript (no external libraries)

## Architecture

### New Files
```
frontend/src/
  ├── lightbox.ts          # Image lightbox functionality
  └── code-copy.ts         # Code block copy functionality
```

### Integration Points
- `frontend/src/main.ts` - Import and initialize both modules
- `frontend/src/styles/components.css` - Add new component styles

## Component Details

### Lightbox Module (`lightbox.ts`)

**Exports:**
```typescript
export function initLightbox(): void;
```

**Behavior:**
1. Delegates click events on `.prose img` elements
2. Creates modal DOM dynamically on first click
3. Reuses single modal instance for all images
4. Handles a11y: traps focus, ESC key, aria-labels

**Modal Structure:**
```html
<div class="lightbox-overlay" role="dialog" aria-modal="true" aria-label="Image viewer">
  <button class="lightbox-close" aria-label="Close">
    <svg><!-- close icon --></svg>
  </button>
  <img class="lightbox-image" src="..." alt="...">
</div>
```

### Code Copy Module (`code-copy.ts`)

**Exports:**
```typescript
export function initCodeCopy(): void;
```

**Behavior:**
1. Queries all `.prose pre` and `.prose .highlight` elements
2. Injects copy button into each block
3. Extracts text content from code element
4. Uses `navigator.clipboard.writeText()`
5. Falls back silently if API unavailable

**Button Structure:**
```html
<button class="code-copy-btn" aria-label="Copy code">
  <svg class="icon-copy"><!-- copy icon --></svg>
  <svg class="icon-check hidden"><!-- check icon --></svg>
</button>
```

## Styles

### Lightbox Styles (`components.css`)
```css
/* Overlay */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(4px);
}

/* Image */
.lightbox-image {
  max-width: 95vw;
  max-height: 95vh;
  object-fit: contain;
}

/* Close button */
.lightbox-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  /* ... */
}
```

### Code Copy Styles (`components.css`)
```css
.code-copy-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  /* ... */
}

.code-copy-btn.copied .icon-copy {
  display: none;
}

.code-copy-btn.copied .icon-check {
  display: inline-block;
}
```

## Accessibility

- Keyboard navigation: Tab, Shift+Tab, Enter, ESC
- ARIA labels and roles
- Focus management when modal opens/closes
- `aria-pressed` for copy button state

## Browser Support

- Clipboard API: Chrome 66+, Firefox 63+, Safari 13.1+
- Graceful degradation for older browsers

## Testing Checklist

- [ ] Image click opens modal
- [ ] Modal closes via button, outside click, ESC
- [ ] Copy button appears on all code blocks
- [ ] Copy feedback shows for ~2 seconds
- [ ] Works with dynamically loaded content
- [ ] Keyboard accessibility (Tab, ESC)
- [ ] Dark/light theme compatibility
- [ ] Special characters in code copy correctly
