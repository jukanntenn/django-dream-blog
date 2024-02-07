from datetime import timedelta

import pytest
from core.tests.models import Entry
from django.utils import timezone

pytestmark = pytest.mark.django_db


@pytest.fixture
def entry():
    return Entry.objects.create(content="# 标题内容")


def test_rich_content_model_properties(entry: Entry):
    assert isinstance(entry.markdownified, dict)
    assert "content" in entry.markdownified
    assert "toc" in entry.markdownified

    assert entry.content_html == entry.markdownified["content"]
    assert entry.toc == entry.markdownified["toc"]


class TestEntryQuerySet:
    def setup_method(self):
        Entry.objects.create(
            publish_date=None,
        )
        Entry.objects.create(
            publish_date=timezone.now() + timedelta(days=1),
        )

    def test_pulished(self):
        hidden_entry = Entry.objects.create(
            publish_date=timezone.now() - timedelta(days=1),
            hidden=True,
        )

        assert Entry.objects.count() == 3
        assert Entry.objects.published().get().pk == hidden_entry.pk

    def test_visible(self):
        visible_entry = Entry.objects.create(
            publish_date=timezone.now() - timedelta(days=1),
            hidden=False,
        )

        assert Entry.objects.count() == 3
        assert Entry.objects.visible().count() == 1
        assert Entry.objects.visible().get().pk == visible_entry.pk
