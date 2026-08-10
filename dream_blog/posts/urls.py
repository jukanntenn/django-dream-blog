from django.urls import path

from dream_blog.posts import views

app_name = "posts"
urlpatterns = [
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
]
