from .models import User


def isAuth(request):
    return bool(request.session.get("userId")) and len(User.objects.filter(id=request.session.get("userId"))) == 1


def getAuthUser(request):
    user = User.objects.filter(id=request.session.get("userId"))

    if len(user) != 1:
        return None

    return user[0]