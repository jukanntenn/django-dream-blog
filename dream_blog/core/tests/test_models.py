from datetime import timedelta

import pytest
from core.tests.models import Entry, RankableEntry
from django.utils import timezone

pytestmark = pytest.mark.django_db


@pytest.fixture
def entry():
    return Entry.objects.create(content="# 标题内容")


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


def test_get_next_or_previous_without_default_ordering():
    now = timezone.now()
    entry1 = Entry.objects.create(publish_date=now)
    entry2 = Entry.objects.create(publish_date=now - timedelta(days=1))
    entry3 = Entry.objects.create(publish_date=now)

    # ordering by pk
    assert entry1.get_next_or_previous(is_next=False) is None
    assert entry1.get_next_or_previous(is_next=True) == entry2

    assert entry2.get_next_or_previous(is_next=False) == entry1
    assert entry2.get_next_or_previous(is_next=True) == entry3

    assert entry3.get_next_or_previous(is_next=False) == entry2
    assert entry3.get_next_or_previous(is_next=True) is None

    # ordering by publish_date
    assert (
        entry1.get_next_or_previous(is_next=False, ordering=["-publish_date"]) is None
    )
    assert (
        entry1.get_next_or_previous(is_next=True, ordering=["-publish_date"]) == entry3
    )

    assert (
        entry2.get_next_or_previous(is_next=False, ordering=["-publish_date"]) == entry3
    )
    assert entry2.get_next_or_previous(is_next=True, ordering=["-publish_date"]) is None

    assert (
        entry3.get_next_or_previous(is_next=False, ordering=["-publish_date"]) == entry1
    )
    assert (
        entry3.get_next_or_previous(is_next=True, ordering=["-publish_date"]) == entry2
    )


def test_get_next_or_previous_with_default_ordering():
    now = timezone.now()
    entry1 = RankableEntry.objects.create(rank=3, publish_date=now)
    entry2 = RankableEntry.objects.create(rank=2, publish_date=now - timedelta(days=1))
    entry3 = RankableEntry.objects.create(rank=1, publish_date=now)

    assert entry1.get_next_or_previous(is_next=False) == entry2
    assert entry1.get_next_or_previous(is_next=True) is None

    assert entry2.get_next_or_previous(is_next=False) == entry3
    assert entry2.get_next_or_previous(is_next=True) == entry1

    assert entry3.get_next_or_previous(is_next=False) is None
    assert entry3.get_next_or_previous(is_next=True) == entry2

    # extra kwargs
    assert (
        entry2.get_next_or_previous(is_next=False, value_fields=["rank"], rank__gt=2)
        is None
    )
    assert entry2.get_next_or_previous(
        is_next=True, value_fields=["rank"], rank__gt=2
    ) == {"rank": 3}


def test_get_next_or_previous_no_hidden():
    now = timezone.now()
    entry1 = RankableEntry.objects.create(rank=1, publish_date=now)
    RankableEntry.objects.create(rank=2)
    entry3 = RankableEntry.objects.create(rank=3, publish_date=now)

    assert entry1.get_next_or_previous(is_next=True) == entry3
    assert entry3.get_next_or_previous(is_next=False) == entry1
