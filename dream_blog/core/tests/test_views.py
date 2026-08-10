import pytest
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView

from dream_blog.core.views import SetHeadlineMixin


class TestSetHeadlineMixin:
    def test_raises_when_headline_not_set(self):
        class MyView(SetHeadlineMixin, TemplateView):
            template_name = "base.html"

        view = MyView()
        view.kwargs = {}
        with pytest.raises(ImproperlyConfigured):
            view.get_headline()

    def test_returns_headline_string(self):
        class MyView(SetHeadlineMixin, TemplateView):
            template_name = "base.html"
            headline = "Test Headline"

        view = MyView()
        assert view.get_headline() == "Test Headline"
