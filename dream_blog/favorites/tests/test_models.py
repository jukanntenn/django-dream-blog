import pytest
from django.utils import timezone

from dream_blog.favorites.models import Favorite, Issue


@pytest.mark.django_db
class TestIssue:
    def test_issue_creation(self):
        issue = Issue.objects.create(
            number=1,
            pub_date=timezone.now(),
            description="First issue",
        )
        assert str(issue) == "Issue #1"
        assert issue.number == 1

    def test_issue_ordering(self):
        Issue.objects.create(number=1, pub_date=timezone.now(), description="First")
        Issue.objects.create(number=2, pub_date=timezone.now(), description="Second")
        issues = list(Issue.objects.all())
        assert issues[0].number == 2


@pytest.mark.django_db
class TestFavorite:
    def test_favorite_creation(self):
        issue = Issue.objects.create(number=1, pub_date=timezone.now(), description="First")
        favorite = Favorite.objects.create(
            issue=issue,
            title="Test Link",
            description="A test link",
            url="https://example.com",
            rank=1,
        )
        assert str(favorite) == "Test Link"
        assert favorite.rank == 1

    def test_favorite_ordering(self):
        issue = Issue.objects.create(number=1, pub_date=timezone.now(), description="First")
        Favorite.objects.create(issue=issue, title="First", url="https://1.com", rank=2)
        Favorite.objects.create(issue=issue, title="Second", url="https://2.com", rank=1)
        favorites = list(issue.favorites.all())
        assert favorites[0].rank == 1
