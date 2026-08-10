from constance import config
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import CreateView, View
from django_ratelimit.decorators import ratelimit

from dream_blog.core.utils import EmailConfirmation
from dream_blog.favorites.models import Issue

from .forms import SubscriptionForm


@method_decorator(ratelimit(key="ip", rate="3/h", method="POST", block=False), name="post")
class SubscriptionCreateView(CreateView):
    form_class = SubscriptionForm
    template_name = "newsletters/subscription.html"
    success_url = reverse_lazy("newsletters:subscription")

    def post(self, request, *args, **kwargs):
        if getattr(request, "limited", False):
            messages.error(request, _("Too many attempts. Please try again later."), extra_tags="danger")
            return redirect("newsletters:subscription")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        confirmation = EmailConfirmation(instance=self.object)

        subject = config.NEWSLETTERS_SUBSCRIPTION_CONFIRMATION_SUBJECT
        confirm_url = self.request.build_absolute_uri(
            reverse(
                "newsletters:subscription-confirm",
                kwargs={"key": confirmation.make_key()},
            )
        )
        html_message = render_to_string(
            "newsletters/subscription_confirmation_email.html",
            context={"link": confirm_url, "expire_days": config.EMAIL_CONFIRMATION_EXPIRE_DAYS},
        )
        plain_message = _("Please open the confirmation link: %(link)s") % {"link": confirm_url}

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=None,
            recipient_list=[self.object.email if self.object else ""],
            fail_silently=True,
        )

        messages.success(
            self.request,
            _("感谢订阅每周精选收藏，确认邮件已发至您的订阅邮箱，请及时前往确认。"),
        )
        return response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue = Issue.objects.order_by("-number").first()
        if issue:
            context["issue"] = issue
            context["favorite_list"] = list(issue.favorites.order_by("rank")[:5])
        context["page_title"] = "订阅每周精选收藏"
        return context


class SubscriptionConfirmView(View):
    def get(self, request, *args, **kwargs):
        confirmation = EmailConfirmation.from_key(kwargs["key"])

        if confirmation is None:
            messages.error(request, _("订阅链接已失效，请重新订阅。"), extra_tags="danger")
            return redirect("newsletters:subscription")

        if confirmation.instance.confirmed:
            messages.warning(request, _("订阅邮箱已确认，无需重复确认。"))
        else:
            confirmation.instance.confirm()
            messages.success(request, _("订阅成功！"))

        return redirect("favorites:issue_list")
