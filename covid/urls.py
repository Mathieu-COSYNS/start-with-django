from django.urls import path
from .views import algo_view

# ce fichier peut vous sembler bizzare il s'agit ici d'une sous application. Utilisée ligne 33 dans mysite/urls.py
urlpatterns = [
    path("", algo_view),
]
