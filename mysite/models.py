from django.db import models
from django.db.models.fields import CharField


class User(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email
