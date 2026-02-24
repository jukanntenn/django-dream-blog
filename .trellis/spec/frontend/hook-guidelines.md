# Hook Guidelines

> How modules and initialization patterns are used in this project.

---

## Overview

This project uses **vanilla TypeScript** (not React), so there are no React hooks. Instead, we use:
- **Class-based components** with initialization methods
- **Module-level functions** for utilities
- **Exported initialization functions** for entry points

---

## Module Patterns

### Pattern 1: Class with init() Method

```typescript
// comment.ts
class Comment {
  private elem: HTMLElement | null;

  constructor(config: Partial<Config> = {}) {
    // Initialize properties
  }

  init(): void {
    // Bind events, set up component
  }
}

export default Comment;

// Usage in main.ts or template
const comment = new Comment();
comment.init();
```

### Pattern 2: Exported Initialization Function

```typescript
// navbar-blur.ts
export function initNavbarBlur(): void {
  const navbar = document.getElementById("site-nav");
  if (!navbar) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 10) {
      navbar.classList.add("backdrop-blur-md");
    } else {
      navbar.classList.remove("backdrop-blur-md");
    }
  });
}

// Usage in main.ts
import { initNavbarBlur } from './navbar-blur';
initNavbarBlur();
```

### Pattern 3: Self-Initializing Class

```typescript
// toast.ts
class Toast {
  constructor(message: string, config?: Config) {
    this.config = { ...defaultConfig, ...config };
    this.show(message);  // Auto-show on construction
  }
}

export default Toast;

// Usage - creates and shows immediately
new Toast("Success!", { type: "success" });
```

---

## Data Fetching

### Using Fetch API

```typescript
private fetchForm(url: string): Promise<string> {
  return fetch(url, { method: "GET" })
    .then((response) => {
      if (!response.ok) {
        throw new Error(ERROR_MESSAGES.server);
      }
      return response.text();
    });
}

// Usage
this.fetchForm(`/comments/form/?${params.toString()}`)
  .then((html) => {
    // Process HTML response
  })
  .catch((error) => {
    this.showError(error.message);
  });
```

### POST with FormData

```typescript
private handleSubmit(event: Event): void {
  event.preventDefault();
  const form = event.target as HTMLFormElement;
  const formData = new FormData(form);

  fetch(form.action, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(ERROR_MESSAGES.server);
      }
      return response.text();
    })
    .then((html) => {
      this.insertComment(html);
      new Toast("Comment posted successfully", { type: "success" });
    })
    .catch((error) => {
      this.showError(error.message || ERROR_MESSAGES.network);
    });
}
```

---

## Naming Conventions

| Pattern | Convention | Example |
|---------|------------|----------|
| Classes | PascalCase | `Comment`, `Toast` |
| Functions | camelCase with init prefix | `initNavbarBlur()` |
| Private methods | camelCase with private keyword | `private handleClick()` |
| Constants | UPPER_SNAKE_CASE | `ERROR_MESSAGES` |
| Config types | PascalCase with `Config` suffix | `ToastConfig` |

---

## Event Delegation Pattern

For handling events on dynamic content, use event delegation:

```typescript
class Comment {
  init(): void {
    // Attach single listener to container
    this.listElem?.addEventListener("click", this.handleListClick.bind(this));
  }

  private handleListClick(event: Event): void {
    const target = event.target as HTMLElement;

    // Check for specific elements using closest()
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
}
```

---

## Common Mistakes

### Not Using Event Delegation

```typescript
// BAD - attaches listeners to each button
document.querySelectorAll(".reply-btn").forEach(btn => {
  btn.addEventListener("click", handleClick);
});

// GOOD - single delegated listener
container.addEventListener("click", (event) => {
  const btn = event.target.closest(".reply-btn");
  if (btn) handleClick(btn);
});
```

### Fetching Without Error Handling

```typescript
// BAD - no error handling
fetch(url).then(r => r.text()).then(doSomething);

// GOOD - with error handling
fetch(url)
  .then((response) => {
    if (!response.ok) throw new Error("Server error");
    return response.text();
  })
  .then(doSomething)
  .catch((error) => showError(error.message));
```

### Memory Leaks from Event Listeners

```typescript
// BAD - no cleanup
class Component {
  init() {
    window.addEventListener("scroll", this.handleScroll);
  }
}

// GOOD - provide dispose method
class Component {
  private handleScroll = () => { /* ... */ };

  init() {
    window.addEventListener("scroll", this.handleScroll);
  }

  dispose() {
    window.removeEventListener("scroll", this.handleScroll);
  }
}
```

---

## Examples

### Complete Module Pattern

```typescript
// navbar-blur.ts
const NAVBAR_ID = "site-nav";
const BLUR_THRESHOLD = 10;
const BLUR_CLASS = "backdrop-blur-md";

function initNavbarBlur(): void {
  const navbar = document.getElementById(NAVBAR_ID);
  if (!navbar) return;

  let ticking = false;

  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        if (window.scrollY > BLUR_THRESHOLD) {
          navbar.classList.add(BLUR_CLASS);
        } else {
          navbar.classList.remove(BLUR_CLASS);
        }
        ticking = false;
      });
      ticking = true;
    }
  });
}

export { initNavbarBlur };
```
