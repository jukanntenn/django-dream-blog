from core.views import SetHeadlineMixin
from django.views.generic import TemplateView


class DonateView(SetHeadlineMixin, TemplateView):
    headline = "赞助"
    template_name = "donate/donate.html"
