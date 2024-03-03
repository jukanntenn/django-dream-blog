import functools

import django_comments
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http.response import HttpResponse as HttpResponse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, TemplateView
from django_comments import get_form, signals
from django_comments.views.comments import CommentPostBadRequest


def inject_comment_target(func):
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


class CommentFormTemplateView(TemplateView):
    template_name = "tree_comments/inclusions/_form.html"

    @inject_comment_target
    def get(self, request, *args, **kwargs):
        target = self.kwargs.pop("target")

        context = self.get_context_data(**kwargs)
        context["form"] = get_form()(target)

        return self.render_to_response(context)


class CommentPostView(FormView):
    http_method_names = ["post"]
    template_name = "tree_comments/inclusions/_comment.html"

    def get_form_kwargs(self):
        target = self.kwargs.pop("target")
        data = self.request.POST.copy()
        if not data.get("name", ""):
            data["name"] = self.request.user.name or self.request.user.get_username()
        if not data.get("email", ""):
            data["email"] = self.request.user.email

        return {"target_object": target, "data": data}

    def get_form_class(self):
        return django_comments.get_form()

    def form_invalid(self, form):
        return CommentPostBadRequest(
            "The comment form failed verification: %s" % escape(str(form.errors))
        )

    def form_valid(self, form):
        request = self.request

        comment = form.get_comment_object(site_id=get_current_site(request).id)
        comment.ip_address = request.META.get("REMOTE_ADDR", None) or None
        comment.user = request.user

        responses = signals.comment_will_be_posted.send(
            sender=comment.__class__, comment=comment, request=request
        )

        for receiver, response in responses:
            if response is False:
                return CommentPostBadRequest(
                    "comment_will_be_posted receiver %r killed the comment"
                    % receiver.__name__
                )

        comment.save()
        signals.comment_was_posted.send(
            sender=comment.__class__, comment=comment, request=request
        )

        context = self.get_context_data(comment=comment, form=form)
        return self.render_to_response(context)

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @inject_comment_target
    def post(self, request, **kwargs):
        form = self.get_form()

        if form.security_errors():
            return CommentPostBadRequest(
                "The comment form failed security verification: %s"
                % escape(str(form.security_errors()))
            )

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
