from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Site, Customer


class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "bio",
        )


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ("name", "url",)
