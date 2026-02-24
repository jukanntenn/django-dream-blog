# Type Safety

> Type safety patterns in this project.

---

## Overview

This project uses **TypeScript 5+** for type safety. The configuration is in `frontend/tsconfig.json`.

---

## Type Organization

### Local Types

Define types at the top of each file:

```typescript
// comment.ts
const NAME = "comment";

// Type definitions
type Config = {
  formSelector: string;
  listSelector: string;
  areaSelector: string;
};

type ToastType = "success" | "error" | "info";

// Union types for finite options
type ErrorResponse = {
  message: string;
  code: number;
};
```

### Shared Types

For types used across multiple files, create a `types/` directory:

```typescript
// frontend/src/types/index.ts
export type ApiResponse<T> = {
  data: T;
  status: number;
  message: string;
};

export type PaginationParams = {
  page: number;
  perPage: number;
};
```

---

## Common Patterns

### Config Pattern

```typescript
type Config = {
  selector: string;
  timeout?: number;  // Optional
  onError?: (error: Error) => void;  // Callback
};

const defaultConfig: Config = {
  selector: ".component",
};

class Component {
  private config: Config;

  constructor(config: Partial<Config> = {}) {
    this.config = { ...defaultConfig, ...config };
  }
}
```

### DOM Element Types

```typescript
// Specific element types
private formElem: HTMLFormElement | null;
private listElem: HTMLElement | null;
private textarea: HTMLTextAreaElement | null;
private input: HTMLInputElement | null;
private button: HTMLButtonElement | null;

// Generic element when specific type not needed
private container: HTMLElement | null;

// Event targets
private handleClick(event: Event): void {
  const target = event.target as HTMLElement;
  const button = target.closest<HTMLButtonElement>("button");
}
```

### Generic Types

```typescript
// Generic API response
type ApiResponse<T> = {
  data: T;
  status: number;
};

// Usage
type User = { id: number; name: string };
const response: ApiResponse<User> = await fetchUser();

// Record type for dictionaries
const ERROR_MESSAGES: Record<string, string> = {
  network: "Network error",
  server: "Server error",
};
```

### Union Types

```typescript
// Finite set of options
type ToastType = "success" | "error" | "info";

// Discriminated union
type Result =
  | { success: true; data: string }
  | { success: false; error: Error };
```

---

## Type Guards

### Type Predicate Functions

```typescript
function isHTMLElement(element: Element | null): element is HTMLElement {
  return element !== null;
}

// Usage
const elem = document.querySelector(".item");
if (isHTMLElement(elem)) {
  elem.style.color = "red";  // TypeScript knows it's HTMLElement
}
```

### Type Assertions with closest()

```typescript
// closest() returns Element | null, assert to specific type
const button = target.closest<HTMLButtonElement>(".action-btn");
if (button) {
  button.disabled = true;  // TypeScript knows it's HTMLButtonElement
}
```

---

## Validation

### Runtime Validation

TypeScript types are compile-time only. For runtime validation:

```typescript
// Manual validation
function parseConfig(input: unknown): Config {
  if (typeof input !== "object" || input === null) {
    throw new Error("Invalid config");
  }

  const config = input as Record<string, unknown>;

  return {
    selector: typeof config.selector === "string" ? config.selector : ".default",
    timeout: typeof config.timeout === "number" ? config.timeout : 3000,
  };
}
```

### Type-Safe Event Handling

```typescript
private handleSubmit(event: Event): void {
  event.preventDefault();
  const form = event.target as HTMLFormElement;
  const formData = new FormData(form);
  // formData is typed
}
```

---

## Forbidden Patterns

### Don't Use `any`

```typescript
// BAD
function process(data: any) {
  return data.value;
}

// GOOD - use unknown and validate
function process(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    return (data as { value: string }).value;
  }
  throw new Error("Invalid data");
}

// BETTER - define the expected type
type Input = { value: string };
function process(data: Input) {
  return data.value;
}
```

### Don't Use Non-Null Assertion

```typescript
// BAD - assumes element exists
const elem = document.querySelector(".item")!;
elem.textContent = "Hello";

// GOOD - check for null
const elem = document.querySelector(".item");
elem?.textContent = "Hello";
```

### Don't Cast Without Checking

```typescript
// BAD - unsafe cast
const elem = document.querySelector(".item") as HTMLButtonElement;

// GOOD - use closest with generic
const elem = document.querySelector<HTMLButtonElement>(".item");
if (elem) {
  // TypeScript knows it's HTMLButtonElement | null
}
```

---

## Examples

### Complete Typed Component

```typescript
// toast.ts
const NAME = "toast";

type ToastType = "success" | "error" | "info";

type Config = {
  type?: ToastType;
  duration?: number;
};

const defaultConfig: Required<Config> = {
  type: "info",
  duration: 3000,
};

class Toast {
  private elem: HTMLElement | null = null;
  private config: Required<Config>;
  private timer: number | null = null;

  constructor(message: string, config?: Config) {
    this.config = { ...defaultConfig, ...config };
    this.show(message);
  }

  static get NAME(): string {
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
    if (this.timer !== null) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    if (this.elem?.parentNode) {
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

### Type-Safe Fetch Wrapper

```typescript
type FetchOptions = {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  headers?: Record<string, string>;
  body?: FormData | string;
};

async function fetchJson<T>(url: string, options?: FetchOptions): Promise<T> {
  const response = await fetch(url, {
    method: options?.method || "GET",
    headers: options?.headers,
    body: options?.body,
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

// Usage
interface User {
  id: number;
  name: string;
}

const user = await fetchJson<User>("/api/users/1");
// user is typed as User
```
