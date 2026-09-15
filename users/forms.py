import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        errors = []
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")
        if re.fullmatch(r"[A-Za-z0-9]", password1):
            raise forms.ValidationError(
                "Password must contain at least one letter and one number"
            )
        if errors:
            raise forms.ValidationError(errors)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords not the same")
        return cleaned_data
