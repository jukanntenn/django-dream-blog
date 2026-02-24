# Component Guidelines

> How components are built in this project.

---

## Overview

This project uses **vanilla TypeScript classes** for UI components (not React/Vue). Each component is a self-contained module with:
- Private state management
- DOM element references
- Event handling
- Public API via methods

---

## Component Structure

### Standard Pattern

```typescript
// 1. Constants and types at the top
const NAME = "component";

type Config = {
  selector: string;
  option?: boolean;
};

const defaultConfig: Config = {
  selector: ".component",
  option: true,
};

// 2. Main class
class Component {
  // 2a. Private properties
  private elem: HTMLElement | null;
  private config: Config;

  // 2b. Constructor with config
  constructor(config: Partial<Config> = {}) {
    this.config = { ...defaultConfig, ...config };
    this.elem = document.querySelector(this.config.selector);
  }

  // 2c. Static NAME getter
  static get NAME() {
    return NAME;
  }

  // 2d. Public init method
  init(): void {
    if (!this.elem) return;
    this.bindEvents();
  }

  // 2e. Private methods
  private bindEvents(): void {
    this.elem?.addEventListener("click", this.handleClick.bind(this));
  }

  private handleClick(event: Event): void {
    // Handle click
  }

  // 2f. Public API methods
  show(): void {
    this.elem?.classList.remove("hidden");
  }

  hide(): void {
    this.elem?.classList.add("hidden");
  }

  // 2g. Cleanup method
  dispose(): void {
    // Remove event listeners, clear timers, etc.
  }
}

// 3. Default export
export default Component;
```

---

## Props/Config Conventions

### Configuration Pattern

Components accept a `Partial<Config>` object in the constructor:

```typescript
type Config = {
  formSelector: string;
  listSelector: string;
  areaSelector: string;
};

const defaultConfig: Config = {
  formSelector: ".comment-form",
  listSelector: "#comment-list",
  areaSelector: "#comment-area",
};

class Comment {
  constructor(config: Partial<Config> = {}) {
    this.config = { ...defaultConfig, ...config };
  }
}
```

### Usage

```typescript
// With default config
const comment = new Comment();
comment.init();

// With custom config
const comment = new Comment({
  formSelector: "#custom-form",
});
comment.init();
```

---

## Styling Patterns

### Tailwind CSS (Preferred)

Use Tailwind utility classes directly in templates:

```html
<div class="flex items-center gap-4 p-4 bg-white dark:bg-gray-800">
  <button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded hover:bg-blue-700">
    Submit
  </button>
</div>
```

### Custom CSS Classes

For complex components, use BEM-like naming:

```css
/* Component base */
.toast {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
}

/* Modifier variants */
.toast--success {
  background-color: #10b981;
  color: white;
}

.toast--error {
  background-color: #ef4444;
  color: white;
}

/* State classes */
.toast--fade-out {
  opacity: 0;
  transition: opacity 0.2s ease-out;
}
```

### Dark Mode

Use Tailwind's `dark:` prefix:

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Content
</div>
```

---

## Event Handling

### Bind Events in init()

```typescript
class Component {
  private elem: HTMLElement | null;

  init(): void {
    if (this.elem) {
      this.elem.addEventListener("click", this.handleClick.bind(this));
    }
  }

  private handleClick(event: Event): void {
    event.preventDefault();
    // Handle click
  }
}
```

### Event Delegation for Dynamic Content

```typescript
private handleListClick(event: Event): void {
  const target = event.target as HTMLElement;

  // Handle specific buttons using closest()
  const replyBtn = target.closest<HTMLElement>(".reply");
  if (replyBtn) {
    event.preventDefault();
    this.handleReply(replyBtn);
    return;
  }

  const foldBtn = target.closest<HTMLElement>(".fold");
  if (foldBtn) {
    event.preventDefault();
    this.handleFold(foldBtn);
  }
}
```

---

## Accessibility

### Interactive Elements

- Use semantic HTML (`<button>`, `<a>`, etc.)
- Add `aria-*` attributes for state
- Ensure keyboard navigation

### Focus Management

```typescript
private showModal(modal: HTMLElement): void {
  modal.classList.remove("hidden");
  // Focus first focusable element
  const focusable = modal.querySelector<HTMLElement>("button, [href], input, select, textarea");
  focusable?.focus();
}
```

---

## Common Mistakes

### Not Checking for Null Elements

```typescript
// BAD - may throw error
constructor() {
  this.elem.textContent = "Hello";
}

// GOOD - null check
constructor() {
  this.elem?.classList.add("active");
}
```

### Not Binding Event Handlers

```typescript
// BAD - `this` is undefined in handler
this.elem.addEventListener("click", this.handleClick);

// GOOD - bind `this`
this.elem.addEventListener("click", this.handleClick.bind(this));
```

### Not Cleaning Up

```typescript
// BAD - no cleanup
class Component {
  private timer: number;

  init(): void {
    this.timer = setInterval(() => {}, 1000);
  }
}

// GOOD - dispose method
class Component {
  private timer: number | null = null;

  init(): void {
    this.timer = setInterval(() => {}, 1000);
  }

  dispose(): void {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }
}
```

---

## Examples

### Toast Component

```typescript
// frontend/src/toast.ts
const NAME = "toast";

type ToastType = "success" | "error" | "info";

type Config = {
  type?: ToastType;
  duration?: number;
};

const defaultConfig: Config = {
  type: "info",
  duration: 3000,
};

class Toast {
  private elem: HTMLElement | null = null;
  private config: Config;
  private timer: number | null = null;

  constructor(message: string, config?: Config) {
    this.config = { ...defaultConfig, ...config };
    this.show(message);
  }

  static get NAME() {
    return NAME;
  }

  show(message: string): void {
    this.elem = this.createElement(message);
    document.body.appendChild(this.elem);

    this.timer = window.setTimeout(() => {
      this.hide();
    }, this.config.duration);
  }

  hide(): void {
    if (this.elem) {
      this.elem.classList.add("toast--fade-out");
      setTimeout(() => {
        this.dispose();
      }, 200);
    }
  }

  dispose(): void {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    if (this.elem && this.elem.parentNode) {
      this.elem.parentNode.removeChild(this.elem);
      this.elem = null;
    }
  }

  private createElement(message: string): HTMLElement {
    const toast = document.createElement("div");
    toast.className = `toast toast--${this.config.type}`;
    toast.textContent = message;
    return toast;
  }
}

export default Toast;
```
