# Notification UI/UX Improvements

## Goal

Improve the notification system UI/UX to match the current design language of the blog, ensuring visual consistency and proper alignment with page elements.

## What I already know

### Current Issues Identified

1. **Navigation bar notification icon**: Currently uses `ri-notification-3-line` (Remix Icon class) which appears to be missing/broken. The icon should use the SVG file at `dream_blog/static/notification-4-line.svg` instead.

2. **Notification list styling**: The current notification list items use heavy borders (`border border-slate-200 dark:border-slate-700`) which don't match the soft, borderless design language used elsewhere in the UI (see `sidebar-card` utility class).

3. **Container padding issue**: The notification list container has `py-4` padding which causes misalignment with sidebar elements (left/right sidebars use `pt-6` on their own containers).

### UI Design Patterns Found

**Navigation icon pattern** (from `_nav.html`):
```html
<img class="dark:invert" height="20" width="20" src="{% static 'icon-name.svg' %}" />
```

**Sidebar styling pattern** (from `components.css`):
```css
/* sidebar-card uses NO borders - just soft background */
@utility sidebar-card {
  @apply p-5 rounded-xl
         bg-slate-50/80 dark:bg-slate-800/30
         backdrop-blur-sm;
  /* No border - uses soft background and backdrop-blur for depth */
}
```

**Base layout structure** (from `base.html`):
- Main content area: `<div class="w-full pt-6 lg:px-64">`
- Sidebars: `<div ... lg:pt-6 ...>`

### Files to Modify

| File | Changes |
|------|---------|
| `dream_blog/templates/inclusions/_nav.html` | Replace Remix Icon with SVG img tag |
| `dream_blog/templates/notifications/base.html` | Remove `py-4`, simplify list item styling |

## Requirements

1. **Navigation Icon Replacement**
   - Replace `<i class="ri-notification-3-line">` with `<img>` tag using `{% static 'notification-4-line.svg' %}`
   - Follow the existing icon pattern: `height="20" width="20" class="dark:invert"`
   - Ensure badge positioning remains correct with the new icon

2. **Notification List Styling**
   - Remove borders from notification items (`border border-slate-200 dark:border-slate-700`)
   - Remove bottom border from header section
   - Use soft background colors only (similar to `sidebar-card`)
   - Keep spacing between items (`space-y-4`)

3. **Container Alignment**
   - Remove `py-4` from the outer container div in `base.html`
   - Let the natural `pt-6` from base layout handle top alignment

## Acceptance Criteria

- [ ] Navigation bar shows notification SVG icon (not broken Remix Icon)
- [ ] Unread badge is positioned correctly on the new icon
- [ ] Notification list items have no visible borders
- [ ] Notification list uses soft background colors matching sidebar style
- [ ] Notification list container aligns horizontally with sidebar content
- [ ] Styling works in both light and dark modes

## Definition of Done

- Templates updated with new styling
- Visual testing in both light/dark modes
- No lint errors

## Out of Scope

- Notification behavior/functionality changes (UI only)
- Additional notification features
- Mobile-specific styling refinements (unless broken by changes)

## Technical Notes

### Icon Badge Positioning
The current badge uses absolute positioning: `absolute -top-1 -right-1`. This should work fine with the new `<img>` tag as the container has `relative` positioning.

### Design System Reference
The project uses the "Prism Design System" (documented in `frontend/src/styles/components.css`):
- Soft, borderless cards (`sidebar-card`)
- Whitespace for separation instead of borders
- Backdrop blur and subtle backgrounds for depth

### Related Files
- `dream_blog/static/notification-4-line.svg` - The icon to use (already exists)
- `frontend/src/styles/components.css` - Design system reference
