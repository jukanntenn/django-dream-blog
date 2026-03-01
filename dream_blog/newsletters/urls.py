from django.urls import path

from . import views

app_name = "newsletters"
urlpatterns = [
    path("subscription/", views.SubscriptionCreateView.as_view(), name="subscription"),
    path(
        "subscription/confirm/<str:key>/",
        views.SubscriptionConfirmView.as_view(),
        name="subscription-confirm",
    ),
]
