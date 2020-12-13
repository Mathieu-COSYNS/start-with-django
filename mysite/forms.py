from django import forms
from django.core.exceptions import ValidationError
from .models import User


class LoginUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = User.objects.filter(email=email).filter(password=password)
            if len(user) != 1:
                raise ValidationError("Email or password invalid")
            return user[0]


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "firstname",
            "lastname",
            "email",
            "password",
            "confirm_password",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            msg = "Password and Confirm password must be identical"
            self.add_error("password", msg)
            self.add_error("confirm_password", msg)
