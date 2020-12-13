from mysite.utils import toInt
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Count
from .models import Confession, Hashtag
from .auth import isAuth, setAuthUser, delAuthUser
from .forms import AddCommentForm, AddConfessionForm, LoginUserForm, RegisterUserForm


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
    confessionsList = []

    if selected_hashtag:
        try:
            selected_hashtag = Hashtag.objects.get(id=selected_hashtag)
        except Hashtag.DoesNotExist:
            return redirect(reverse("home"))
        confessions = Confession.objects.filter(hashtags__in=[selected_hashtag])
    else:
        confessions = Confession.objects.all()

    for confession in confessions:
        confessionDict = {
            "id": confession.id,
            "title": confession.title,
            "content": confession.content,
            "hashtags": confession.hashtags.all().values_list("name", flat=True),
            "likes": confession.confessionlike_set.filter(positive=True).count(),
            "dislikes": confession.confessionlike_set.filter(positive=False).count(),
        }
        confessionsList.append(confessionDict)

    confession_top10_id_title_map = (
        Confession.objects.annotate(like_count=Count("confessionlike"))
        .order_by("-like_count")
        .values("id", "title")[:10]
    )

    context = {
        "hashtags": Hashtag.objects.all(),
        "selected_hashtag": selected_hashtag,
        "confessions": confessionsList,
        "confession_top10_id_title_map": confession_top10_id_title_map,
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

    confession = get_object_or_404(Confession, id=id)

    confessionDict = {
        "id": confession.id,
        "title": confession.title,
        "content": confession.content,
        "hashtags": confession.hashtags.all().values_list("name", flat=True),
        "likes": confession.confessionlike_set.filter(positive=True).count(),
        "dislikes": confession.confessionlike_set.filter(positive=False).count(),
    }
    comments = []

    for comment in confession.comment_set.all():
        commentDict = {
            "content": comment.content,
            "likes": comment.commentlike_set.filter(positive=True).count(),
            "dislikes": comment.commentlike_set.filter(positive=False).count(),
        }
        comments.append(commentDict)

    form = None

    if isAuth(request):
        form = AddCommentForm(request.POST or None)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            print(cleaned_data)
            """ confession = Confession(title=cleaned_data["title"], content=cleaned_data["content"])
            confession.save() """

            return redirect(reverse("confession-details", id=id))

    context = {"confession": confessionDict, "comments": comments, "form": form}
    response = render(request, "confession_details.html", context)
    return response