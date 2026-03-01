import pytest
from django.urls import reverse
from django.utils import timezone

from dream_blog.favorites.models import Favorite, Issue


@pytest.mark.django_db
class TestIssueListView:
    def test_view_resolves(self, client):
        url = reverse("favorites:issue_list")
        response = client.get(url)
        assert response.status_code == 200

    def test_view_uses_correct_template(self, client):
        url = reverse("favorites:issue_list")
        response = client.get(url)
        assert "favorites/issue_list.html" in [t.name for t in response.templates if t.name]

    def test_view_displays_issues(self, client):
        Issue.objects.create(
            number=1,
            pub_date=timezone.now(),
            description="Test issue",
        )
        url = reverse("favorites:issue_list")
        response = client.get(url)
        content = response.content.decode()
        assert "Issue #1" in content


@pytest.mark.django_db
class TestIssueDetailView:
    def test_view_resolves(self, client):
        Issue.objects.create(
            number=1,
            pub_date=timezone.now(),
            description="Test issue",
        )
        url = reverse("favorites:issue_detail", kwargs={"number": 1})
        response = client.get(url)
        assert response.status_code == 200

    def test_view_displays_favorites(self, client):
        issue = Issue.objects.create(
            number=1,
            pub_date=timezone.now(),
            description="Test issue",
        )
        Favorite.objects.create(
            issue=issue,
            title="Test Favorite",
            url="https://example.com",
            rank=1,
        )
        url = reverse("favorites:issue_detail", kwargs={"number": 1})
        response = client.get(url)
        content = response.content.decode()
        assert "Test Favorite" in content
