# Directory Structure

> How frontend code is organized in this project.

---

## Overview

This project uses **Vite 5 + Tailwind CSS 4 + TypeScript** with `django-vite` for integration. The frontend is vanilla TypeScript/JavaScript (not React/Vue) with class-based components.

---

## Directory Layout

```
frontend/
├── src/                        # TypeScript/JavaScript source
│   ├── main.ts                # Entry point, imports all modules
│   ├── index.js               # Main initialization script
│   ├── index.css              # Global styles (Tailwind imports)
│   ├── friendly.css           # Third-party friendly styles
│   │
│   ├── comment.ts             # Comment system (class-based)
│   ├── toast.ts               # Toast notification component
│   ├── navbar-blur.ts         # Navbar blur effect on scroll
│   ├── backtop.ts             # Back to top button
│   ├── offcanvas.ts           # Offcanvas/drawer component
│   ├── scrollspy.ts           # Scroll spy for navigation
│   ├── theme-switcher.ts      # Dark/light theme toggle
│   ├── admin-theme-sync.ts    # Admin theme synchronization
│   │
│   ├── scripts/               # Feature-specific scripts
│   │   ├── katex.js          # KaTeX math rendering
│   │   └── admin-preview-render.ts
│   │
│   ├── styles/                # Additional stylesheets
│   │
│   ├── util/                  # Utility functions
│   │   └── backdrop.ts       # Backdrop/modal utility
│   │
│   └── vite-env.d.ts          # Vite type declarations
│
├── dist/                       # Build output (served as static files)
├── package.json               # Dependencies (pnpm)
├── tsconfig.json              # TypeScript configuration
├── vite.config.js             # Vite configuration
└── postcss.config.js          # PostCSS configuration (Tailwind)
```

---

## Module Organization

### Feature Modules

Each feature is a self-contained TypeScript module:

```typescript
// feature.ts
const NAME = "feature";

type Config = {
  // configuration options
};

const defaultConfig: Config = {
  // default values
};

class Feature {
  private config: Config;

  constructor(config: Partial<Config> = {}) {
    this.config = { ...defaultConfig, ...config };
  }

  static get NAME() {
    return NAME;
  }

  init(): void {
    // initialization logic
  }
}

export default Feature;
```

### Integration with Django Templates

Use `django-vite` to load modules:

```html
{% load vite %}
{% vite_asset "frontend/src/main.ts" %}
```

---

## Naming Conventions

### Files

- **TypeScript**: `kebab-case.ts` (e.g., `theme-switcher.ts`)
- **JavaScript**: `kebab-case.js` (e.g., `katex.js`)
- **CSS**: `kebab-case.css` (e.g., `index.css`)

### Classes

- **PascalCase** for class names (e.g., `Comment`, `Toast`)
- **Private properties** with underscore prefix or `private` keyword

### Constants

- **UPPER_SNAKE_CASE** for constants (e.g., `ERROR_MESSAGES`)
- **camelCase** for configuration objects (e.g., `defaultConfig`)

### CSS Classes

- **Tailwind utility classes** preferred
- **BEM-like naming** for custom classes: `component--modifier`

```css
/* Example from toast */
.toast { }
.toast--success { }
.toast--error { }
.toast--fade-out { }
```

---

## Examples

### Well-organized module: `comment.ts`

```typescript
// frontend/src/comment.ts
import Toast from "./toast";

const NAME = "comment";

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

const ERROR_MESSAGES: Record<string, string> = {
  network: "Network connection failed, please try again",
  server: "Server error, please try again later",
};

class Comment {
  private formElem: HTMLFormElement | null;
  private listElem: HTMLElement | null;
  private areaElem: HTMLElement | null;
  private config: Config;

  constructor(config: Partial<Config> = {}) {
    this.config = { ...defaultConfig, ...config };
    this.formElem = document.querySelector(this.config.formSelector);
    this.listElem = document.querySelector(this.config.listSelector);
    this.areaElem = document.querySelector(this.config.areaSelector);
  }

  static get NAME() {
    return NAME;
  }

  init(): void {
    if (this.formElem) {
      this.formElem.addEventListener("submit", this.handleSubmit.bind(this));
    }
    if (this.listElem) {
      this.listElem.addEventListener("click", this.handleListClick.bind(this));
    }
  }

  // ... other methods
}

export default Comment;
```

### Initialization pattern

```typescript
// frontend/src/main.ts
import "vite/modulepreload-polyfill";
import "./index.js";
import "./friendly.css";
import "./index.css";
import { initNavbarBlur } from './navbar-blur';

initNavbarBlur();
```
