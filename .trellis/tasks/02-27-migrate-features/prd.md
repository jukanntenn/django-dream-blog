# Migrate Features from django-blog-project

## Goal

Migrate three feature modules (friendlinks, webtools, and user notification system) from the source Django project (`/home/alice/Workspace/django-blog-project`) to the current project, adapting them to use Tailwind CSS v4 and integrate seamlessly with the existing architecture.

## What I Already Know

### Source Project Features

**1. FriendLinks**
- Located in `blogproject/friendlinks/`
- Model: `FriendLink` (site_name, site_link, rank)
- Inherits from `TimeStampedModel`
- Admin interface for management
- Displayed in blog sidebar

**2. Webtools**
- Located in `blogproject/webtools/`
- Django Secret Key Generator
- Form-based view with prefix/suffix options
- No models - utility tool only
- Template: `webtools/django_secret_key.html`

**3. Notify (User Notification System)**
- Located in `blogproject/notify/`
- Uses `django-notifications-hq` package
- Views: AllNotificationsListView, UnreadNotificationsListView
- Context processor for unread count
- Template tags for notification display
- Templates for notification list

### Current Project State

- Target directories already exist: `dream_blog/friendlinks/`, `dream_blog/notify/`, `dream_blog/webtools/`
- `django-notifications-hq` already in dependencies
- Has `TimeStampedModel` in `dream_blog/core/models.py`
- Missing dependencies: `django-braces`, `django-pure-pagination`

### Dependencies to Add

- `django-braces` - for SetHeadlineMixin
- `django-pure-pagination` - for pagination

## Assumptions (Temporary)

- All three features should be migrated with full functionality
- Templates will need adaptation to current project's template structure
- URLs will be integrated into main URL configuration
- Migration will maintain the same admin interface capabilities

## Decision (ADR-lite)

**Context**: Source project has both "alerts" (admin notification banners) and "notify" (user notifications). User notifications are the primary need.

**Decision**: Migrate only the notify system, skip alerts feature.

**Consequences**: Simpler migration, focus on user-facing notification functionality. No admin banner system will be available.

## What I Already Know (Updated)

### Current Project State

- Target directories already exist: `dream_blog/friendlinks/`, `dream_blog/notify/`, `dream_blog/webtools/`
- `django-notifications-hq` already in dependencies and INSTALLED_APPS
- Has `TimeStampedModel` in `dream_blog/core/models.py`
- Missing dependencies: `django-braces`, `django-pure-pagination`
- Template structure: Uses Tailwind CSS with three-column layout (left sidebar, main, right sidebar)
- URLs organized by app in `config/urls.py`
- Template directories exist but appear empty: `dream_blog/templates/notifications/`, `dream_blog/templates/webtools/`

## Decision (ADR-lite) - URL Structure

**Context**: Need to decide URL patterns for the three features.

**Decision**: Use Standard RESTful URLs:
- FriendLinks: Admin only (no public URLs)
- Webtools: `/webtools/django-secret-key-creator`
- Notify: `/notifications/` (all) and `/notifications/unread/`

**Consequences**: Clear, predictable URL structure following Django conventions.

## Decision (ADR-lite) - Template Styling

**Context**: Source project uses Tailwind CSS v3, current project uses v4.

**Decision**: Use Tailwind CSS styling adapted for v4 syntax, extend base.html template.

**Consequences**: Consistent look and feel with current project. Need to convert v3 class names to v4 syntax where different.

## Decision (ADR-lite) - FriendLinks Display

**Context**: Need to decide where to display friendlinks in the frontend.

**Decision**: Display friendlinks in the right sidebar, alongside tutorials and columns.

**Consequences**: Consistent with source project's sidebar approach, integrates well with existing right sidebar layout.

## Open Questions

None - all major decisions resolved.

## Requirements (Final)

### FriendLinks
- [ ] Create FriendLink model (inherits from TimeStampedModel)
- [ ] Register FriendLink in admin
- [ ] Create template tag to display friendlinks in right sidebar
- [ ] Integrate friendlinks display into base.html right sidebar

### Webtools
- [ ] Create DjangoSecretKeyCreateForm
- [ ] Create DjangoSecretKeyCreateView with SetHeadlineMixin
- [ ] Create URL pattern: `/webtools/django-secret-key-creator`
- [ ] Create template using base.html and Tailwind CSS v4

### Notify
- [ ] Create AllNotificationsListView and UnreadNotificationsListView
- [ ] Create URL patterns: `/notifications/` and `/notifications/unread/`
- [ ] Create context processor for unread notification count
- [ ] Create template tags for notification display
- [ ] Create notification list template using base.html and Tailwind CSS v4
- [ ] Create notification fragment templates for different notification types

### Infrastructure
- [ ] Add django-braces and django-pure-pagination to dependencies
- [ ] Add 'friendlinks' and 'notify' to INSTALLED_APPS
- [ ] Add notification context processor to template context processors
- [ ] Integrate app URLs into main URL configuration
- [ ] Create and run migrations for FriendLink model
- [ ] Test all features

## Acceptance Criteria

- [ ] FriendLinks can be created/edited/deleted in Django admin
- [ ] FriendLinks display in the right sidebar on all pages
- [ ] Django Secret Key generator is accessible at `/webtools/django-secret-key-creator`
- [ ] Secret key generator creates valid 50-character keys with optional prefix/suffix
- [ ] User notifications list is accessible at `/notifications/`
- [ ] Unread notifications list is accessible at `/notifications/unread/`
- [ ] Unread notification count displays in templates via context processor
- [ ] All notification templates use Tailwind CSS v4 styling
- [ ] Pagination works correctly for notification lists
- [ ] All existing tests continue to pass
- [ ] No lint/type errors

## Definition of Done

- Tests added/updated for all three features
- Lint/typecheck pass
- Migrations created and tested
- Templates adapted and styled consistently
- Documentation updated if needed

## Out of Scope (Explicit)

- New features beyond what exists in source project
- Major refactoring of existing code
- Changes to django-notifications-hq configuration

## Technical Approach

### Migration Strategy

1. **Dependencies First**: Add django-braces and django-pure-pagination
2. **Models**: Create FriendLink model with migration
3. **Admin**: Register FriendLink in admin
4. **Views & URLs**: Create views and URL patterns for all three features
5. **Templates**: Adapt source templates to use base.html and Tailwind CSS v4
6. **Integration**: Add template tags, context processors, and integrate into base template

### Key Adaptations

**Tailwind CSS v3 → v4 Changes:**
- No major breaking changes expected for utility classes used
- Test all templates after migration
- Reference: https://tailwindcss.com/docs/upgrade-guide

**Template Structure:**
- Extend `base.html` instead of source's base template
- Use existing three-column layout
- Adapt CSS classes to match current project patterns

**Dependencies:**
- `django-braces`: For SetHeadlineMixin in views
- `django-pure-pagination`: For pagination in notification lists

### Implementation Plan (Small PRs)

**PR1: Infrastructure & FriendLinks**
- Add dependencies
- Create FriendLink model and migration
- Register in admin
- Create template tag and display in sidebar

**PR2: Webtools**
- Create form and view
- Create URL pattern
- Create template

**PR3: Notify System**
- Create views and URLs
- Create context processor and template tags
- Create templates
- Integrate with base template

## Technical Notes

### Source Project Structure
```
blogproject/
├── friendlinks/      # Blog sidebar links
│   ├── models.py     # FriendLink model
│   └── admin.py      # FriendLinkAdmin
├── webtools/         # Utility tools
│   ├── views.py      # DjangoSecretKeyCreateView
│   ├── forms.py      # DjangoSecretKeyCreateForm
│   └── urls.py       # URL patterns
└── notify/           # User notifications
    ├── views.py      # Notification list views
    ├── urls.py       # URL patterns
    ├── context_processors.py  # unread_count
    └── templatetags/ # notify_tags
```

### Current Project Structure
```
dream_blog/
├── friendlinks/      # Empty directory with migrations
├── notify/           # Empty directory with templatetags
└── webtools/         # Empty directory with migrations
```

### Dependencies Comparison

**Source Project:**
- django-notifications-hq = "^1.6.0"
- django-braces = "^1.14.0"
- django-pure-pagination = "^0.3.0"

**Current Project:**
- django-notifications-hq>=1.8.3,<2 (already present)
- Missing: django-braces, django-pure-pagination
