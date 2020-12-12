from .models import User
from django.shortcuts import redirect, render
from datetime import datetime
from .auth import isAuth, getAuthUser


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

    if request.method == "POST":
        if request.POST.get("email"):
            newUser = User(
                firstname=request.POST.get("firstname"),
                lastname=request.POST.get("lastname"),
                country=request.POST.get("country"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                password=request.POST.get("password"),
                gender=request.POST.get("gender"),
            )

            newUser.save()

            request.session["userId"] = newUser.id
            return redirect("/account")

        return redirect("/register")

    response = render(request, "register.html")
    return response


def account(request):

    if not isAuth(request):
        return redirect("/login")

    data = {"user": getAuthUser(request)}
    response = render(request, "account.html", data)
    return response