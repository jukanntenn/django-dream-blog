# Quality Guidelines

> Code quality standards for frontend development.

---

## Overview

This project enforces code quality through:
- **TypeScript** for type safety
- **Vite** for build and bundling
- **Tailwind CSS** for consistent styling
- **Manual testing** for verification

---

## Required Patterns

### TypeScript for New Files

All new frontend files should be TypeScript:

```typescript
// GOOD - TypeScript with types
class Comment {
  private formElem: HTMLFormElement | null;

  constructor(config: Partial<Config> = {}) {
    this.config = { ...defaultConfig, ...config };
  }
}

// BAD - JavaScript without types
class Comment {
  constructor(config = {}) {
    this.config = { ...defaultConfig, ...config };
  }
}
```

### Null Checks

Always use optional chaining for DOM elements:

```typescript
// GOOD
this.elem?.classList.add("active");
const value = input?.value || "";

// BAD - may throw error
this.elem.classList.add("active");
```

### Event Delegation

Use event delegation for dynamic content:

```typescript
// GOOD - single listener on container
this.listElem?.addEventListener("click", this.handleListClick.bind(this));

private handleListClick(event: Event): void {
  const target = event.target as HTMLElement;
  const btn = target.closest<HTMLElement>(".reply");
  if (btn) {
    this.handleReply(btn);
  }
}
```

### Class-Based Components

Use classes for stateful components:

```typescript
// GOOD
class Toast {
  private elem: HTMLElement | null = null;
  private timer: number | null = null;

  constructor(message: string, config?: Config) {
    this.show(message);
  }

  dispose(): void {
    if (this.timer) clearTimeout(this.timer);
  }
}
```

---

## Forbidden Patterns

### Don't Use `var`

```typescript
// BAD
var name = "test";

// GOOD
const name = "test";
let count = 0;
```

### Don't Use Implicit `any`

```typescript
// BAD
function handle(data) {
  return data.value;
}

// GOOD
function handle(data: { value: string }): string {
  return data.value;
}
```

### Don't Modify DOM Directly with innerHTML (for user content)

```typescript
// BAD - XSS vulnerability
element.innerHTML = userInput;

// GOOD - use textContent
element.textContent = userInput;

// GOOD - sanitize if HTML needed
element.innerHTML = sanitizeHTML(userInput);
```

### Don't Skip Error Handling in Fetch

```typescript
// BAD
fetch(url).then(r => r.json()).then(doSomething);

// GOOD
fetch(url)
  .then((response) => {
    if (!response.ok) throw new Error("Request failed");
    return response.json();
  })
  .then(doSomething)
  .catch((error) => {
    console.error(error);
    showError(error.message);
  });
```

### Don't Use Inline Event Handlers

```html
<!-- BAD -->
<button onclick="doSomething()">Click</button>

<!-- GOOD - attach in JS -->
<button class="action-btn">Click</button>
```

```typescript
document.querySelector(".action-btn")?.addEventListener("click", doSomething);
```

---

## Code Style

### File Organization

1. Constants and types at top
2. Default configuration
3. Main class
4. Export at bottom

```typescript
// 1. Constants
const NAME = "comment";

// 2. Types
type Config = { ... };

// 3. Default config
const defaultConfig: Config = { ... };

// 4. Main class
class Comment { ... }

// 5. Export
export default Comment;
```

### Method Ordering

1. Static getters (NAME)
2. Constructor
3. Public methods (init, show, hide)
4. Private methods
5. Cleanup (dispose)

---

## Testing

Currently, this project relies on manual testing. When adding tests:

### Test Checklist

- [ ] Component initializes without errors
- [ ] Event handlers fire correctly
- [ ] State changes reflect in UI
- [ ] Error states handled gracefully
- [ ] Cleanup prevents memory leaks

---

## Code Review Checklist

### Before Submitting

- [ ] TypeScript compiles without errors (`pnpm build`)
- [ ] No `any` types without justification
- [ ] Null checks for all DOM elements
- [ ] Error handling for all fetch calls
- [ ] Event listeners cleaned up in dispose
- [ ] Tailwind classes used for styling (not custom CSS when possible)
- [ ] Dark mode supported where applicable

### TypeScript Review

- [ ] All types defined (no implicit any)
- [ ] Type annotations for function parameters and returns
- [ ] Private properties marked with `private`
- [ ] Null types handled (`| null` where needed)

### DOM Safety

- [ ] Optional chaining for DOM queries
- [ ] Event delegation for dynamic content
- [ ] No innerHTML with unsanitized user content
- [ ] Accessible elements (buttons, aria labels)

---

## Build Commands

```bash
# Development server
cd frontend && pnpm dev

# Production build
cd frontend && pnpm build

# Type check (via build)
cd frontend && pnpm build
```
