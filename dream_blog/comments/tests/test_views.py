import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from dream_blog.comments.forms import TreeCommentForm
from dream_blog.posts.tests.factories import PostFactory

pytestmark = pytest.mark.django_db


class TestCommentFormTemplateView:
    @pytest.fixture
    def post(self, user):
        return PostFactory(author=user)

    def test_get_returns_form(self, client, post):
        ct = ContentType.objects.get_for_model(post)
        url = reverse("comments:form")
        response = client.get(url, {"content_type": f"{ct.app_label}.{ct.model}", "object_pk": post.pk})
        assert response.status_code == 200

    def test_get_missing_content_type(self, client):
        url = reverse("comments:form")
        response = client.get(url, {"object_pk": 1})
        assert response.status_code == 400

    def test_get_missing_object_pk(self, client, post):
        ct = ContentType.objects.get_for_model(post)
        url = reverse("comments:form")
        response = client.get(url, {"content_type": f"{ct.app_label}.{ct.model}"})
        assert response.status_code == 400

    def test_get_invalid_content_type_format(self, client):
        url = reverse("comments:form")
        response = client.get(url, {"content_type": "invalid", "object_pk": 1})
        assert response.status_code == 400

    def test_get_nonexistent_model(self, client):
        url = reverse("comments:form")
        response = client.get(url, {"content_type": "nonexistent.model", "object_pk": 1})
        assert response.status_code == 400

    def test_get_nonexistent_object(self, client, post):
        ct = ContentType.objects.get_for_model(post)
        url = reverse("comments:form")
        response = client.get(url, {"content_type": f"{ct.app_label}.{ct.model}", "object_pk": 99999})
        assert response.status_code == 400


def _get_security_data(target_object):
    """Helper to generate valid security data for a target object."""
    form = TreeCommentForm(target_object)
    return form.generate_security_data()


class TestCommentPostView:
    @pytest.fixture
    def post(self, user):
        return PostFactory(author=user)

    def test_post_requires_login(self, client, post):
        ct = ContentType.objects.get_for_model(post)
        url = reverse("comments:post")
        response = client.post(url, {"content_type": f"{ct.app_label}.{ct.model}", "object_pk": post.pk})
        assert response.status_code == 302

    def test_post_missing_content_type(self, client, user):
        client.force_login(user)
        url = reverse("comments:post")
        response = client.post(url, {"object_pk": 1})
        assert response.status_code == 400

    def test_post_missing_object_pk(self, client, user, post):
        client.force_login(user)
        ct = ContentType.objects.get_for_model(post)
        url = reverse("comments:post")
        response = client.post(url, {"content_type": f"{ct.app_label}.{ct.model}"})
        assert response.status_code == 400

    def test_post_invalid_content_type(self, client, user):
        client.force_login(user)
        url = reverse("comments:post")
        response = client.post(url, {"content_type": "invalid", "object_pk": 1})
        assert response.status_code == 400

    def test_post_nonexistent_model(self, client, user):
        client.force_login(user)
        url = reverse("comments:post")
        response = client.post(url, {"content_type": "nonexistent.model", "object_pk": 1})
        assert response.status_code == 400

    def test_post_nonexistent_object(self, client, user, post):
        client.force_login(user)
        ct = ContentType.objects.get_for_model(post)
        url = reverse("comments:post")
        response = client.post(url, {"content_type": f"{ct.app_label}.{ct.model}", "object_pk": 99999})
        assert response.status_code == 400

    def test_post_valid_comment(self, client, user, post):
        client.force_login(user)
        security_data = _get_security_data(post)
        url = reverse("comments:post")
        data = {
            **security_data,
            "comment": "Test comment content",
            "name": "Test User",
            "email": "test@example.com",
        }
        response = client.post(url, data)
        assert response.status_code == 200

    def test_post_uses_user_name_when_empty(self, client, user, post):
        client.force_login(user)
        security_data = _get_security_data(post)
        url = reverse("comments:post")
        data = {
            **security_data,
            "comment": "Test comment content",
            "name": "",
            "email": "",
        }
        response = client.post(url, data)
        assert response.status_code == 200

    def test_post_security_errors(self, client, user, post):
        client.force_login(user)
        ct = ContentType.objects.get_for_model(post)
        url = reverse("comments:post")
        data = {
            "content_type": f"{ct.app_label}.{ct.model}",
            "object_pk": post.pk,
            "comment": "Test comment",
            "timestamp": "invalid",
            "security_hash": "invalid",
        }
        response = client.post(url, data)
        assert response.status_code == 400

    def test_post_invalid_form(self, client, user, post):
        """Test with valid security but missing comment."""
        client.force_login(user)
        security_data = _get_security_data(post)
        url = reverse("comments:post")
        data = {
            **security_data,
            "comment": "",  # empty comment
        }
        response = client.post(url, data)
        assert response.status_code == 400
