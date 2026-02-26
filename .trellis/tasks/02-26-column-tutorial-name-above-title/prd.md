# Add column/tutorial name above post title

## Goal

Improve the display of column/tutorial names on the home page (list/index page) to enhance layout aesthetics and mobile experience. Change from the current inline format `[parent_title]` to a separate line above the title with format "专栏 · 名称" or "教程 · 名称", with distinct colors for each type.

## What I already know

* Display format: "专栏 · {name}" for columns, "教程 · {name}" for tutorials
* Column color: `#7d5de7` (purple)
* Tutorial color: `#0e8a16` (green)
* Goal: Improve layout aesthetics and mobile display
* The name should appear **above** the post title (not inline)

**Current Implementation**:
- Home page template: `dream_blog/templates/pages/home.html`
- Currently displays `parent_title` inline with title: `[parent_title] Title`
- Color: cyan (`text-cyan-600 dark:text-cyan-400`)
- Data source: `get_index_queryset()` in `dream_blog/core/entries.py`
- Available fields: `parent_title`, `parent_slug`, `type` ('p', 'a', 'm')

**Type mapping**:
- `type='p'`: Post (no parent_title)
- `type='a'`: Article (parent_title = column title)
- `type='m'`: Material (parent_title = tutorial title)

## Assumptions (temporary)

* Only applies to home page list view (not detail pages)
* Posts (type='p') will not display anything (no parent)
* The label should be clickable (link to column/tutorial detail page)

## Open Questions

(none - all resolved)

## Decision (ADR-lite)

**Context**: Need to display column/tutorial names on home page list view with better UX and visual design

**Decision**:
1. Use `entry.type` to determine parent type ('a' = 专栏, 'm' = 教程)
2. Display as clickable link above title with format "类型 · 名称"
3. Use distinct colors: purple (#7d5de7) for columns, green (#0e8a16) for tutorials
4. Font size: text-sm with mb-1 spacing for clear visual hierarchy

**Consequences**:
- Improved mobile experience (separate line instead of inline)
- Better visual distinction between columns and tutorials
- Users can navigate directly to column/tutorial pages
- Simple implementation without backend changes

## Requirements (evolving)

* Display column/tutorial name above post title (not inline)
* Use format: "类型 · 名称" (Type · Name)
* Apply distinct colors: purple (#7d5de7) for columns, green (#0e8a16) for tutorials
* Use `entry.type` to determine type: 'a' = 专栏, 'm' = 教程
* Make the name a clickable link to column/tutorial detail page
* Remove old inline `[parent_title]` display
* Font size: text-sm with mb-1 spacing (compact, clear visual hierarchy)
* Optimize for both desktop and mobile layouts

## Acceptance Criteria (evolving)

* [ ] Column name displays above title with format "专栏 · {name}" and purple color (#7d5de7)
* [ ] Tutorial name displays above title with format "教程 · {name}" and green color (#0e8a16)
* [ ] Names are clickable links to respective column/tutorial detail pages
* [ ] Old inline `[parent_title]` display is removed
* [ ] Font size is text-sm with mb-1 spacing
* [ ] Posts (type='p') show no label
* [ ] Layout looks good on both desktop and mobile viewports

## Definition of Done (team quality bar)

* Tests added/updated (unit/integration where appropriate)
* Lint / typecheck / CI green
* Docs/notes updated if behavior changes
* Manual testing on both desktop and mobile viewports

## Out of Scope (explicit)

* (to be determined)

## Technical Notes

**Files to modify**:
- `dream_blog/templates/pages/home.html` - Change parent_title display from inline to above title

**Current display pattern** (lines 11-18 in home.html):
```html
<h2 class="text-xl font-semibold leading-snug">
  <a href="{{ entry|entry_url }}" class="article-title-link">
    {% if entry.parent_title %}
      <span class="text-cyan-600 dark:text-cyan-400">[{{ entry.parent_title }}]</span>
    {% endif %}
    {{ entry.title }}
  </a>
</h2>
```

**New display pattern**:
```html
{% if entry.parent_title %}
  <div class="text-sm mb-1">
    <a href="{% if entry.type == 'a' %}{% url 'columns:detail' slug=entry.parent_slug %}{% else %}{% url 'tutorials:detail' slug=entry.parent_slug %}{% endif %}"
       class="hover:underline"
       style="color: {% if entry.type == 'a' %}#7d5de7{% else %}#0e8a16{% endif %};">
      {% if entry.type == 'a' %}专栏{% else %}教程{% endif %} · {{ entry.parent_title }}
    </a>
  </div>
{% endif %}
<h2 class="text-xl font-semibold leading-snug">
  <a href="{{ entry|entry_url }}" class="article-title-link">
    {{ entry.title }}
  </a>
</h2>
```

**Available data**:
- `entry.parent_title`: Column or Tutorial title
- `entry.parent_slug`: Column or Tutorial slug
- `entry.type`: 'p' (Post), 'a' (Article/Column), 'm' (Material/Tutorial)

**URL construction**:
- Column: `{% url 'columns:detail' slug=entry.parent_slug %}`
- Tutorial: `{% url 'tutorials:detail' slug=entry.parent_slug %}`
