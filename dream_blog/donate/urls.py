from django.urls import path

from .views import DonateView

app_name = "donate"

urlpatterns = [
    path("", DonateView.as_view(), name="donate"),
]
