from django.urls import path
from posts import views

app_name = "posts"
urlpatterns = [
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
]
