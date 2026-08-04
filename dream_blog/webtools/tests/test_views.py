import pytest
from test_plus.plugin import TestCase

pytestmark = pytest.mark.django_db


def test_secret_key_form_view(tp: TestCase):
    response = tp.get_check_200("webtools:create_django_secret_key")
    tp.assertTemplateUsed(response, "webtools/django_secret_key.html")


def test_secret_key_form_valid_submission(tp: TestCase):
    response = tp.post("webtools:create_django_secret_key", data={"prefix": "test", "suffix": "end"})
    assert response.status_code == 200
    assert "django_secret_key" in response.context
