from django.urls import path
from tutorials import views

app_name = "tutorials"
urlpatterns = [
    path("<str:slug>/", views.TutorialDetailView.as_view(), name="detail"),
    path(
        "<str:slug>/materials/<int:pk>/",
        views.MaterialDetailView.as_view(),
        name="material_detail",
    ),
]
