# Migrate @tailwindcss/postcss to @tailwindcss/vite

## Goal

Replace the PostCSS-based Tailwind CSS integration with the dedicated Vite plugin for improved performance and developer experience.

## What I already know

**Current Setup:**
- Using `@tailwindcss/postcss@^4.1.18` via `postcss.config.js`
- Vite 5.0.8 with multiple entry points (main.ts, preview.css, admin-theme-sync.ts, admin-preview-render.ts)
- Tailwind CSS 4.1.18 with CSS-first configuration (`@theme`, `@custom-variant`, `@utility` in CSS files)
- CSS imports: `@import "tailwindcss"` in `tailwind-base.css`
- Template scanning: `@source '../../dream_blog/templates/**/*.{html,js}'` in `index.css`

**Recommended by Tailwind:**
> "If you're using Vite, we recommend migrating from the PostCSS plugin to the new dedicated Vite plugin for improved performance and the best developer experience."

## Research Notes

### What the migration involves

1. **Install** `@tailwindcss/vite` package
2. **Update** `vite.config.js` to add the plugin
3. **Remove** `postcss.config.js` (no longer needed)
4. **Remove** `@tailwindcss/postcss` and `postcss` dependencies

### Constraints from our repo

- Multiple entry points in Vite config (must all continue working)
- Django integration via `django-vite` (should be unaffected)
- CSS-first Tailwind 4 configuration (fully compatible)
- `@source` directive for template scanning (works with Vite plugin)

### Feasible approaches

**Approach A: Clean Migration** (Recommended)

- Install `@tailwindcss/vite`
- Add plugin to `vite.config.js` (first in plugins array)
- Delete `postcss.config.js`
- Remove `@tailwindcss/postcss` and `postcss` from dependencies

*Pros:*
- Simpler configuration (one less config file)
- Better performance (Vite-native integration)
- Official recommendation for Vite projects
- HMR improvements

*Cons:*
- None identified

**Approach B: Keep PostCSS as backup**

- Add `@tailwindcss/vite` but keep PostCSS config
- Switch between them via environment variable

*Pros:*
- Easy rollback

*Cons:*
- Unnecessary complexity
- Maintaining two configurations

## Requirements

- [ ] Install `@tailwindcss/vite` package
- [ ] Update `vite.config.js` to use the Vite plugin
- [ ] Remove `postcss.config.js`
- [ ] Remove `@tailwindcss/postcss` and `postcss` from `package.json`
- [ ] Verify dev server works (`pnpm dev`)
- [ ] Verify production build works (`pnpm build`)

## Acceptance Criteria

- [ ] `pnpm dev` runs without errors
- [ ] `pnpm build` completes successfully
- [ ] Tailwind styles render correctly in browser
- [ ] HMR works during development
- [ ] No PostCSS-related config files remain

## Definition of Done

- [ ] All acceptance criteria met
- [ ] Manual testing in browser verified
- [ ] No lint/typecheck errors

## Out of Scope

- Changes to Tailwind CSS configuration (`@theme`, `@utility`, etc.)
- Changes to CSS file structure
- Django backend changes

## Technical Notes

**Files to modify:**
- `frontend/package.json` - update dependencies
- `frontend/vite.config.js` - add Vite plugin

**Files to delete:**
- `frontend/postcss.config.js`

**Files unchanged:**
- All CSS files (fully compatible)
- `frontend/src/main.ts` and other entry points

**References:**
- https://tailwindcss.com/docs/installation/using-vite
- https://tailwindcss.com/docs/upgrade-guide
