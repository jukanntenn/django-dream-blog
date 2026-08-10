from unittest.mock import MagicMock

import pytest
from django.http import QueryDict

from dream_blog.core.templatetags.core_extra import querystring, show_profile


@pytest.mark.django_db
class TestShowProfile:
    def test_returns_profile_context(self):
        result = show_profile()
        assert "profile" in result
        assert "blogger" in result["profile"]
        assert "slogan" in result["profile"]
        assert "social_links" in result["profile"]
        assert len(result["profile"]["social_links"]) == 5


class TestQuerystring:
    def test_returns_empty_without_request(self):
        context = {}
        result = querystring(context)
        assert result == ""

    def test_returns_querystring_from_request(self):
        request = MagicMock()
        request.GET = QueryDict("page=2&q=test")
        context = {"request": request}
        result = querystring(context)
        assert "page=2" in result
        assert "q=test" in result
        assert result.startswith("?")

    def test_removes_key_when_value_is_none(self):
        request = MagicMock()
        request.GET = QueryDict("page=2&q=test")
        context = {"request": request}
        result = querystring(context, q=None)
        assert "page=2" in result
        assert "q=" not in result

    def test_removes_key_when_value_is_empty(self):
        request = MagicMock()
        request.GET = QueryDict("page=2&q=test")
        context = {"request": request}
        result = querystring(context, q="")
        assert "page=2" in result
        assert "q=" not in result

    def test_adds_new_key(self):
        request = MagicMock()
        request.GET = QueryDict("page=2")
        context = {"request": request}
        result = querystring(context, sort="date")
        assert "page=2" in result
        assert "sort=date" in result

    def test_returns_question_mark_for_empty_query(self):
        request = MagicMock()
        request.GET = QueryDict("")
        context = {"request": request}
        result = querystring(context)
        assert result == "?"
