from datetime import timedelta

import pytest
from columns.models import Article, Column
from django.utils import timezone
from posts.tests.factories import PostFactory
from search.search_indexes.article_index import ArticleIndex
from search.search_indexes.material_index import MaterialIndex
from search.search_indexes.post_index import PostIndex
from search.search_indexes.tutorial_index import TutorialIndex
from tutorials.models import Material, Tutorial
from tutorials.tests.factories import MaterialFactory, TutorialFactory

pytestmark = pytest.mark.django_db


class TestPostIndex:
    def test_index_model(self):
        assert PostIndex().get_model().__name__ == "Post"

    def test_index_queryset_filters_non_visible(self, user):
        visible_post = PostFactory(
            author=user,
            publish_date=timezone.now() - timedelta(days=1),
            hidden=False,
        )
        hidden_post = PostFactory(
            author=user,
            publish_date=timezone.now() - timedelta(days=1),
            hidden=True,
        )
        future_post = PostFactory(
            author=user,
            publish_date=timezone.now() + timedelta(days=1),
            hidden=False,
        )

        qs = PostIndex().index_queryset()
        assert visible_post in qs
        assert hidden_post not in qs
        assert future_post not in qs


class TestMaterialIndex:
    def test_index_model(self):
        assert MaterialIndex().get_model() is Material

    def test_index_queryset_filters_non_visible(self, user, tutorial_category):
        visible_tutorial = TutorialFactory(
            author=user,
            category=tutorial_category,
            hidden=False,
        )
        hidden_tutorial = TutorialFactory(
            author=user,
            category=tutorial_category,
            hidden=True,
        )

        visible_material = MaterialFactory(
            tutorial=visible_tutorial,
            publish_date=timezone.now() - timedelta(days=1),
            hidden=False,
        )
        hidden_material = MaterialFactory(
            tutorial=visible_tutorial,
            publish_date=timezone.now() - timedelta(days=1),
            hidden=True,
        )
        material_under_hidden_tutorial = MaterialFactory(
            tutorial=hidden_tutorial,
            publish_date=timezone.now() - timedelta(days=1),
            hidden=False,
        )

        qs = MaterialIndex().index_queryset()
        assert visible_material in qs
        assert hidden_material not in qs
        assert material_under_hidden_tutorial not in qs


class TestTutorialIndex:
    def test_index_model(self):
        assert TutorialIndex().get_model() is Tutorial

    def test_index_queryset_filters_hidden(self, user, tutorial_category):
        visible_tutorial = TutorialFactory(
            author=user,
            category=tutorial_category,
            hidden=False,
        )
        hidden_tutorial = TutorialFactory(
            author=user,
            category=tutorial_category,
            hidden=True,
        )

        qs = TutorialIndex().index_queryset()
        assert visible_tutorial in qs
        assert hidden_tutorial not in qs


class TestArticleIndex:
    def test_index_model(self):
        assert ArticleIndex().get_model() is Article

    def test_index_queryset_filters_non_visible(self, user):
        now = timezone.now()
        visible_column = Column.objects.create(
            title="Visible Column",
            slug="visible-col",
            excerpt="Excerpt",
            content="Content",
            author=user,
            hidden=False,
        )
        hidden_column = Column.objects.create(
            title="Hidden Column",
            slug="hidden-col",
            excerpt="Excerpt",
            content="Content",
            author=user,
            hidden=True,
        )

        visible_article = Article.objects.create(
            column=visible_column,
            title="Visible Article",
            content="Content",
            publish_date=now - timedelta(days=1),
            hidden=False,
        )
        hidden_article = Article.objects.create(
            column=visible_column,
            title="Hidden Article",
            content="Content",
            publish_date=now - timedelta(days=1),
            hidden=True,
        )
        future_article = Article.objects.create(
            column=visible_column,
            title="Future Article",
            content="Content",
            publish_date=now + timedelta(days=1),
            hidden=False,
        )
        article_under_hidden_column = Article.objects.create(
            column=hidden_column,
            title="Article Hidden Column",
            content="Content",
            publish_date=now - timedelta(days=1),
            hidden=False,
        )

        qs = ArticleIndex().index_queryset()
        assert visible_article in qs
        assert hidden_article not in qs
        assert future_article not in qs
        assert article_under_hidden_column not in qs
