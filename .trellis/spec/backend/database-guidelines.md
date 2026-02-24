# Database Guidelines

> ORM patterns, migrations, and query conventions for this Django project.

---

## Overview

This project uses:
- **Database**: SQLite for both development and production
- **ORM**: Django ORM with custom QuerySets
- **Migrations**: Standard Django migrations
- **Async Tasks**: Huey with SqliteHuey for background processing

---

## Model Patterns

### Abstract Base Models

Use the abstract models from `core/models.py` for consistent behavior:

```python
# dream_blog/core/models.py
from core.models import (
    TimeStampedModel,    # adds created_at, modified_at
    RichContentModel,    # adds markdown content with TOC
    CommentsModel,       # adds generic comment relation
    HitCountModel,       # adds hit count functionality
)

class Post(HitCountModel, RichContentModel, TimeStampedModel, CommentsModel):
    title = models.CharField(_("Title"), max_length=200)
    # ... other fields
```

**Order matters**: Mixins should be ordered from most specific to least specific.

### Custom QuerySets

Define custom QuerySets for reusable query logic:

```python
# dream_blog/core/models.py
class EntryQuerySet(QuerySet):
    def published(self):
        return self.filter(
            publish_date__isnull=False,
            publish_date__lte=timezone.now(),
        )

    def visible(self):
        return self.published().filter(hidden=False)

    def with_comment_count(self):
        return self.annotate(comment_count=Count("comments"))

# dream_blog/posts/models.py
class PostManager(Manager.from_queryset(EntryQuerySet)):
    pass

class Post(...):
    objects = PostManager()
```

**Usage in views**:
```python
Post.objects.visible().with_comment_count()
```

### Foreign Keys

Always use `settings.AUTH_USER_MODEL` for user references:

```python
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
    )
```

### Model Methods

Use `@cached_property` for computed values that are accessed multiple times:

```python
from django.utils.functional import cached_property

class CommentsModel(models.Model):
    @cached_property
    def num_comments(self):
        if hasattr(self, "comment_count"):
            return getattr(self, "comment_count")
        return self.comments.visible().count()
```

---

## Migrations

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Migration Naming

Django auto-generates migration names. For custom names:
```bash
python manage.py makemigrations --name add_user_email_index
```

### Best Practices

1. **Atomic migrations**: SQLite is configured with `ATOMIC_REQUESTS = True`
2. **Reversible migrations**: Always implement `reverse()` for data migrations
3. **Test migrations**: Run `pytest` after each migration

---

## Query Optimization

### select_related vs prefetch_related

- `select_related`: For ForeignKey and OneToOne relationships
- `prefetch_related`: For ManyToMany and reverse ForeignKey relationships

```python
# In admin.py
list_select_related = ["author"]  # Optimizes list display

# In views.py
Post.objects.select_related("author").prefetch_related("comments")
```

### Annotation for Aggregates

Use annotations to avoid N+1 queries:

```python
# Instead of counting in a loop
for post in posts:
    print(post.comments.count())  # N+1 query problem

# Use annotation
posts = Post.objects.annotate(comment_count=Count("comments"))
for post in posts:
    print(post.comment_count)  # Single query
```

---

## Naming Conventions

### Table Names

Django defaults to `{app}_{model}`. Keep this convention unless there's a strong reason to change.

### Column Names

- Use `snake_case` for field names
- Use verbose names with translation for display:

```python
title = models.CharField(_("Title"), max_length=200)
publish_date = models.DateTimeField(_("Publish Date"), blank=True, null=True)
```

---

## Common Mistakes

### Don't Use Raw SQL

Avoid raw SQL queries unless absolutely necessary. Use Django ORM instead:

```python
# BAD
Post.objects.raw("SELECT * FROM posts_post WHERE hidden = 0")

# GOOD
Post.objects.filter(hidden=False)
```

### Don't Use .all() in Loops

```python
# BAD - loads all records into memory
for post in Post.objects.all():
    print(post.title)

# GOOD - use iterator for memory efficiency
for post in Post.objects.iterator():
    print(post.title)
```

### Don't Access Related Objects Without Prefetching

```python
# BAD - N+1 queries
posts = Post.objects.all()
for post in posts:
    print(post.author.username)  # Queries database each time

# GOOD - single query with join
posts = Post.objects.select_related("author")
for post in posts:
    print(post.author.username)
```

---

## Examples

### Full Model Example

```python
# dream_blog/posts/models.py
from core.models import (
    CommentsModel,
    EntryQuerySet,
    HitCountModel,
    RichContentModel,
    TimeStampedModel,
)
from django.conf import settings
from django.db import models
from django.db.models import Manager
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class PostManager(Manager.from_queryset(EntryQuerySet)):
    pass


class Post(HitCountModel, RichContentModel, TimeStampedModel, CommentsModel):
    title = models.CharField(_("Title"), max_length=200)
    excerpt = models.TextField(_("Excerpt"), blank=True)
    publish_date = models.DateTimeField(
        _("Publish Date"),
        blank=True,
        null=True,
    )
    hidden = models.BooleanField(_("Hidden"), default=False)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
    )

    objects = PostManager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})
```

### QuerySet Usage in Views

```python
# dream_blog/posts/views.py
class PostDetailView(SetHeadlineMixin, HitCountDetailView):
    model = Post
    count_hit = True
    template_name = "posts/detail.html"

    def get_queryset(self):
        return Post.objects.visible().with_comment_count()
```
