# Tutorial Sidebar Enhancements Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update tutorial sidebar to use teal active state color and add thin scrollbar for overflow

**Architecture:**
- Modify CSS utility class for active state color change
- Add Tailwind utility classes directly to template for scrolling behavior
- Build frontend to compile CSS changes

**Tech Stack:** Tailwind CSS 4, Django templates, Vite

---

### Task 1: Update Active State Color in CSS

**Files:**
- Modify: `frontend/src/styles/components.css:767-770`

**Step 1: Read current CSS**

Run: `cat frontend/src/styles/components.css | grep -A 3 "toc-item--active"`

Expected output showing current cyan color:
```css
@utility toc-item--active {
  @apply block py-1.5 px-3 -mx-3 rounded-lg
         font-semibold text-cyan-600 dark:text-cyan-400;
}
```

**Step 2: Edit CSS utility class**

Replace the `toc-item--active` utility in `frontend/src/styles/components.css` (around line 767):

```css
/**
 * TOC Item - Active
 * Usage: <a class="toc-item--active">Current Chapter</a>
 * Design intent: Font highlight without background for cleaner look
 */
@utility toc-item--active {
  @apply block py-1.5 px-3 -mx-3 rounded-lg
         font-semibold text-teal-600 dark:text-teal-400;
}
```

**Step 3: Verify the change**

Run: `grep -A 3 "toc-item--active" frontend/src/styles/components.css`

Expected: Shows `text-teal-600 dark:text-teal-400`

**Step 4: Commit**

```bash
git add frontend/src/styles/components.css
git commit -m "feat(ui): change tutorial toc active color to teal

Replace cyan with teal for active chapter state to improve
visual consistency with link colors throughout the site.
"
```

---

### Task 2: Add Scrollbar to Chapter List Template

**Files:**
- Modify: `dream_blog/templates/tutorials/inclusions/_toc.html:13`

**Step 1: Read current template**

Run: `cat dream_blog/templates/tutorials/inclusions/_toc.html`

Current output should show:
```html
<ul class="space-y-0.5">
```

**Step 2: Add scrolling utilities to ul element**

Edit `dream_blog/templates/tutorials/inclusions/_toc.html`, line 13:

```html
  {# Chapter list with active state and scroll #}
  <ul class="space-y-0.5 max-h-[calc(100vh-20rem)] scrollbar-thin overflow-y-auto">
```

**Step 3: Verify the change**

Run: `grep "space-y-0.5" dream_blog/templates/tutorials/inclusions/_toc.html`

Expected: Shows `max-h-[calc(100vh-20rem)] scrollbar-thin overflow-y-auto`

**Step 4: Commit**

```bash
git add dream_blog/templates/tutorials/inclusions/_toc.html
git commit -m "feat(ui): add thin scrollbar to tutorial chapter list

Add max-height constraint and thin scrollbar for overflow.
Title remains fixed while chapters scroll.
"
```

---

### Task 3: Build Frontend

**Files:**
- Output: `frontend/dist/`

**Step 1: Navigate to frontend directory**

Run: `cd frontend && pwd`

Expected: `/home/alice/Workspace/django-dream-blog/frontend`

**Step 2: Build frontend**

Run: `cd frontend && pnpm build`

Expected output: Build completes successfully with new CSS hash

**Step 3: Verify CSS contains new active color**

Run: `grep -o "text-teal-600" frontend/dist/assets/main-*.css`

Expected: Found teal color in compiled CSS

**Step 4: Commit build artifacts**

```bash
git add frontend/dist/
git commit -m "chore: build frontend with updated toc styles"
```

---

### Task 4: Manual Testing

**Files:**
- Test: Manual browser verification

**Step 1: Start development servers**

Run in separate terminals:
```bash
# Terminal 1: Vite dev server
cd frontend && pnpm dev

# Terminal 2: Django dev server
# Note Vite port from terminal 1, then:
VITE_PORT=<port> uv run python manage.py runserver
```

**Step 2: Navigate to a tutorial page**

Open browser to any tutorial detail page (e.g., `/tutorials/python-basics/`)

**Step 3: Verify active state color**

- Light mode: Active chapter should be teal-600 (darker teal)
- Dark mode: Toggle dark mode, active chapter should be teal-400 (lighter teal)
- Both modes: Active chapter has bold font, no background

**Step 4: Verify scrollbar behavior**

- Add enough chapters or reduce window height to cause overflow
- Scrollbar should appear on right side of chapter list only
- Scrollbar should be 4px wide, subtle color
- Title "目录" should remain fixed at top
- Chapter list should scroll smoothly

**Step 5: Verify hover states still work**

- Hover over inactive chapters: should show cyan color and light background
- Click different chapter: should become teal active state

**Step 6: Document test results**

If all tests pass, the implementation is complete.

---

## Testing Checklist

- [ ] Active chapter uses teal color in light mode
- [ ] Active chapter uses teal color in dark mode
- [ ] Active chapter has bold font weight
- [ ] Active chapter has no background color
- [ ] Inactive chapters use slate color
- [ ] Hover shows cyan color with background
- [ ] Scrollbar appears when content overflows
- [ ] Scrollbar is thin (4px) and subtle
- [ ] Title stays fixed during scroll
- [ ] Scrolling is smooth

---

## Notes

- The `scrollbar-thin` utility already exists in `components.css` (line 882-895)
- Max-height of `calc(100vh-20rem)` leaves room for header, title, and padding
- No JavaScript required - pure CSS solution
