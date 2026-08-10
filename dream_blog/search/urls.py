from django.urls import path

from dream_blog.search.views import SearchView

app_name = "search"

urlpatterns = [
    path("", SearchView.as_view(), name="search"),
]
