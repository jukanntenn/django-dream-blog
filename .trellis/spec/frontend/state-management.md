# State Management

> How state is managed in this project.

---

## Overview

This project uses **vanilla TypeScript** with **class-based state management**. There is no Redux, Zustand, or similar library. State is managed within component classes using private properties.

---

## State Categories

### Component State (Private Properties)

State is stored as private class properties:

```typescript
class Comment {
  // Component state
  private formElem: HTMLFormElement | null;
  private listElem: HTMLElement | null;
  private config: Config;

  constructor(config: Partial<Config> = {}) {
    this.config = { ...defaultConfig, ...config };
    this.formElem = document.querySelector(this.config.formSelector);
    this.listElem = document.querySelector(this.config.listSelector);
  }
}
```

### UI State

For UI state like loading, visibility:

```typescript
class Comment {
  private setButtonLoading(btn: HTMLButtonElement, loading: boolean): void {
    btn.disabled = loading;
    if (loading) {
      btn.dataset.originalText = btn.textContent || "";
      btn.textContent = "Submitting...";
    } else {
      btn.textContent = btn.dataset.originalText || "Submit";
    }
  }
}
```

### DOM State

Use data attributes for state stored in DOM:

```typescript
// Store state in data attribute
btn.dataset.originalText = btn.textContent || "";

// Read state from data attribute
const originalText = btn.dataset.originalText || "Submit";
```

---

## State Patterns

### Single Source of Truth

Keep state in one place:

```typescript
// BAD - duplicated state
class Component {
  private isLoading = false;
  private button: HTMLButtonElement;

  private submit() {
    this.isLoading = true;
    this.button.disabled = true;  // Duplicated!
  }
}

// GOOD - derive from single source
class Component {
  private button: HTMLButtonElement;

  private setLoading(loading: boolean) {
    this.button.disabled = loading;  // Single source
    this.button.textContent = loading ? "Loading..." : "Submit";
  }

  private isLoading(): boolean {
    return this.button.disabled;
  }
}
```

### Immutable Updates

Create new objects/arrays instead of mutating:

```typescript
// BAD - mutation
this.config.selector = newSelector;

// GOOD - create new object
this.config = { ...this.config, selector: newSelector };
```

---

## Server State

### Fetch and Cache Pattern

```typescript
class Comment {
  private fetchForm(url: string): Promise<string> {
    return fetch(url, { method: "GET" })
      .then((response) => {
        if (!response.ok) {
          throw new Error(ERROR_MESSAGES.server);
        }
        return response.text();
      });
  }
}
```

### No Client-Side Caching

This project does not implement client-side caching. Each request goes to the server. HTMX-style HTML responses are used for dynamic content.

---

## State Synchronization

### DOM → State

Read from DOM when needed:

```typescript
private getTargetFields(formElem: HTMLElement): Record<string, string> {
  const contentType = formElem.querySelector<HTMLInputElement>("input[name='content_type']")?.value || "";
  const objectPk = formElem.querySelector<HTMLInputElement>("input[name='object_pk']")?.value || "";
  return { content_type: contentType, object_pk: objectPk };
}
```

### State → DOM

Update DOM when state changes:

```typescript
private insertComment(html: string): void {
  if (!this.listElem) return;

  if (this.listElem.firstChild) {
    this.listElem.insertAdjacentHTML("afterbegin", html);
  } else {
    this.listElem.innerHTML = html;
  }
}
```

---

## When to Add Global State

This project intentionally avoids global state. Consider adding global state only when:
1. Multiple independent components need shared state
2. State persists across page navigation (use localStorage)
3. Complex cross-component communication is needed

### Using localStorage for Persistence

```typescript
// theme-switcher.ts
class ThemeSwitcher {
  private STORAGE_KEY = "theme";

  private loadTheme(): string {
    return localStorage.getItem(this.STORAGE_KEY) || "light";
  }

  private saveTheme(theme: string): void {
    localStorage.setItem(this.STORAGE_KEY, theme);
  }
}
```

---

## Common Mistakes

### Storing State in Global Variables

```typescript
// BAD
let currentComment = null;
let isLoading = false;

function submitComment() {
  isLoading = true;
}

// GOOD - encapsulated in class
class Comment {
  private currentComment: Comment | null = null;
  private isLoading = false;
}
```

### Not Cleaning Up State

```typescript
// BAD - timer keeps running
class Toast {
  constructor() {
    this.timer = setInterval(() => {}, 1000);
  }
}

// GOOD - clean up in dispose
class Toast {
  private timer: number | null = null;

  constructor() {
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

### Storing DOM Elements Unnecessarily

```typescript
// BAD - stores text that could be read from DOM
class Component {
  private buttonText: string;

  constructor(btn: HTMLButtonElement) {
    this.buttonText = btn.textContent || "";
  }
}

// GOOD - read from DOM when needed
class Component {
  private button: HTMLButtonElement;

  private getButtonText(): string {
    return this.button.textContent || "";
  }
}
```

---

## Examples

### Complete State Management Example

```typescript
class Comment {
  // Configuration (immutable after construction)
  private config: Config;

  // DOM references
  private formElem: HTMLFormElement | null;
  private listElem: HTMLElement | null;

  constructor(config: Partial<Config> = {}) {
    this.config = { ...defaultConfig, ...config };
    this.formElem = document.querySelector(this.config.formSelector);
    this.listElem = document.querySelector(this.config.listSelector);
  }

  // State changes via methods
  private setButtonLoading(btn: HTMLButtonElement, loading: boolean): void {
    btn.disabled = loading;
    if (loading) {
      btn.dataset.originalText = btn.textContent || "";
      btn.textContent = "Submitting...";
    } else {
      btn.textContent = btn.dataset.originalText || "Submit";
    }
  }

  // State queries
  private isLoading(btn: HTMLButtonElement): boolean {
    return btn.disabled;
  }

  // State updates
  private resetForm(form: HTMLFormElement): void {
    const textarea = form.querySelector<HTMLTextAreaElement>("textarea[name='comment']");
    if (textarea) {
      textarea.value = "";
    }
  }
}
```
