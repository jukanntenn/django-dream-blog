# Notification Feature Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate missing notification features (factories, navigation icon, template inheritance) from the old project to the current project.

**Architecture:** Introduce template inheritance for notification templates (base.html with child templates for comment/reply), add navigation icon with unread count, and add test factories. All changes maintain existing functionality while improving code organization.

**Tech Stack:** Django 5+, django-notifications, Tailwind CSS 4, factory_boy

---

## Prerequisites

Before starting, verify:
- `django-notifications` is installed (should already be in dependencies)
- `factory_boy` is installed (for test factories)
- Notification views, URLs, and context_processors already exist

---

## Task 1: Add Notification Factory

**Files:**
- Create: `dream_blog/notify/factories.py`

**Step 1: Create the factories.py file**

Create `dream_blog/notify/factories.py` with:

```python
import factory
from factory.django import DjangoModelFactory
from notifications.models import Notification
from dream_blog.users.tests.factories import UserFactory


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    recipient = factory.SubFactory(UserFactory)
    actor = factory.SubFactory(UserFactory)
    verb = "comment"
```

**Step 2: Verify the file exists and has correct syntax**

Run: `python -m py_compile dream_blog/notify/factories.py`
Expected: No output (successful compilation)

**Step 3: Commit**

```bash
git add dream_blog/notify/factories.py
git commit -m "feat(notify): add NotificationFactory for testing"
```

---

## Task 2: Create Notification Base Template

**Files:**
- Create: `dream_blog/templates/notifications/base.html`

**Step 1: Create the base template**

Create `dream_blog/templates/notifications/base.html` with:

```html
{% load notifications_tags %}
<div class="flex items-start gap-3">
  {# Avatar #}
  <div class="flex-shrink-0">
    <div class="w-10 h-10 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center">
      {% if actor.social_avatar_url %}
        <img src="{{ actor.social_avatar_url }}" alt="" class="w-10 h-10 rounded-full object-cover">
      {% else %}
        <span class="text-slate-500 dark:text-slate-400 text-sm">{{ actor.name|slice:":1"|default:"?" }}</span>
      {% endif %}
    </div>
  </div>
  {# Content #}
  <div class="flex-1 min-w-0">
    {% block header %}{% endblock %}
    <div class="mt-1 text-xs text-slate-500 dark:text-slate-400 flex items-center gap-2">
      <time>{{ notification.timestamp|date:'Y-m-d H:i' }}</time>
      {% if notification.unread %}
        <a class="text-cyan-600 dark:text-cyan-400 hover:text-cyan-700 dark:hover:text-cyan-300"
           href="{% url 'notifications:mark_as_read' notification.slug %}?next={{ request.path }}{% if request.META.QUERY_STRING %}&{{ request.META.QUERY_STRING }}{% endif %}">
          标为已读</a>
      {% endif %}
    </div>
  </div>
</div>
{% if target.comment_html %}
  <div class="mt-3 text-sm text-slate-600 dark:text-slate-400 prose prose-sm dark:prose-invert max-w-none">
    {{ target.comment_html|safe }}
  </div>
{% endif %}
```

**Step 2: Verify template syntax**

Run: `python manage.py check --deploy 2>&1 | grep -i template`
Expected: No template-related errors

**Step 3: Commit**

```bash
git add dream_blog/templates/notifications/base.html
git commit -m "feat(notify): add base notification template with common structure"
```

---

## Task 3: Refactor Comment Template to Use Inheritance

**Files:**
- Modify: `dream_blog/templates/notifications/comment.html`
- Deprecate: `dream_blog/templates/notifications/inclusions/_comment.html`

**Step 1: Create new comment.html extending base.html**

Create `dream_blog/templates/notifications/comment.html` with:

```html
{% extends 'notifications/base.html' %}
{% load notifications_tags %}

{% block header %}
  <div class="text-sm text-slate-900 dark:text-slate-100">
    <span class="font-medium text-slate-600 dark:text-slate-400">{{ actor.name }}</span>
    {% if target.content_object %}
      评论了文章
      <a class="text-cyan-600 dark:text-cyan-400 hover:underline" target="_blank" href="{{ target.content_object.get_absolute_url }}#c{{ target.pk }}">{{ target.content_object.title }}</a>
    {% else %}
      评论了已删除的内容
    {% endif %}
  </div>
{% endblock %}
```

**Step 2: Update frag filter to use new template**

Modify `dream_blog/notify/templatetags/notify_tags.py:24-27`:

Change from:
```python
@register.filter
def frag(notification):
    verb = notification.verb
    return "notifications/inclusions/_{verb}.html".format(verb=verb)
```

To:
```python
@register.filter
def frag(notification):
    verb = notification.verb
    return "notifications/{verb}.html".format(verb=verb)
```

**Step 3: Delete the old inclusion template**

Run: `rm dream_blog/templates/notifications/inclusions/_comment.html`

**Step 4: Test the template rendering**

Run: `python manage.py shell`
```python
from dream_blog.notify.factories import NotificationFactory
from django.template import Template, Context

# Create a test notification
notif = NotificationFactory(verb="comment")

# Test template rendering
from django.template.loader import render_to_string
output = render_to_string("notifications/comment.html", {
    "notification": notif,
    "actor": notif.actor,
    "target": notif.target,
})
print("Template renders successfully" if output else "Template failed")
exit()
```

Expected: "Template renders successfully"

**Step 5: Commit**

```bash
git add dream_blog/templates/notifications/comment.html
git add dream_blog/notify/templatetags/notify_tags.py
git commit -m "refactor(notify): refactor comment template to extend base"
```

---

## Task 4: Refactor Reply Template to Use Inheritance

**Files:**
- Modify: `dream_blog/templates/notifications/reply.html`
- Deprecate: `dream_blog/templates/notifications/inclusions/_reply.html`

**Step 1: Create new reply.html extending base.html**

Create `dream_blog/templates/notifications/reply.html` with:

```html
{% extends 'notifications/base.html' %}
{% load notifications_tags %}

{% block header %}
  <div class="text-sm text-slate-900 dark:text-slate-100">
    <span class="font-medium text-slate-600 dark:text-slate-400">{{ actor.name }}</span>
    {% if target.content_object %}
      在文章
      <a class="text-cyan-600 dark:text-cyan-400 hover:underline" target="_blank" href="{{ target.content_object.get_absolute_url }}#c{{ target.pk }}">{{ target.content_object.title }}</a>
      中回复了你
    {% else %}
      在已删除的内容中回复了你
    {% endif %}
  </div>
{% endblock %}
```

**Step 2: Delete the old inclusion template**

Run: `rm dream_blog/templates/notifications/inclusions/_reply.html`

**Step 3: Delete the empty inclusions directory if empty**

Run: `rmdir dream_blog/templates/notifications/inclusions/ 2>/dev/null || true`

**Step 4: Test the template rendering**

Run: `python manage.py shell`
```python
from dream_blog.notify.factories import NotificationFactory

# Create a test notification
notif = NotificationFactory(verb="reply")

# Test template rendering
from django.template.loader import render_to_string
output = render_to_string("notifications/reply.html", {
    "notification": notif,
    "actor": notif.actor,
    "target": notif.target,
})
print("Template renders successfully" if output else "Template failed")
exit()
```

Expected: "Template renders successfully"

**Step 5: Commit**

```bash
git add dream_blog/templates/notifications/reply.html
git commit -m "refactor(notify): refactor reply template to extend base"
```

---

## Task 5: Add Notification Icon to Navigation

**Files:**
- Modify: `dream_blog/templates/inclusions/_nav.html`

**Step 1: Add notifications tag loading**

At the top of `dream_blog/templates/inclusions/_nav.html`, add notifications tag loading:

Change line 1 from:
```html
{% load static %}
```

To:
```html
{% load static %}
{% load notifications_tags %}
```

**Step 2: Add notification icon after the theme switcher button**

Add the notification icon section after the theme switcher button (after `</button>` on line 41, before `</div></div></div>` closing tags):

```html
        {% if user.is_authenticated %}
          {% notifications_unread as num_unread %}
          <a href="{% url 'notify:notification_all' %}"
             class="p-2 rounded-lg hover:bg-slate-100/80 dark:hover:bg-slate-800/50 transition-colors relative"
             aria-label="通知">
            <i class="ri-notification-3-line text-slate-600 dark:text-slate-400{% if num_unread != 0 %} text-cyan-600 dark:text-cyan-400{% endif %}"></i>
            {% if num_unread != 0 %}
              <span class="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-cyan-600 dark:bg-cyan-400 text-[10px] font-bold text-white dark:text-slate-900">
                {% if num_unread > 99 %}99+{% else %}{{ num_unread }}{% endif %}
              </span>
            {% endif %}
          </a>
        {% endif %}
```

**Step 3: Verify the navigation template**

Run: `python manage.py check --deploy 2>&1 | grep -i template`
Expected: No template-related errors

**Step 4: Commit**

```bash
git add dream_blog/templates/inclusions/_nav.html
git commit -m "feat(ui): add notification icon with unread count to navigation"
```

---

## Task 6: Add Unit Tests for Notification Factory

**Files:**
- Create: `dream_blog/notify/tests/test_factories.py`

**Step 1: Create test file**

Create `dream_blog/notify/tests/test_factories.py` with:

```python
import pytest
from notifications.models import Notification
from dream_blog.notify.factories import NotificationFactory
from dream_blog.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestNotificationFactory:
    def test_factory_creates_notification(self):
        """Test that NotificationFactory creates a valid notification."""
        notification = NotificationFactory()
        assert isinstance(notification, Notification)
        assert notification.recipient is not None
        assert notification.actor is not None
        assert notification.verb == "comment"

    def test_factory_with_custom_verb(self):
        """Test that NotificationFactory accepts custom verb."""
        notification = NotificationFactory(verb="reply")
        assert notification.verb == "reply"

    def test_factory_creates_unique_users(self):
        """Test that recipient and actor are different users by default."""
        notification = NotificationFactory()
        assert notification.recipient != notification.actor

    def test_factory_with_same_user(self):
        """Test that same user can be both recipient and actor."""
        user = UserFactory()
        notification = NotificationFactory(recipient=user, actor=user)
        assert notification.recipient == notification.actor
```

**Step 2: Run the tests**

Run: `pytest dream_blog/notify/tests/test_factories.py -v`
Expected: All tests PASS (4 passed)

**Step 3: Commit**

```bash
git add dream_blog/notify/tests/test_factories.py
git commit -m "test(notify): add unit tests for NotificationFactory"
```

---

## Task 7: Add Unit Tests for Template Filter

**Files:**
- Create: `dream_blog/notify/tests/test_templatetags.py`

**Step 1: Create test file**

Create `dream_blog/notify/tests/test_templatetags.py` with:

```python
import pytest
from django.template import Template, Context
from dream_blog.notify.factories import NotificationFactory
from dream_blog.notify.templatetags.notify_tags import frag


@pytest.mark.django_db
class TestNotifyTags:
    def test_frag_filter_comment(self):
        """Test that frag filter returns correct template for comment."""
        notification = NotificationFactory(verb="comment")
        result = frag(notification)
        assert result == "notifications/comment.html"

    def test_frag_filter_reply(self):
        """Test that frag filter returns correct template for reply."""
        notification = NotificationFactory(verb="reply")
        result = frag(notification)
        assert result == "notifications/reply.html"

    def test_frag_filter_unknown_verb(self):
        """Test that frag filter handles unknown verbs."""
        notification = NotificationFactory(verb="unknown")
        result = frag(notification)
        assert result == "notifications/unknown.html"
```

**Step 2: Run the tests**

Run: `pytest dream_blog/notify/tests/test_templatetags.py -v`
Expected: All tests PASS (3 passed)

**Step 3: Commit**

```bash
git add dream_blog/notify/tests/test_templatetags.py
git commit -m "test(notify): add unit tests for template tags"
```

---

## Task 8: Add Integration Tests for Notification Views

**Files:**
- Create: `dream_blog/notify/tests/test_views.py`

**Step 1: Create test file**

Create `dream_blog/notify/tests/test_views.py` with:

```python
import pytest
from django.urls import reverse
from dream_blog.notify.factories import NotificationFactory
from dream_blog.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestNotificationViews:
    def test_all_notifications_list_requires_login(self, client):
        """Test that all notifications list requires authentication."""
        url = reverse("notify:notification_all")
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith("/accounts/login/")

    def test_unread_notifications_list_requires_login(self, client):
        """Test that unread notifications list requires authentication."""
        url = reverse("notify:notification_unread")
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith("/accounts/login/")

    def test_all_notifications_list_authenticated(self, client):
        """Test that authenticated user can see all notifications."""
        user = UserFactory()
        client.force_login(user)
        NotificationFactory.create_batch(5, recipient=user)

        url = reverse("notify:notification_all")
        response = client.get(url)
        assert response.status_code == 200
        assert "notifications" in response.context

    def test_unread_notifications_list_authenticated(self, client):
        """Test that authenticated user can see unread notifications."""
        user = UserFactory()
        client.force_login(user)
        NotificationFactory.create_batch(3, recipient=user, unread=True)

        url = reverse("notify:notification_unread")
        response = client.get(url)
        assert response.status_code == 200
```

**Step 2: Run the tests**

Run: `pytest dream_blog/notify/tests/test_views.py -v`
Expected: All tests PASS (4 passed)

**Step 3: Commit**

```bash
git add dream_blog/notify/tests/test_views.py
git commit -m "test(notify): add integration tests for notification views"
```

---

## Task 9: Verify End-to-End Notification Flow

**Files:**
- None (verification only)

**Step 1: Start development server**

Run: `python manage.py runserver 127.0.0.1:8000`
Note: Keep server running for manual testing

**Step 2: Manual verification checklist**

1. Log in as a test user
2. Visit `/notifications/` - should see notification list page
3. Check navigation bar for notification icon
4. Create a comment on a post
5. Verify notification appears for post author
6. Verify unread count badge shows on notification icon
7. Click "标为已读" (mark as read) link
8. Verify notification is marked as read

**Step 3: Run all notification tests**

Run: `pytest dream_blog/notify/tests/ -v`
Expected: All tests PASS

**Step 4: Run full test suite to ensure no regressions**

Run: `pytest dream_blog/ -v --tb=short`
Expected: All existing tests still pass

**Step 5: Commit**

```bash
git add docs/plans/2026-02-28-notification-migration.md
git commit -m "docs: add notification migration implementation plan"
```

---

## Task 10: Clean Up and Documentation

**Files:**
- Update: `CLAUDE.md` (if needed)
- Update: `docs/plans/2026-02-28-notification-migration-design.md`

**Step 1: Update CLAUDE.md with notification info**

Add to the "Project Structure" section in `CLAUDE.md`:

```markdown
- `notify/`: User notifications (comment replies, mentions)
  - `factories.py`: Notification factory for testing
  - `views.py`: Notification list views (all/unread)
  - `templates/notifications/`: Notification display templates
```

**Step 2: Mark design doc as implemented**

Update `docs/plans/2026-02-28-notification-migration-design.md` header:

Change:
```markdown
**Status:** Approved
```

To:
```markdown
**Status:** Implemented
```

**Step 3: Final commit**

```bash
git add CLAUDE.md docs/plans/2026-02-28-notification-migration-design.md
git commit -m "docs: update project documentation for notification migration"
```

---

## Summary

This implementation plan:
- ✅ Adds test factories for notification testing
- ✅ Introduces template inheritance for cleaner code
- ✅ Adds navigation icon with unread count
- ✅ Provides comprehensive test coverage
- ✅ Maintains backward compatibility

Total estimated steps: 35
Total estimated commits: 10
