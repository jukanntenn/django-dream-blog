from django.urls import path

from dream_blog.views import HomeView
from posts.views import ArchivesView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("archives/", ArchivesView.as_view(), name="archives"),
]
