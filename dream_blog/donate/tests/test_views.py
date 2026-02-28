import pytest
from test_plus.plugin import TestCase

pytestmark = pytest.mark.django_db


def test_donate_page_status(tp: TestCase):
    tp.get_check_200("/donate/")


def test_donate_page_template(tp: TestCase):
    response = tp.get_check_200("/donate/")
    tp.assertTemplateUsed(response, "donate/donate.html")


def test_donate_page_headline(tp: TestCase):
    response = tp.get_check_200("/donate/")
    assert response.context["headline"] == "赞助"
