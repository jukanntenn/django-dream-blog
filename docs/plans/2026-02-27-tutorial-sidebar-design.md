# Tutorial Sidebar Enhancements Design

**Date:** 2026-02-27
**Status:** Approved
**Type:** UI Enhancement

---

## Goal

Refine the tutorial sidebar to improve visual consistency and usability:

1. Use a more harmonious active state color (teal instead of cyan)
2. Add a thin, unobtrusive scrollbar when chapter list overflows

---

## Requirements

- [ ] Active chapter uses teal color (teal-600 light, teal-400 dark) with font-semibold
- [ ] Chapter list has max-height constraint
- [ ] Scrollbar appears only when content overflows
- [ ] Scrollbar is thin (4px) and aesthetically subtle
- [ ] Title remains fixed (no scroll)

---

## Technical Implementation

### Files to Modify

| File | Change |
|------|--------|
| `frontend/src/styles/components.css` | Update `toc-item--active` color from cyan to teal |
| `dream_blog/templates/tutorials/inclusions/_toc.html` | Add max-height, scrollbar, and overflow classes to `<ul>` |

### CSS Changes

```css
/* Before */
@utility toc-item--active {
  @apply block py-1.5 px-3 -mx-3 rounded-lg
         font-semibold text-cyan-600 dark:text-cyan-400;
}

/* After */
@utility toc-item--active {
  @apply block py-1.5 px-3 -mx-3 rounded-lg
         font-semibold text-teal-600 dark:text-teal-400;
}
```

### Template Changes

```html
<!-- Before -->
<ul class="space-y-0.5">

<!-- After -->
<ul class="space-y-0.5 max-h-[calc(100vh-20rem)] scrollbar-thin overflow-y-auto">
```

---

## Visual Specifications

### Active State Colors

| Mode | Color | Tailwind Class |
|------|-------|----------------|
| Light | Teal 600 | `text-teal-600` |
| Dark | Teal 400 | `text-teal-400` |

### Chapter List States

| State | Text Color | Background |
|-------|------------|------------|
| Active | teal-600 / teal-400 | None |
| Inactive | slate-700 / slate-300 | None |
| Hover | cyan-600 / cyan-400 | slate-100 / slate-800/50 |

### Scrollbar

- Width: 4px
- Track: Transparent
- Thumb: slate-300 (light), slate-600 (dark)
- Border radius: 2px

---

## Rationale

### Why Teal?

1. **Consistency** - Teal is already used for links (`link` class)
2. **Softness** - Less jarring than cyan for navigation states
3. **Purpose alignment** - Sidebar is navigation; teal signals "current location"

### Why Direct Tailwind Classes?

1. **Simplicity** - Single line change in template
2. **Existing utility** - `scrollbar-thin` already defined in components.css
3. **YAGNI** - No need for additional CSS abstraction

---

## Acceptance Criteria

- [ ] Active chapter displays in teal with bold font
- [ ] Inactive chapters display in slate
- [ ] Chapter list scrolls when height exceeds viewport
- [ ] Scrollbar is 4px wide and subtle
- [ ] Title stays fixed during scroll
- [ ] Works correctly in both light and dark modes
- [ ] No layout shifts
