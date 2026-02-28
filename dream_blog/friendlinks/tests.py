import pytest
from friendlinks.models import FriendLink
from friendlinks.templatetags.friendlinks_extra import show_friendlinks

pytestmark = pytest.mark.django_db


class TestFriendLinkModel:
    """Test the FriendLink model."""

    def test_create_friendlink(self):
        """Test creating a friend link."""
        friendlink = FriendLink.objects.create(
            site_name="Test Site",
            site_link="https://example.com",
            rank=1,
        )
        assert friendlink.site_name == "Test Site"
        assert friendlink.site_link == "https://example.com"
        assert friendlink.rank == 1

    def test_str_representation(self):
        """Test the string representation of a friend link."""
        friendlink = FriendLink.objects.create(
            site_name="Test Site",
            site_link="https://example.com",
        )
        assert str(friendlink) == "Test Site"

    def test_default_rank(self):
        """Test that rank defaults to 0."""
        friendlink = FriendLink.objects.create(
            site_name="Test Site",
            site_link="https://example.com",
        )
        assert friendlink.rank == 0

    def test_ordering(self):
        """Test that friend links are ordered by rank and created_at."""
        FriendLink.objects.create(site_name="Site C", site_link="https://c.com", rank=3)
        FriendLink.objects.create(site_name="Site B", site_link="https://b.com", rank=2)
        FriendLink.objects.create(site_name="Site A", site_link="https://a.com", rank=1)
        FriendLink.objects.create(site_name="Site D", site_link="https://d.com", rank=1)

        qs = FriendLink.objects.all()
        assert qs[0].site_name == "Site A"  # rank 1, earlier created_at
        assert qs[1].site_name == "Site D"  # rank 1, later created_at
        assert qs[2].site_name == "Site B"  # rank 2
        assert qs[3].site_name == "Site C"  # rank 3


class TestShowFriendLinksTemplateTag:
    """Test the show_friendlinks template tag."""

    def test_default_num_parameter(self):
        """Test that default num=10 returns 10 friend links."""
        for i in range(15):
            FriendLink.objects.create(
                site_name=f"Site {i}",
                site_link=f"https://site{i}.com",
                rank=i,
            )

        context = show_friendlinks()
        assert len(context["friendlinks"]) == 10

    def test_custom_num_parameter(self):
        """Test that custom num parameter returns correct number of friend links."""
        for i in range(15):
            FriendLink.objects.create(
                site_name=f"Site {i}",
                site_link=f"https://site{i}.com",
                rank=i,
            )

        context = show_friendlinks(num=5)
        assert len(context["friendlinks"]) == 5

    def test_num_larger_than_total(self):
        """Test that num larger than total returns all friend links."""
        for i in range(15):
            FriendLink.objects.create(
                site_name=f"Site {i}",
                site_link=f"https://site{i}.com",
                rank=i,
            )

        context = show_friendlinks(num=100)
        assert len(context["friendlinks"]) == 15

    def test_returns_ordered_queryset(self):
        """Test that returned friend links are ordered by rank and created_at."""
        for i in range(15):
            FriendLink.objects.create(
                site_name=f"Site {i}",
                site_link=f"https://site{i}.com",
                rank=i,
            )

        context = show_friendlinks(num=5)
        friendlinks = context["friendlinks"]
        # Should be ordered by rank (0-4)
        for i, link in enumerate(friendlinks):
            assert link.rank == i
