import pytest
from feeds import RssFeed


class TestRssFeed:
    @pytest.fixture
    def feed(self):
        return RssFeed()

    def test_title(self, feed):
        assert feed.title == "追梦人物的博客"

    def test_link(self, feed):
        assert feed.link == "/"

    def test_description(self, feed):
        assert feed.description == "一直走在追梦的路上"

    def test_item_title(self, feed):
        item = {"title": "Test Title"}
        assert feed.item_title(item) == "Test Title"

    def test_item_description_with_brief(self, feed):
        item = {"brief": "Test brief"}
        assert feed.item_description(item) == "Test brief"

    def test_item_description_without_brief(self, feed):
        item = {"brief": None}
        assert feed.item_description(item) == "查看详情"

    def test_item_link_post(self, feed):
        item = {"type": "p", "id": 1}
        assert feed.item_link(item) == "/posts/1/"

    def test_item_link_article(self, feed):
        item = {"type": "a", "id": 1, "parent_slug": "my-column"}
        assert feed.item_link(item) == "/columns/my-column/articles/1/"

    def test_item_link_material(self, feed):
        item = {"type": "m", "id": 1, "parent_slug": "my-tutorial"}
        assert feed.item_link(item) == "/tutorials/my-tutorial/materials/1/"

    def test_item_link_unknown_type(self, feed):
        item = {"type": "x", "id": 1}
        assert feed.item_link(item) == "/"

    def test_item_pubdate(self, feed):
        item = {"pub_date": "2024-01-01"}
        assert feed.item_pubdate(item) == "2024-01-01"
