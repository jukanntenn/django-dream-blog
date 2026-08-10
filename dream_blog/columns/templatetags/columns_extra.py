from django import template

from dream_blog.columns.models import Column

register = template.Library()


@register.inclusion_tag("columns/inclusions/_columns.html")
def show_columns(num=5):
    columns = Column.objects.visible().order_by("-created_at")[:num]
    return {
        "columns": columns,
    }


@register.inclusion_tag("columns/inclusions/_toc.html")
def show_column_toc(column, current=None):
    articles = column.article_set.visible().order_by("-publish_date").values("id", "title")

    return {
        "column": column,
        "articles": articles,
        "current": current,
    }
