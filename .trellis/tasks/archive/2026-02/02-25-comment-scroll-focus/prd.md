# Comment Scroll and Form Auto-Focus

## Goal

Improve comment UX by adding smooth scroll with auto-focus for comment interactions:
1. Meta info comment link → smooth scroll + focus (both detail page and index → detail navigation)
2. Reply button → auto-focus after form expands
3. Reply completion → form auto-collapses (already working)

## What I already know

### Current Implementation

1. **Comment module initialization** (`index.js` lines 56-57):
   - `commentModule` is a global instance
   - `commentModule.init()` binds form submit and list click handlers

2. **Meta info templates**:
   - `_entry_meta.html` (detail pages): links to `#comment-area` on current page
   - `_entry_meta_index.html` (index pages): links to `{{ entry|entry_url }}#comment-area` (navigates to detail)

3. **Content types affected**:
   - Posts (`posts/detail.html`)
   - Articles (`columns/article_detail.html`)
   - Materials (`tutorials/material_detail.html`)
   - All use same `_entry_meta.html` and `show_comment_app` tag

4. **Existing hash scroll handling** (`index.js` lines 118-133):
   - Handles initial page load with hash in URL
   - Uses `commentModule.scrollToSelector()` for comment targets
   - This covers index → detail page navigation scenario!

5. **Reply form** (`_comment.html` line 31):
   - Has class `.reply` with `data-cid` attribute
   - Form inserted inline via `handleReply()` in `comment.ts`
   - No auto-focus after form expands

6. **Reply auto-collapse** (already implemented in `comment.ts` lines 199-205)

7. **Form textarea ID**: Dynamically generated via `{{ form.comment.id_for_label }}`

## Requirements

### R1: Detail Page Meta Info Click
- Click comment link in `_entry_meta.html` → smooth scroll to `#comment-area`
- After scroll → focus the comment textarea (if authenticated)
- Anonymous users → scroll only (no form to focus)

### R2: Index Page → Detail Page Navigation
- Click comment link in `_entry_meta_index.html` → navigate to detail page with `#comment-area` hash
- On detail page load → smooth scroll to `#comment-area` + focus textarea
- Leverage existing hash handling in `index.js` (lines 118-133)

### R3: Reply Button Click
- Click `.reply` button → form expands inline
- After form inserted → auto-focus the textarea
- Already calls `setupReplyForm()` at line 140 in `comment.ts`

### R4: Reply Completion Auto-Collapse
- Already working (lines 199-205 in `comment.ts`)
- No changes needed

## Acceptance Criteria

- [x] On detail page: clicking meta info comment link smoothly scrolls to comment area
- [x] After scroll: comment textarea receives focus (authenticated users only)
- [x] From index page: clicking comment link navigates to detail page, scrolls to comment area, focuses textarea
- [x] Clicking reply button: form expands and textarea auto-focuses
- [x] Works on posts, articles, and materials detail pages
- [x] Works on desktop and mobile

## Definition of Done

- `pnpm build` succeeds in frontend/
- Manual testing on all three content types
- Test both detail page clicks and index → detail navigation
- Test reply button focus behavior

## Technical Approach

### Changes to `frontend/src/index.js`

1. **Add event delegation for meta info comment links**:
   - Target: `a[href$="#comment-area"]` in `.text-slate-500` (meta info container)
   - Intercept clicks on detail pages
   - Use `commentModule.scrollToSelector('#comment-area', 'smooth')`
   - Focus textarea after scroll

2. **Enhance existing hash handler** (lines 118-133):
   - Add focus logic for `#comment-area` target
   - Use `setTimeout` or `requestAnimationFrame` for timing

### Changes to `frontend/src/comment.ts`

1. **Expose public focus method**:
   ```typescript
   focusForm(): void {
     const textarea = this.formElem?.querySelector<HTMLTextAreaElement>('textarea');
     textarea?.focus();
   }
   ```

2. **Add focus after reply form insertion** (in `handleReply`):
   - After `setupReplyForm()` call, find textarea in inserted form
   - Call `focus()` after small delay

### Focus Timing Strategy

- Use `setTimeout(fn, 100)` for focus after scroll
- This ensures scroll animation has started and DOM is ready
- Alternative: `requestAnimationFrame` + `setTimeout` combo

## Out of Scope

- Changing scroll animation duration
- Adding new UI elements
- Mobile-specific touch interactions
- Changing existing reply collapse behavior

## Technical Notes

### Files to Modify

1. `frontend/src/index.js`:
   - Add click handler for meta info comment links
   - Enhance hash scroll handler with focus

2. `frontend/src/comment.ts`:
   - Add `focusForm()` public method
   - Add focus logic in `handleReply()` after form insertion

### Key Code Locations

- Comment initialization: `index.js:56-57`
- Hash scroll handler: `index.js:118-133`
- Meta info template: `_entry_meta.html:3`
- Meta info index template: `_entry_meta_index.html:23`
- Reply handling: `comment.ts:108-148`
- Scroll method: `comment.ts:284-308`

### Existing Scroll Helper

```javascript
// index.js lines 50-54
function scrollToElement(target, behavior) {
  const top =
    target.getBoundingClientRect().top + window.pageYOffset - getScrollOffsetTop();
  window.scrollTo({ top: Math.max(0, top), behavior });
}
```

This can be reused for the meta info scroll.
