import re
import warnings
from html.parser import HTMLParser

import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


class TOCHTMLParser(HTMLParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ul_cnt = 0
        self._ul_start_line = None
        self._ul_start_pos = None
        self._ul_end_line = None
        self._ul_end_pos = None
        self.html = ""

    def error(self, message):
        warnings.warn(message)

    def handle_starttag(self, tag, attrs):
        if tag == "ul":
            if self._ul_cnt == 0:
                self._ul_start_line, self._ul_start_pos = self.getpos()
            self._ul_cnt += 1

    def handle_endtag(self, tag):
        if tag == "ul":
            self._ul_cnt -= 1
            if self._ul_cnt == 0:
                self._ul_end_line, self._ul_end_pos = self.getpos()
                lines = self.rawdata.split("\n")
                lines = lines[self._ul_start_line - 1 : self._ul_end_line]
                lines[-1] = lines[-1][: self._ul_end_pos]
                lines[0] = lines[0][self._ul_start_pos + 4 :]
                self.html = "".join(lines)


def markdownify(value, *, toc_depth=3, toc_url=""):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.admonition",
            "markdown.extensions.nl2br",
            TocExtension(slugify=slugify, toc_depth=toc_depth),
            "pymdownx.extra",
            "pymdownx.magiclink",
            "pymdownx.tasklist",
            "pymdownx.tilde",
            "pymdownx.caret",
            "pymdownx.superfences",
            "pymdownx.tabbed",
            "pymdownx.highlight",
            "pymdownx.inlinehilite",
            "pymdownx.arithmatex",
        ],
        extension_configs={
            "pymdownx.highlight": {
                "linenums_style": "pymdownx-inline",
            },
            "pymdownx.arithmatex": {
                "generic": True,
            },
        },
    )
    content = md.convert(value)
    toc = md.toc

    # If there is no content, set `toc` to an empty string instead of wrapping it in a `div` tag.
    parser = TOCHTMLParser()
    parser.feed(toc)
    toc = parser.html

    if toc_url:

        def absolutify(matchobj):
            return 'href="{toc_url}{frag}"'.format(
                toc_url=toc_url, frag=matchobj.group(1)
            )

        toc = re.sub('href="(.+)"', absolutify, toc)
    return {"content": content, "toc": toc}
