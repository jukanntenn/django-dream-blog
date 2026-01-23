from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.urls import reverse

from core.entries import get_index_queryset


class RssFeed(Feed):
    feed_type = Rss201rev2Feed
    title = "追梦人物的博客"
    link = "/"
    description = "一直走在追梦的路上"

    def items(self):
        return get_index_queryset()[:100]

    def item_title(self, item):
        return item['title']

    def item_description(self, item):
        return item.get('brief') or "查看详情"

    def item_link(self, item):
        """Generate URL based on entry type."""
        entry_type = item['type']
        pk = item['id']
        parent_slug = item.get('parent_slug')

        if entry_type == 'p':
            return reverse('posts:detail', kwargs={'pk': pk})
        if entry_type == 'a':
            return reverse('columns:article_detail', kwargs={'slug': parent_slug, 'pk': pk})
        if entry_type == 'm':
            return reverse('tutorials:material_detail', kwargs={'slug': parent_slug, 'pk': pk})
        return '/'

    def item_pubdate(self, item):
        return item['pub_date']

    item_updateddate = item_pubdate
