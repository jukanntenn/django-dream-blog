import pytest

pytestmark = pytest.mark.django_db


class TestCategory:
    def test_str(self, tutorial_category):
        assert str(tutorial_category) == tutorial_category.name


class TestTutorial:
    def test_str(self, tutorial):
        assert str(tutorial) == tutorial.title

    def test_get_absolute_url(self, tutorial):
        assert tutorial.get_absolute_url() == f"/tutorials/{tutorial.slug}/"


class TestMaterial:
    def test_str(self, material):
        assert str(material) == material.title

    def test_get_absolute_url(self, material):
        assert (
            material.get_absolute_url()
            == f"/tutorials/{material.tutorial.slug}/materials/{material.pk}/"
        )

    def test_hits_property(self, material):
        assert material.hits == 0
