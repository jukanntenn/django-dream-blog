# Error Handling

> How errors are handled in this Django project.

---

## Overview

This project uses Django's built-in error handling with custom bad request responses for API-style interactions. The project follows Django's class-based view patterns with form validation.

---

## Error Types

### Django Built-in Exceptions

The project uses Django's standard exceptions:

```python
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseBadRequest
```

### Custom Error Responses

For HTMX/AJAX requests, use `CommentPostBadRequest` from `tree_comments`:

```python
from tree_comments.views import CommentPostBadRequest

# Returns HTTP 400 with error message
return CommentPostBadRequest("Missing content_type or object_pk field.")
```

---

## Error Handling Patterns

### View Error Handling

Use try-except for expected error conditions:

```python
# dream_blog/comments/views.py
def inject_comment_target(func):
    @functools.wraps(func)
    def wrapper(view, *args, **kwargs):
        request = view.request
        ctype = request.POST.get("content_type")
        object_pk = request.POST.get("object_pk")

        if ctype is None or object_pk is None:
            return CommentPostBadRequest("Missing content_type or object_pk field.")

        try:
            model = apps.get_model(*ctype.split(".", 1))
            target = model.objects.get(pk=object_pk)
            view.kwargs["target"] = target
        except (LookupError, TypeError):
            return CommentPostBadRequest(
                "Invalid content_type value: %r" % escape(ctype)
            )
        except AttributeError:
            return CommentPostBadRequest(
                "The given content-type %r does not resolve to a valid model."
                % escape(ctype)
            )
        except ObjectDoesNotExist:
            return CommentPostBadRequest(
                "No object matching content-type %r and object PK %r exists."
                % (escape(ctype), escape(object_pk))
            )
        except (ValueError, ValidationError) as e:
            return CommentPostBadRequest(
                "Attempting to get content-type %r and object PK %r raised %s"
                % (escape(ctype), escape(object_pk), e.__class__.__name__)
            )
        return func(view, *args, **kwargs)

    wrapper.__wrapped__ = func
    return wrapper
```

### Form Validation

Use Django's form validation:

```python
class CommentPostView(FormView):
    def form_invalid(self, form):
        return CommentPostBadRequest(
            "The comment form failed verification: %s" % escape(str(form.errors))
        )

    def form_valid(self, form):
        # Process valid form
        pass
```

### Model Validation

Raise `ValueError` for invalid operations on model instances:

```python
# dream_blog/core/models.py
class PreviousNextMixin:
    def get_next_or_previous(self, is_next, ordering=None, value_fields=None, **kwargs):
        if not self.pk:
            raise ValueError(
                _("get_next/get_previous cannot be used on unsaved objects.")
            )
```

---

## HTTP Error Responses

### 404 Not Found

Django's `get_object_or_404` for simple cases:

```python
from django.shortcuts import get_object_or_404

post = get_object_or_404(Post, pk=pk)
```

For QuerySet-based filtering, return 404 if no results:

```python
# In views - get_queryset returns empty, raises 404 automatically
def get_queryset(self):
    return Post.objects.visible()  # Returns 404 if hidden or not published
```

### 400 Bad Request

Use `CommentPostBadRequest` for form/API errors:

```python
return CommentPostBadRequest("Error message here")
```

### 403 Forbidden

Use Django's permission decorators:

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required)
def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)
```

---

## Signal-based Error Handling

Use Django signals to interrupt processes:

```python
# dream_blog/comments/views.py
responses = signals.comment_will_be_posted.send(
    sender=comment.__class__, comment=comment, request=request
)

for receiver, response in responses:
    if response is False:
        return CommentPostBadRequest(
            "comment_will_be_posted receiver %r killed the comment"
            % receiver.__name__
        )
```

---

## Common Mistakes

### Don't Swallow Exceptions

```python
# BAD
try:
    do_something()
except:
    pass  # Hides all errors

# GOOD - be specific about what you catch
try:
    do_something()
except ObjectDoesNotExist:
    # Handle expected error
    pass
```

### Don't Return HTML Errors for API Requests

```python
# BAD for HTMX/AJAX
raise Http404("Not found")  # Returns HTML error page

# GOOD for HTMX/AJAX
return CommentPostBadRequest("Not found")  # Returns plain text
```

### Always Escape User Input in Error Messages

```python
# BAD - XSS vulnerability
return CommentPostBadRequest(f"Invalid content_type: {ctype}")

# GOOD - escaped
return CommentPostBadRequest(
    "Invalid content_type value: %r" % escape(ctype)
)
```

---

## Examples

### Complete Error Handling Example

```python
# dream_blog/comments/views.py
import functools
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView
from tree_comments.views import CommentPostBadRequest


def inject_comment_target(func):
    """Decorator that validates and injects comment target into view kwargs."""
    @functools.wraps(func)
    def wrapper(view, *args, **kwargs):
        request = view.request
        if request.method.upper() == "POST":
            ctype = request.POST.get("content_type")
            object_pk = request.POST.get("object_pk")
        else:
            ctype = request.GET.get("content_type")
            object_pk = request.GET.get("object_pk")

        if ctype is None or object_pk is None:
            return CommentPostBadRequest("Missing content_type or object_pk field.")

        try:
            model = apps.get_model(*ctype.split(".", 1))
            target = model.objects.get(pk=object_pk)
            view.kwargs["target"] = target
        except (LookupError, TypeError):
            return CommentPostBadRequest(
                "Invalid content_type value: %r" % escape(ctype)
            )
        except AttributeError:
            return CommentPostBadRequest(
                "The given content-type %r does not resolve to a valid model."
                % escape(ctype)
            )
        except ObjectDoesNotExist:
            return CommentPostBadRequest(
                "No object matching content-type %r and object PK %r exists."
                % (escape(ctype), escape(object_pk))
            )
        except (ValueError, ValidationError) as e:
            return CommentPostBadRequest(
                "Attempting to get content-type %r and object PK %r raised %s"
                % (escape(ctype), escape(object_pk), e.__class__.__name__)
            )
        return func(view, *args, **kwargs)

    wrapper.__wrapped__ = func
    return wrapper
```
