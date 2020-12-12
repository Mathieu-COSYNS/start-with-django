from .models import User
from django.shortcuts import redirect, render
from datetime import datetime
from .auth import isAuth, getAuthUser
from .forms import RegisterUserForm


def login(request):

    if isAuth(request):
        return redirect("/account")

    if request.method == "POST":
        if request.POST.get("email") and request.POST.get("password"):
            email = request.POST.get("email")
            password = request.POST.get("password")
            if len(User.objects.filter(email=email).filter(password=password)) == 1:
                request.session["userId"] = 1
                return redirect("/account")

        return redirect("/login")

    response = render(request, "login.html")
    return response


def register(request):

    if isAuth(request):
        return redirect("/account")

    form = RegisterUserForm(request.POST or None)

    if form.is_valid():
        form.save()

        # request.session["userId"] = newUser.id
        return redirect("/account")

    context = {"form": form}

    response = render(request, "register.html", context)
    return response


def account(request):

    if not isAuth(request):
        return redirect("/login")

    data = {"user": getAuthUser(request)}
    response = render(request, "account.html", data)
    return response