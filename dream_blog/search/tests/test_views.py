from datetime import timedelta

import pytest
from django.test import Client
from django.utils import timezone
from django.utils.html import strip_tags
from posts.models import Post
from posts.tests.factories import PostFactory

pytestmark = pytest.mark.django_db(transaction=True)


class TestSearchView:
    @pytest.fixture
    def client(self):
        return Client()

    def test_search_view_requires_query(self, client):
        response = client.get("/search/")
        assert response.status_code == 200
        assert "请输入搜索关键词" in response.content.decode()

    def test_search_view_returns_results(self, client, settings, tmp_path, user):
        settings.HAYSTACK_CONNECTIONS = {
            "default": {
                "ENGINE": "search.backends.whoosh_cn_backend.WhooshJiebaEngine",
                "PATH": str(tmp_path / "whoosh"),
            }
        }
        settings.HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.BaseSignalProcessor"

        from haystack import connections

        connections.connections_info = settings.HAYSTACK_CONNECTIONS
        connections.reload("default")

        post = PostFactory(
            author=user,
            title="中文测试文章",
            publish_date=timezone.now() - timedelta(days=1),
        )
        backend = connections["default"].get_backend()
        unified_index = connections["default"].get_unified_index()
        backend.clear()
        backend.update(unified_index.get_index(post.__class__), [post])

        response = client.get("/search/", {"q": "中文"})
        assert response.status_code == 200
        content = response.content.decode()
        assert post.title in strip_tags(content)

    def test_search_view_pagination_preserves_querystring(self, client, settings, tmp_path, user):
        settings.HAYSTACK_CONNECTIONS = {
            "default": {
                "ENGINE": "search.backends.whoosh_cn_backend.WhooshJiebaEngine",
                "PATH": str(tmp_path / "whoosh"),
            }
        }
        settings.HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.BaseSignalProcessor"

        from haystack import connections

        connections.connections_info = settings.HAYSTACK_CONNECTIONS
        connections.reload("default")

        for i in range(25):
            PostFactory(
                author=user,
                title=f"Test Post {i}",
                publish_date=timezone.now() - timedelta(days=1),
            )
        backend = connections["default"].get_backend()
        unified_index = connections["default"].get_unified_index()
        backend.clear()
        backend.update(unified_index.get_index(Post), Post.objects.all())

        response = client.get("/search/", {"q": "Test"})
        assert response.status_code == 200
        content = response.content.decode()
        assert "?q=Test&amp;page=2" in content
