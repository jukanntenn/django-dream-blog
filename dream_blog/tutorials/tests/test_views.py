from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from test_plus.plugin import TestCase
from tutorials.models import Material, Tutorial
from tutorials.tests.factories import MaterialFactory, TutorialFactory

pytestmark = pytest.mark.django_db


def test_tutorial_detail_view_is_good(tp: TestCase, tutorial: Tutorial):
    response = tp.get_check_200("tutorials:detail", slug=tutorial.slug)
    tp.assertTemplateUsed(response, "tutorials/detail.html")


def test_tutorial_detail_view_headline(tp: TestCase, tutorial: Tutorial):
    response = tp.get_check_200("tutorials:detail", slug=tutorial.slug)
    tp.assertContains(response, tutorial.title)


def test_can_not_see_invisible_tutorial(tp: TestCase):
    tutorial = TutorialFactory(hidden=True)
    response = tp.get("tutorials:detail", slug=tutorial.slug)
    tp.assert_http_404_not_found(response)


def test_material_detail_view_is_good(tp: TestCase, material: Material):
    response = tp.get_check_200(
        "tutorials:material_detail",
        slug=material.tutorial.slug,
        pk=material.pk,
    )
    tp.assertTemplateUsed(response, "tutorials/material_detail.html")


def test_material_detail_view_headline(tp: TestCase, material: Material):
    response = tp.get_check_200(
        "tutorials:material_detail",
        slug=material.tutorial.slug,
        pk=material.pk,
    )
    tp.assertContains(
        response,
        f"{material.title} - {material.tutorial.title}",
    )


def test_material_detail_view_hits(tp: TestCase, material: Material):
    assert material.hits == 0

    tp.get_check_200(
        "tutorials:material_detail",
        slug=material.tutorial.slug,
        pk=material.pk,
    )
    material.refresh_from_db()
    assert material.hits == 1

    with freeze_time(lambda: datetime.now() + timedelta(minutes=1)):
        tp.get_check_200(
            "tutorials:material_detail",
            slug=material.tutorial.slug,
            pk=material.pk,
        )

    material.refresh_from_db()
    assert material.hits == 2


def test_can_not_see_invisible_material(tp: TestCase):
    hidden_tutorial = TutorialFactory(hidden=True)
    material = MaterialFactory(tutorial=hidden_tutorial)
    response = tp.get(
        "tutorials:material_detail", slug=hidden_tutorial.slug, pk=material.pk
    )
    tp.assert_http_404_not_found(response)

    tutorial = TutorialFactory(hidden=False)
    hidden_material = MaterialFactory(tutorial=hidden_tutorial, hidden=True)
    response = tp.get(
        "tutorials:material_detail", slug=tutorial.slug, pk=hidden_material.pk
    )
    tp.assert_http_404_not_found(response)
