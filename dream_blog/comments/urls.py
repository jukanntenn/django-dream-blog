from django.urls import path

from dream_blog.comments.views import CommentFormTemplateView, CommentPostView

app_name = "comments"
urlpatterns = [
    path("form/", CommentFormTemplateView.as_view(), name="form"),
    path("post/", CommentPostView.as_view(), name="post"),
]
