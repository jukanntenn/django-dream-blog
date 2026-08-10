from django.views.generic import TemplateView

from dream_blog.core.views import SetHeadlineMixin


class DonateView(SetHeadlineMixin, TemplateView):
    headline = "赞助"
    template_name = "donate/donate.html"
