from columns.models import Article, Column
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from posts.models import Post
from tutorials.models import Material, Tutorial


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    lastmod = "modified_at"

    def items(self):
        return Post.objects.visible().order_by("-publish_date")


class TutorialSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    lastmod = "modified_at"

    def items(self):
        return Tutorial.objects.visible().order_by("-created_at")


class MaterialSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    lastmod = "modified_at"

    def items(self):
        return Material.objects.visible().order_by("-publish_date")


class ColumnSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    lastmod = "modified_at"

    def items(self):
        return Column.objects.visible().order_by("-created_at")


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    lastmod = "modified_at"

    def items(self):
        return Article.objects.visible().order_by("-publish_date")


SITEMAPS = {
    "static": StaticViewSitemap,
    "posts": PostSitemap,
    "tutorials": TutorialSitemap,
    "materials": MaterialSitemap,
    "columns": ColumnSitemap,
    "articles": ArticleSitemap,
}
