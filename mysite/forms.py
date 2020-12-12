from django import forms
from django.db.models import fields
from .models import User


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
