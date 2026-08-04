import pytest
from columns.tests.factories import ArticleFactory, ColumnFactory
from django.utils import timezone
from test_plus.plugin import TestCase

pytestmark = pytest.mark.django_db


def test_column_detail_view(tp: TestCase, user):
    column = ColumnFactory(author=user)
    response = tp.get_check_200("columns:detail", slug=column.slug)
    tp.assertTemplateUsed(response, "columns/detail.html")


def test_column_detail_view_headline(tp: TestCase, user):
    column = ColumnFactory(author=user)
    response = tp.get_check_200("columns:detail", slug=column.slug)
    tp.assertContains(response, column.title)


def test_column_detail_view_context_articles(tp: TestCase, user):
    column = ColumnFactory(author=user)
    article = ArticleFactory(column=column, publish_date=timezone.now())
    response = tp.get_check_200("columns:detail", slug=column.slug)
    assert article in response.context["articles"]


def test_hidden_column_returns_404(tp: TestCase, user):
    column = ColumnFactory(author=user, hidden=True)
    response = tp.get("columns:detail", slug=column.slug)
    tp.assert_http_404_not_found(response)


def test_article_detail_view(tp: TestCase, user):
    column = ColumnFactory(author=user)
    article = ArticleFactory(column=column, publish_date=timezone.now())
    response = tp.get_check_200("columns:article_detail", slug=column.slug, pk=article.pk)
    tp.assertTemplateUsed(response, "columns/article_detail.html")


def test_article_detail_view_headline(tp: TestCase, user):
    column = ColumnFactory(author=user)
    article = ArticleFactory(column=column, publish_date=timezone.now())
    response = tp.get_check_200("columns:article_detail", slug=column.slug, pk=article.pk)
    expected = f"{article.title} - {column.title}"
    tp.assertContains(response, expected)


def test_hidden_article_returns_404(tp: TestCase, user):
    column = ColumnFactory(author=user)
    article = ArticleFactory(column=column, hidden=True, publish_date=timezone.now())
    response = tp.get("columns:article_detail", slug=column.slug, pk=article.pk)
    tp.assert_http_404_not_found(response)


def test_article_in_hidden_column_returns_404(tp: TestCase, user):
    column = ColumnFactory(author=user, hidden=True)
    article = ArticleFactory(column=column, publish_date=timezone.now())
    response = tp.get("columns:article_detail", slug=column.slug, pk=article.pk)
    tp.assert_http_404_not_found(response)
