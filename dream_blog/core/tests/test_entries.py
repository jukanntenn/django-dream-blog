from dream_blog.core.entries import IndexEntry


class TestIndexEntry:
    def test_get_absolute_url_post(self):
        entry = IndexEntry(
            id=1,
            title="Test",
            brief="",
            views=0,
            parent_slug=None,
            parent_title=None,
            comment_count=0,
            pub_date="2024-01-01",
            type="p",
        )
        assert entry.get_absolute_url() == "/posts/1/"

    def test_get_absolute_url_article(self):
        entry = IndexEntry(
            id=1,
            title="Test",
            brief="",
            views=0,
            parent_slug="my-column",
            parent_title="Column",
            comment_count=0,
            pub_date="2024-01-01",
            type="a",
        )
        assert entry.get_absolute_url() == "/columns/my-column/articles/1/"

    def test_get_absolute_url_material(self):
        entry = IndexEntry(
            id=1,
            title="Test",
            brief="",
            views=0,
            parent_slug="my-tutorial",
            parent_title="Tutorial",
            comment_count=0,
            pub_date="2024-01-01",
            type="m",
        )
        assert entry.get_absolute_url() == "/tutorials/my-tutorial/materials/1/"
