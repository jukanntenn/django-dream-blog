from core.views import SetHeadlineMixin
from django.views.generic import ListView
from posts.models import Post


class HomeView(SetHeadlineMixin, ListView):
    template_name = "pages/home.html"
    context_object_name = "posts"
    headline = "追梦人物的博客"
    paginate_by = 20
    paginate_orphans = 3

    def get_queryset(self):
        return Post.objects.visible().with_comment_count().order_by("-publish_date")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        paginator = context_data["paginator"]
        page_obj = context_data["page_obj"]
        elided_page_range = paginator.get_elided_page_range(
            page_obj.number,
            on_each_side=2,
            on_ends=1,
        )
        context_data["elided_page_range"] = elided_page_range
        return context_data
