# UI Polish: Meta Info, Markdown Icon, Sidebar, Dark Mode, Mobile Menu

## Goal

Polish 5 UI elements to improve visual consistency and readability across the blog.

## What I already know

### Task 1: Home page meta info
- **Current**: `_entry_meta_index.html` uses icons (calendar, eye, comment) and badges (专栏/教程)
- **Reference**: `_entry_meta.html` uses dot separators (`•`) without icons
- **Files**: `dream_blog/templates/inclusions/_entry_meta_index.html`

### Task 2: Markdown icon in comment form
- **Current**: Generic comment icon before "支持 Markdown 语法"
- **File**: `dream_blog/templates/comments/inclusions/_form.html` (line 24-26)

### Task 3: Tutorial sidebar active state
- **Current**: `toc-item--active` uses background highlight (`bg-cyan-50 dark:bg-cyan-900/30`)
- **File**: `frontend/src/styles/components.css` (line 766-771)
- **Sidebar scrollbar**: Already has `scrollbar-hide` class

### Task 4: Dark mode article list separators
- **Current**: `border-b border-slate-100/80 dark:border-slate-800/80`
- **File**: `dream_blog/templates/pages/home.html` (line 9)

### Task 5: Mobile sidebar transparency
- **Current**: `bg-slate-50/80 dark:bg-slate-800/30` (80% and 30% opacity)
- **File**: `dream_blog/templates/base.html` (line 53)

## Assumptions (temporary)

- Task 1: Remove all icons and badges, use only dot separators like the reference
- Task 2: Use official Markdown logo SVG
- Task 3: "Font highlight" means bold + color change, no background
- Task 4: Remove border completely in dark mode (not just reduce opacity)
- Task 5: Increase opacity to ~95% for better readability

## Open Questions

*All questions resolved*

## Requirements (evolving)

### Task 1: Home page meta info
- Remove calendar, eye, and comment icons
- Remove 专栏/教程 badges
- Use dot separators (`•`) between meta items
- Match the style of `_entry_meta.html`

### Task 2: Markdown icon
- Replace generic comment icon with official Markdown logo
- Keep the same size (w-4 h-4)
- Use official Markdown "M" with arrow SVG

### Task 3: Tutorial sidebar
- Change active state from background highlight to font highlight
- Active item: `font-semibold text-cyan-600 dark:text-cyan-400` (no background)
- Show thin scrollbar (2-3px width) instead of hiding it completely

### Task 4: Dark mode separators
- Remove border-bottom in dark mode on home page article list

### Task 5: Mobile sidebar opacity
- Increase background opacity to 95% (`bg-slate-50/95 dark:bg-slate-800/95`)
- Reduce transparency to prevent content interference

## Acceptance Criteria (evolving)

- [ ] Home page meta info matches reference style (dot separators, no icons/badges)
- [ ] Comment form shows Markdown logo instead of generic icon
- [ ] Tutorial sidebar active item uses font highlight (no background)
- [ ] Dark mode home page has no article separators
- [ ] Mobile sidebar has reduced transparency for better readability

## Definition of Done (team quality bar)

- Visual testing in both light and dark modes
- Mobile responsive testing
- Frontend build passes (`pnpm build`)
- No console errors

## Out of Scope (explicit)

- Changes to other meta info displays (detail pages, etc.)
- Functional changes to sidebar navigation
- Changes to desktop sidebar appearance

## Technical Notes

### Files to modify
1. `dream_blog/templates/inclusions/_entry_meta_index.html` - Remove icons/badges, add dot separators
2. `dream_blog/templates/comments/inclusions/_form.html` - Replace icon with Markdown logo
3. `frontend/src/styles/components.css` - Update `toc-item--active` style, add thin scrollbar utility
4. `dream_blog/templates/pages/home.html` - Remove dark mode border
5. `dream_blog/templates/base.html` - Update mobile sidebar opacity

### Implementation details

**Task 1: Meta info**
- Remove SVG icons (calendar, eye, comment)
- Remove badge links for 专栏/教程
- Use dot separator: `<span class="after:content-['•'] after:mx-1">...</span>`

**Task 2: Markdown logo**
- Use official Markdown logo SVG path
- Keep `w-4 h-4` size
- Apply appropriate color classes

**Task 3: Sidebar**
- Update `toc-item--active`: remove background, add `font-semibold text-cyan-600 dark:text-cyan-400`
- Add custom scrollbar utility for thin scrollbar (2-3px width)
- Apply to tutorial sidebar container

**Task 4: Dark mode border**
- Change `dark:border-slate-800/80` to `dark:border-b-0` or `dark:border-transparent`

**Task 5: Mobile sidebar**
- Change `bg-slate-50/80 dark:bg-slate-800/30` to `bg-slate-50/95 dark:bg-slate-800/95`
