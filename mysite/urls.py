"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (
    add_confession,
    confession_details,
    confession_details_action,
    confession_details_comment_action,
    home,
    sign_in,
    sign_up,
    sign_out,
)

import covid

urlpatterns = [
    path("admin/", admin.site.urls),
    path("covid/", include("covid.urls")),
    path("", home, name="home"),
    path("sign-in", sign_in, name="sign-in"),
    path("sign-up", sign_up, name="sign-up"),
    path("sign-out", sign_out, name="sign-out"),
    path("confession/add", add_confession, name="add-confession"),
    path("confession/<int:id>", confession_details, name="confession-details"),
    path("confession/<int:id>/<slug:slug>", confession_details_action, name="confession-details-action"),
    path(
        "confession/<int:confession_id>/comment/<int:comment_id>/<slug:slug>",
        confession_details_comment_action,
        name="confession-details-comment-action",
    ),
]
