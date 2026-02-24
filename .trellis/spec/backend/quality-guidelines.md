# Quality Guidelines

> Code quality standards for backend development.

---

## Overview

This project enforces code quality through:
- **pytest** for testing with pytest-django
- **Factory Boy** for test fixtures
- **test-plus** for enhanced test assertions
- **freezegun** for time-based testing

---

## Testing Requirements

### Test Structure

Tests are organized in a `tests/` directory within each app:

```
dream_blog/posts/tests/
├── __init__.py
├── factories.py      # Factory Boy factories
├── test_models.py    # Model tests
├── test_views.py     # View tests
└── test_admin.py     # Admin tests
```

### Test Naming Convention

- Test files: `test_{what}.py`
- Test functions: `test_{what}_{condition}_{expected}`
- Use `pytestmark = pytest.mark.django_db` for database tests

### Test Example

```python
# dream_blog/posts/tests/test_views.py
import pytest
from freezegun import freeze_time
from posts.models import Post
from posts.tests.factories import PostFactory
from test_plus.plugin import TestCase

pytestmark = pytest.mark.django_db


def test_post_detail_view_is_good(tp: TestCase, post: Post):
    response = tp.get_check_200("posts:detail", pk=post.pk)
    tp.assertTemplateUsed(response, "posts/detail.html")


def test_post_detail_view_hits(tp: TestCase, post: Post):
    assert post.hits == 0

    tp.get_check_200("posts:detail", pk=post.pk)
    post.refresh_from_db()
    assert post.hits == 1
```

### Fixtures

Define fixtures in `conftest.py`:

```python
# dream_blog/conftest.py
import pytest
from posts.models import Post
from posts.tests.factories import PostFactory
from users.models import User


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username="user", password="password", email="user@example.com"
    )


@pytest.fixture
def post(user: User) -> Post:
    return PostFactory(author=user, title="Test Title")
```

### Factory Boy Pattern

```python
# dream_blog/posts/tests/factories.py
import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from posts.models import Post
from users.tests.factories import UserFactory


class PostFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    excerpt = factory.Faker("sentence")
    publish_date = factory.LazyFunction(timezone.now)

    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post
```

---

## Required Patterns

### Class-Based Views

Always use class-based views:

```python
# GOOD
class PostDetailView(SetHeadlineMixin, HitCountDetailView):
    model = Post
    count_hit = True
    template_name = "posts/detail.html"

    def get_queryset(self):
        return Post.objects.visible().with_comment_count()

# BAD - function-based views for complex logic
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # ...
```

### Translation Strings

Use `gettext_lazy` for all user-facing strings:

```python
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    publish_date = models.DateTimeField(_("Publish Date"), blank=True, null=True)
```

### URL Namespacing

Always namespace app URLs:

```python
# dream_blog/posts/urls.py
app_name = "posts"

urlpatterns = [
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
]
```

Usage in templates:
```html
{% url 'posts:detail' pk=post.pk %}
```

---

## Forbidden Patterns

### Don't Use Function-Based Views for CRUD Operations

```python
# BAD
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/detail.html", {"post": post})

# GOOD
class PostDetailView(DetailView):
    model = Post
    template_name = "posts/detail.html"
```

### Don't Hardcode URLs

```python
# BAD
return redirect("/posts/123/")

# GOOD
return redirect(post.get_absolute_url())
# or
return reverse("posts:detail", kwargs={"pk": post.pk})
```

### Don't Skip Translation

```python
# BAD
title = models.CharField("Title", max_length=200)

# GOOD
title = models.CharField(_("Title"), max_length=200)
```

### Don't Use .objects.all() Without Ordering

```python
# BAD - unpredictable order
Post.objects.all()

# GOOD - explicit ordering
Post.objects.all().order_by("-publish_date")
```

---

## Code Review Checklist

### Before Submitting

- [ ] All new code has corresponding tests
- [ ] Tests pass: `pytest`
- [ ] No hardcoded URLs or strings
- [ ] User-facing strings use translation (`_()`)
- [ ] Class-based views follow project patterns
- [ ] Models use abstract base classes from `core.models`
- [ ] Foreign keys use `settings.AUTH_USER_MODEL`
- [ ] Query optimization: `select_related` / `prefetch_related` used where needed

### Model Review

- [ ] Inherits from appropriate abstract models
- [ ] `__str__` method defined
- [ ] `get_absolute_url` defined if appropriate
- [ ] `Meta` class with `verbose_name` and `verbose_name_plural`
- [ ] Custom Manager/QuerySet if needed

### View Review

- [ ] Uses class-based view
- [ ] `get_queryset` uses custom QuerySet methods
- [ ] Template name follows convention
- [ ] Proper error handling

### Admin Review

- [ ] `@admin.register(Model)` decorator used
- [ ] `list_display`, `list_filter`, `search_fields` defined
- [ ] `list_select_related` for FK optimization
- [ ] Custom `save_model` if needed

---

## Running Tests

```bash
# Run all tests
pytest

# Run tests for specific app
pytest dream_blog/posts/tests/

# Run specific test file
pytest dream_blog/posts/tests/test_views.py

# Run specific test
pytest dream_blog/posts/tests/test_views.py::test_post_detail_view_is_good

# Run with coverage
pytest --cov=dream_blog
```
