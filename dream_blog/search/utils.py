from django.utils.html import strip_tags
from haystack.utils import Highlighter as HaystackHighlighter
from jieba.analyse.analyzer import ChineseTokenizer


def _token_text(token) -> str:
    return (getattr(token, "text", None) or getattr(token, "word", None) or str(token)).strip()


class Highlighter(HaystackHighlighter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tokenizer = ChineseTokenizer()
        self.query_words = {_token_text(token) for token in tokenizer(self.query)}
        self.query_words.discard("")

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        if len(self.text_block) < self.max_length:
            start_offset = 0
        return self.render_html(highlight_locations, start_offset, end_offset)
