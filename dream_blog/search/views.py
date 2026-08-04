from columns.models import Article
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import TemplateView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from posts.models import Post
from tutorials.models import Material, Tutorial


class SearchView(TemplateView):
    template_name = "search/search.html"

    def get(self, request, *args, **kwargs):
        query = (request.GET.get("q") or "").strip()
        sqs = SearchQuerySet().models(Post, Material, Tutorial, Article)
        form = SearchForm(request.GET or None, searchqueryset=sqs)

        results = form.search().load_all() if query and form.is_valid() else sqs.none()

        results_per_page = getattr(settings, "HAYSTACK_SEARCH_RESULTS_PER_PAGE", 20)
        paginator = Paginator(results, results_per_page)

        try:
            page_number = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            page_number = 1

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = self.get_context_data(**kwargs)
        context["form"] = form
        context["query"] = query
        context["headline"] = "搜索"
        context["paginator"] = paginator
        context["page_obj"] = page_obj
        context["is_paginated"] = paginator.num_pages > 1
        context["elided_page_range"] = paginator.get_elided_page_range(
            page_obj.number,
            on_each_side=2,
            on_ends=1,
        )
        context["hits"] = paginator.count
        return self.render_to_response(context)
