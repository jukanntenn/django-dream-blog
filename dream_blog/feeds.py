from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.html import strip_tags
from django.utils.text import Truncator

from posts.models import Post


class RssFeed(Feed):
    feed_type = Rss201rev2Feed
    title = "追梦人物的博客"
    link = "/"
    description = "一直走在追梦的路上"

    def items(self):
        return Post.objects.visible().order_by("-publish_date")[:100]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if getattr(item, "excerpt", ""):
            return item.excerpt
        return Truncator(strip_tags(item.content_html)).chars(200)

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.publish_date

    def item_updateddate(self, item):
        return item.modified_at
