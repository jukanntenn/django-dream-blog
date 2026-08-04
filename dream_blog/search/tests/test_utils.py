from django.utils.html import strip_tags
from search.utils import Highlighter


class TestHighlighter:
    def test_highlighter_chinese_tokenization(self):
        highlighter = Highlighter("中文测试")
        assert highlighter.query_words

    def test_highlighter_short_text_not_truncated(self):
        highlighter = Highlighter("测试", max_length=200)
        short_text = "这是一个简短的标题"
        result = highlighter.highlight(short_text)
        assert strip_tags(result) == short_text

    def test_highlighter_long_text_truncated(self):
        highlighter = Highlighter("测试", max_length=50)
        long_text = "这是一段很长的文本内容" * 20
        result = highlighter.highlight(long_text)
        assert len(strip_tags(result)) <= 60
