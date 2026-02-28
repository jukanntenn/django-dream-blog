from datetime import timedelta

import pytest
from django.utils import timezone

from columns.models import Article, Column

pytestmark = pytest.mark.django_db


class TestArticlePrevNext:
    def test_article_prev_next_within_column(self, user):
        now = timezone.now()

        column1 = Column.objects.create(
            title="Column 1",
            slug="col-1",
            excerpt="Test column 1",
            content="Test column 1",
            author=user,
        )
        column2 = Column.objects.create(
            title="Column 2",
            slug="col-2",
            excerpt="Test column 2",
            content="Test column 2",
            author=user,
        )

        article1 = Article.objects.create(
            column=column1,
            title="Article 1",
            content="Content 1",
            publish_date=now - timedelta(days=2),
        )
        article2 = Article.objects.create(
            column=column1,
            title="Article 2",
            content="Content 2",
            publish_date=now - timedelta(days=1),
        )
        article3 = Article.objects.create(
            column=column2,
            title="Article 3",
            content="Content 3",
            publish_date=now,
        )

        assert article1.next == article2
        assert article2.prev == article1
        assert article2.next is None
        assert article3.prev is None

    def test_article_prev_next_with_hidden_articles(self, user):
        now = timezone.now()

        column = Column.objects.create(
            title="Test Column",
            slug="test-col",
            excerpt="Test column",
            content="Test column",
            author=user,
        )

        article1 = Article.objects.create(
            column=column,
            title="Article 1",
            content="Content 1",
            publish_date=now - timedelta(days=2),
        )
        Article.objects.create(
            column=column,
            title="Article 2",
            content="Content 2",
            publish_date=now - timedelta(days=1),
            hidden=True,
        )
        article3 = Article.objects.create(
            column=column,
            title="Article 3",
            content="Content 3",
            publish_date=now,
        )

        assert article1.next == article3
        assert article3.prev == article1
