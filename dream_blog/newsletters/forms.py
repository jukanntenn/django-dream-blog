from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": _("your@email.com"),
                    "class": "w-full rounded-lg border px-4 py-2 focus:ring-2 focus:ring-blue-500",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            subscription = Subscription.objects.get(email=email)
            if subscription.confirmed:
                raise forms.ValidationError(_("This email is already subscribed."))
            subscription.delete()
        except Subscription.DoesNotExist:
            pass
        return email

    def save(self, commit=True):
        subscription = super().save(commit=False)
        if self.user and self.user.is_authenticated:
            subscription.user = self.user
        if commit:
            subscription.save()
        return subscription
