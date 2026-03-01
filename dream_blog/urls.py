from django.urls import include, path

from dream_blog.views import HomeView
from posts.views import ArchivesView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("archives/", ArchivesView.as_view(), name="archives"),
    path("favorites/", include("dream_blog.favorites.urls")),
    path("newsletters/", include("dream_blog.newsletters.urls")),
]
