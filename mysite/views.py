from mysite.utils import toInt
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Count
from .models import Comment, CommentLike, Confession, ConfessionLike, Hashtag
from .auth import getAuthUser, isAuth, setAuthUser, delAuthUser
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
        "myUser": getAuthUser(request),
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

    context = {"form": form, "myUser": getAuthUser(request)}

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
            "id": comment.id,
            "content": comment.content,
            "author": comment.author.firstname + " " + comment.author.lastname,
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
            comment = Comment(content=cleaned_data["content"], author=getAuthUser(request), confession=confession)
            comment.save()

            return redirect(reverse("confession-details", args=[id]))

    context = {"confession": confessionDict, "comments": comments, "form": form, "myUser": getAuthUser(request)}
    response = render(request, "confession_details.html", context)
    return response


def confession_details_action(request, id, slug):

    if not isAuth(request):
        return redirect(reverse("confession-details", args=[id]))

    confession = get_object_or_404(Confession, id=id)

    if slug == "like":
        like = ConfessionLike.objects.filter(confession=confession, user=getAuthUser(request))

        if len(like) == 1:
            like[0].positive = True
            like[0].save()
        elif len(like) == 0:
            ConfessionLike(confession=confession, user=getAuthUser(request), positive=True).save()

    if slug == "dislike":
        like = ConfessionLike.objects.filter(confession=confession, user=getAuthUser(request))

        if len(like) == 1:
            like[0].positive = False
            like[0].save()
        elif len(like) == 0:
            ConfessionLike(confession=confession, user=getAuthUser(request), positive=False).save()

    return redirect(reverse("confession-details", args=[id]))


def confession_details_comment_action(request, confession_id, comment_id, slug):

    if not isAuth(request):
        return redirect(reverse("confession-details", args=[confession_id]))

    confession = get_object_or_404(Confession, id=confession_id)
    comment = get_object_or_404(confession.comment_set, id=comment_id)

    if slug == "like":
        like = CommentLike.objects.filter(comment=comment, user=getAuthUser(request))

        if len(like) == 1:
            like[0].positive = True
            like[0].save()
        elif len(like) == 0:
            CommentLike(comment=comment, user=getAuthUser(request), positive=True).save()

    if slug == "dislike":
        like = CommentLike.objects.filter(comment=comment, user=getAuthUser(request))

        if len(like) == 1:
            like[0].positive = False
            like[0].save()
        elif len(like) == 0:
            CommentLike(comment=comment, user=getAuthUser(request), positive=False).save()

    return redirect(reverse("confession-details", args=[confession_id]))