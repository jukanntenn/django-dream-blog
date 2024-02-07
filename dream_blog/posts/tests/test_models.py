import pytest
from posts.models import Post

pytestmark = pytest.mark.django_db


class TestPost:
    def test_str(self, post: Post):
        assert str(post) == post.title

    def test_get_absolute_url(self, post: Post):
        assert post.get_absolute_url() == f"/posts/{post.pk}/"

    def test_hits_property(self, post: Post):
        assert post.hits == 0
