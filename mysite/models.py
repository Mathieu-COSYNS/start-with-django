from django.db import models
from django.db.models.fields import CharField


class User(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("X", "X"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.email
