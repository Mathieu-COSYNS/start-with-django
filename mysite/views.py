from mysite.models import User
from django.shortcuts import redirect, render
from datetime import datetime
import random


def hello(request):
    data = {
        "names": ["a", "b", "c", "d"],
        "datetime": datetime.now().strftime("%H:%M:%S"),
        "random": random.randrange(100),
    }
    response = render(request, "hello.html", data)
    return response


def login(request):

    if isAuth(request):
        return redirect("/account")

    if request.POST.get("email") and request.POST.get("password"):
        email = request.POST.get("email")
        password = request.POST.get("password")
        if len(User.objects.filter(email=email).filter(password=password)) == 1:
            request.session["userType"] = "basic"
            return redirect("/account")
        else:
            return redirect("/login")

    response = render(request, "login.html")
    return response


def register(request):

    if isAuth(request):
        return redirect("/account")

    if request.POST:
        if request.POST.get("email"):
            User(
                firstname=request.POST.get("firstname"),
                lastname=request.POST.get("lastname"),
                country=request.POST.get("country"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                password=request.POST.get("password"),
                gender=request.POST.get("gender"),
            ).save()

            request.session["userType"] = "basic"
            return redirect("/account")
        else:
            return redirect("/register")

    response = render(request, "register.html")
    return response


def account(request):

    if not isAuth(request):
        return redirect("/login")

    data = {"userType": request.session["userType"]}
    response = render(request, "account.html", data)
    return response


def isAuth(request):
    return request.session.get("userType") == "basic"