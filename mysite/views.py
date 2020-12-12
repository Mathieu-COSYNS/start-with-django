from .models import User
from django.shortcuts import redirect, render
from .auth import isAuth, getAuthUser, setAuthUser, delAuthUser
from .forms import LoginUserForm, RegisterUserForm


def login(request):

    if isAuth(request):
        return redirect("/account")

    form = LoginUserForm(request.POST or None)

    if form.is_valid():
        user = form.cleaned_data
        setAuthUser(request, user)
        return redirect("/account")

    context = {"form": form}
    response = render(request, "login.html", context)
    return response


def register(request):

    if isAuth(request):
        return redirect("/account")

    form = RegisterUserForm(request.POST or None)

    if form.is_valid():
        new_user = form.save()

        setAuthUser(request, new_user)
        return redirect("/account")

    context = {"form": form}
    response = render(request, "register.html", context)
    return response


def account(request):

    if not isAuth(request):
        return redirect("/login")

    print(User.objects.all())

    context = {"myUser": getAuthUser(request)}
    response = render(request, "account.html", context)
    return response


def logout(request):

    delAuthUser(request)
    return redirect("/login")
