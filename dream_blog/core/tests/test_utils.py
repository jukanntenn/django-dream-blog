from core.utils import markdownify


def test_markdownify():
    value = "~~del~~"
    result = markdownify(value)
    assert result["content"] == "<p><del>del</del></p>"
    assert result["toc"] == ""

    value = "# 标题"
    result = markdownify(value)
    assert result["content"] == '<h1 id="标题">标题</h1>'
    assert result["toc"] == '<li><a href="#标题">标题</a></li>'

    value = "# header"
    result = markdownify(value, toc_url="/absolute/")
    assert result["toc"] == '<li><a href="/absolute/#header">header</a></li>'
