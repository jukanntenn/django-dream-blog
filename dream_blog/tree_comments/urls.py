from django.urls import path
from tree_comments.views import CommentFormTemplateView, CommentPostView

app_name = "tree_comments"
urlpatterns = [
    path("form/", CommentFormTemplateView.as_view(), name="form"),
    path("post/", CommentPostView.as_view(), name="post"),
]
