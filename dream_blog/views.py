from core.views import SetHeadlineMixin
from django.views.generic import ListView
from posts.models import Post


class HomeView(SetHeadlineMixin, ListView):
    template_name = "pages/home.html"
    context_object_name = "posts"
    headline = "追梦人物的博客"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.visible().with_comment_count().order_by("-publish_date")
