# Notification Feature Migration Design

**Date:** 2026-02-28
**Status:** Approved
**Related Issue:** Migration of notification features from old project to current project

## Overview

This design documents the migration of missing notification features from `/home/alice/Workspace/django-blog-project` to the current project `/home/alice/Workspace/django-dream-blog`. The migration introduces template inheritance for a cleaner, more maintainable structure while adding missing functionality.

## Problem Statement

The current project has most notification functionality migrated, but is missing:
1. Test factories for notification testing
2. Notification icon in the navigation bar
3. Template inheritance structure for better code organization

## Components to Add

### 1. `notify/factories.py` (New File)

Add `NotificationFactory` for testing notification functionality using `django-notifications` models and existing user factories.

### 2. `notifications/base.html` (New Template)

Create a base template that other notification templates will extend, containing:
- Avatar display with fallback to first letter
- Main content container
- Metadata section (timestamp, mark as read link)
- `{% block header %}` for notification-specific content
- Comment HTML display section

### 3. `notifications/comment.html` and `notifications/reply.html` (Refactor)

Refactor existing inclusions to extend `base.html`:
- Only define `{% block header %}` with specific message
- Eliminates code duplication
- Deprecates `inclusions/_comment.html` and `inclusions/_reply.html`

### 4. Navigation Notification Icon (Update `_nav.html`)

Add notification bell icon to navigation:
- Bell icon using RemixIcon (`ri-notification-3-line`)
- Conditional display for authenticated users only
- Unread count badge when count > 0
- Tailwind CSS styling to match existing design
- Links to `{% url 'notify:notification_all' %}`

## Template Structure

```
notifications/
├── base.html          # NEW - Base template with common structure
├── comment.html       # REFACTOR - Extends base.html
├── reply.html         # REFACTOR - Extends base.html
├── list.html          # KEEP - Uses frag filter for inclusion
└── inclusions/
    ├── _comment.html  # DEPRECATE - Functionality moved to comment.html
    └── _reply.html    # DEPRECATE - Functionality moved to reply.html
```

## Data Flow and Context

### Context Processor
- `notification_count` in `notify/context_processors.py`
- Provides `unread_count` to all templates
- Used by navigation to show badge count

### View Context
- `AllNotificationsListView` and `UnreadNotificationsListView` provide:
  - `num_all` - total active notifications
  - `num_unread` - unread notification count

### Template Filter Update
- `frag` filter in `notify_tags.py` needs updating:
  - Current: `comment` → `_comment.html`, `reply` → `_reply.html`
  - Change to: `comment` → `comment.html`, `reply` → `reply.html`

## Error Handling

### Deleted Content
- When `target.content_object` is None, show fallback text
- Preserve existing behavior from current templates

### Anonymous Users
- Context processor returns `None` for `unread_count`
- Navigation icon should not display for anonymous users

### Empty States
- `list.html` already handles empty notification list

### Avatar Handling
- Check for `social_avatar_url`
- Fallback to first letter of username

## Testing Considerations

### Unit Tests to Add
- Notification view rendering (all/unread)
- Notification factory creation
- Context processor output for authenticated/anonymous users
- Template filter `frag` returns correct paths

### Integration Tests
- Comment creation triggers notification
- Reply creation triggers notification
- Mark as read functionality
- Navigation icon displays correct count

## Implementation Notes

1. The `notify` app already exists in both projects with identical views, URLs, and context_processors
2. The current project's templates are already updated with Tailwind CSS
3. Template inheritance will reduce code duplication and improve maintainability
