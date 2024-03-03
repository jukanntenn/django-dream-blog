from columns.models import Article, Column
from core.views import SetHeadlineMixin
from hitcount.views import HitCountDetailView


class ColumnDetailView(SetHeadlineMixin, HitCountDetailView):
    model = Column
    count_hit = True
    template_name = "columns/detail.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = self.object.article_set.visible().order_by("-publish_date")
        context["articles"] = articles
        return context

    def get_queryset(self):
        return Column.objects.visible().order_by("-created_at")

    def get_headline(self):
        return self.object.title


class ArticleDetailView(SetHeadlineMixin, HitCountDetailView):
    model = Article
    count_hit = True
    template_name = "columns/article_detail.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return (
            Article.objects.visible()
            .select_related("column")
            .order_by("-publish_date")
            .with_comment_count()
        )

    def get_headline(self):
        return f"{self.object.title} - {self.object.column.title}"
