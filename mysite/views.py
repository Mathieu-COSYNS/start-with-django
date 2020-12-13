from mysite.utils import toInt
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Confession, ConfessionLike, Hashtag, User
from .auth import isAuth, getAuthUser, setAuthUser, delAuthUser
from .forms import AddConfessionForm, LoginUserForm, RegisterUserForm


def sign_in(request):

    if isAuth(request):
        return redirect(reverse("home"))

    form = LoginUserForm(request.POST or None)

    if form.is_valid():
        user = form.cleaned_data
        setAuthUser(request, user)
        return redirect(reverse("home"))

    context = {"form": form}
    response = render(request, "sign-in.html", context)
    return response


def sign_up(request):

    if isAuth(request):
        return redirect(reverse("home"))

    form = RegisterUserForm(request.POST or None)

    if form.is_valid():
        new_user = form.save()
        setAuthUser(request, new_user)
        return redirect(reverse("home"))

    context = {"form": form}
    response = render(request, "sign-up.html", context)
    return response


def sign_out(request):

    delAuthUser(request)
    return redirect(reverse("sign-in"))


def home(request):
    selected_hashtag = toInt(request.GET.get("hashtag"))

    if selected_hashtag:
        try:
            selected_hashtag = Hashtag.objects.get(id=selected_hashtag)
        except Hashtag.DoesNotExist:
            return redirect(reverse("home"))
        confessions = Confession.objects.filter(hashtags__in=[selected_hashtag])
    else:
        confessions = Confession.objects.all()

    context = {
        "hashtags": Hashtag.objects.all(),
        "selected_hashtag": selected_hashtag,
        "confessions": confessions,
    }
    response = render(request, "home.html", context)
    return response


def add_confession(request):

    form = AddConfessionForm(request.POST or None)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        print(cleaned_data)
        confession = Confession(title=cleaned_data["title"], content=cleaned_data["content"])
        confession.save()
        for hashtag_name in cleaned_data["hashtags"]:
            hashtag = Hashtag.objects.get_or_create(name=hashtag_name)[0]
            confession.hashtags.add(hashtag)

        return redirect(reverse("home"))

    context = {"form": form}

    response = render(request, "add_confession.html", context)
    return response


def confession_details(request, id):
    response = render(request, "confession_details.html")
    return response