import pytest
from posts.tests.factories import PostFactory
from test_plus.plugin import TestCase

pytestmark = pytest.mark.django_db


def test_sitemap_is_good(tp: TestCase):
    response = tp.get_check_200("sitemap")
    assert response["Content-Type"].startswith(("application/xml", "text/xml"))
    assert b"<urlset" in response.content


def test_posts_rss_feed_is_good(tp: TestCase):
    post = PostFactory(title="Test RSS Title")
    response = tp.get_check_200("rss")
    assert response["Content-Type"].startswith(("application/rss+xml", "application/xml"))
    assert b"<rss" in response.content
    assert post.title.encode() in response.content
