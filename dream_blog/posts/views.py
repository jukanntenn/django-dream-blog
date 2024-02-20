from core.views import SetHeadlineMixin
from hitcount.views import HitCountDetailView
from posts.models import Post


class PostDetailView(SetHeadlineMixin, HitCountDetailView):
    model = Post
    count_hit = True
    template_name = "posts/detail.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Post.objects.visible().with_comment_count()

    def get_headline(self):
        return f"{self.object.title} - 追梦人物的博客"
