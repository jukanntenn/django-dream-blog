from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from dream_blog.core.entries import get_index_queryset
from dream_blog.core.views import SetHeadlineMixin
from dream_blog.posts.models import Post


class PostDetailView(SetHeadlineMixin, HitCountDetailView):
    model = Post
    count_hit = True
    template_name = "posts/detail.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return Post.objects.visible().with_comment_count()

    def get_headline(self):
        return f"{self.object.title} - 追梦人物的博客"


class ArchivesView(SetHeadlineMixin, ListView):
    template_name = "posts/archives.html"
    context_object_name = "entries"
    headline = "归档"

    def get_queryset(self):
        return get_index_queryset()
