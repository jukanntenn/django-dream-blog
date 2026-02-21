from comments.views import CommentFormTemplateView, CommentPostView
from django.urls import path

app_name = "comments"
urlpatterns = [
    path("form/", CommentFormTemplateView.as_view(), name="form"),
    path("post/", CommentPostView.as_view(), name="post"),
]
