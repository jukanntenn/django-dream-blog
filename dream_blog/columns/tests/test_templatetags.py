import pytest
from columns.templatetags.columns_extra import show_column_toc, show_columns
from columns.tests.factories import ArticleFactory, ColumnFactory
from django.utils import timezone

pytestmark = pytest.mark.django_db


class TestShowColumns:
    def test_returns_visible_columns(self, user):
        ColumnFactory(author=user)
        ColumnFactory(author=user)
        result = show_columns(num=5)
        assert len(result["columns"]) == 2

    def test_limits_columns(self, user):
        for _ in range(5):
            ColumnFactory(author=user)
        result = show_columns(num=3)
        assert len(result["columns"]) == 3

    def test_excludes_hidden_columns(self, user):
        ColumnFactory(author=user)
        ColumnFactory(author=user, hidden=True)
        result = show_columns(num=5)
        assert len(result["columns"]) == 1


class TestShowColumnToc:
    def test_returns_column_articles(self, user):
        column = ColumnFactory(author=user)
        article = ArticleFactory(column=column, publish_date=timezone.now())
        result = show_column_toc(column)
        assert result["column"] == column
        assert result["current"] is None
        articles = list(result["articles"])
        assert len(articles) == 1
        assert articles[0]["id"] == article.pk
        assert articles[0]["title"] == article.title

    def test_with_current_article(self, user):
        column = ColumnFactory(author=user)
        article = ArticleFactory(column=column, publish_date=timezone.now())
        result = show_column_toc(column, current=article.pk)
        assert result["current"] == article.pk

    def test_excludes_hidden_articles(self, user):
        column = ColumnFactory(author=user)
        ArticleFactory(column=column, publish_date=timezone.now())
        ArticleFactory(column=column, hidden=True, publish_date=timezone.now())
        result = show_column_toc(column)
        assert len(list(result["articles"])) == 1
