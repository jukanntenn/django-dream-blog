from django.urls import path

from dream_blog.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
