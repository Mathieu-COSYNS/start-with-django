from django.shortcuts import redirect, render
from django.urls import reverse
from .models import User
from .auth import isAuth, getAuthUser, setAuthUser, delAuthUser
from .forms import LoginUserForm, RegisterUserForm


def sign_in(request):

    if isAuth(request):
        return redirect(reverse("account"))

    form = LoginUserForm(request.POST or None)

    if form.is_valid():
        user = form.cleaned_data
        setAuthUser(request, user)
        return redirect(reverse("account"))

    context = {"form": form}
    response = render(request, "sign-in.html", context)
    return response


def sign_up(request):

    if isAuth(request):
        return redirect(reverse("account"))

    form = RegisterUserForm(request.POST or None)

    if form.is_valid():
        new_user = form.save()
        setAuthUser(request, new_user)
        return redirect(reverse("account"))

    context = {"form": form}
    response = render(request, "sign-up.html", context)
    return response


def sign_out(request):

    delAuthUser(request)
    return redirect(reverse("sign-in"))


def home(request):
    return redirect(reverse("sign-in"))


def account(request):

    if not isAuth(request):
        return redirect(reverse("sign-in"))

    print(User.objects.all())

    context = {"myUser": getAuthUser(request)}
    response = render(request, "account.html", context)
    return response