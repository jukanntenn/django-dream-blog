from django.views.generic import DetailView, ListView

from .models import Issue


class IssueListView(ListView):
    model = Issue
    context_object_name = "issue_list"
    template_name = "favorites/issue_list.html"
    paginate_by = 15

    def get_queryset(self):
        return Issue.objects.prefetch_related("tags").order_by("-number")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "每周精选收藏"
        return context


class IssueDetailView(DetailView):
    model = Issue
    context_object_name = "issue"
    template_name = "favorites/issue_detail.html"
    slug_field = "number"
    slug_url_kwarg = "number"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorite_list"] = self.object.favorites.order_by("rank", "-created_at")
        context["page_title"] = f"第{self.object.number}周精选收藏"
        return context
