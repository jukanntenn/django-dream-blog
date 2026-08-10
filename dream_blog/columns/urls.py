from django.urls import path

from dream_blog.columns import views

app_name = "columns"
urlpatterns = [
    path("<str:slug>/", views.ColumnDetailView.as_view(), name="detail"),
    path(
        "<str:slug>/articles/<int:pk>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
]
