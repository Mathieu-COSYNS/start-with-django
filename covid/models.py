from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

# Create your models here.
class User(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class Covid(models.Model):
    user = models.ForeignKey("User", on_delete=CASCADE)
    test_date = models.DateField()

    def __str__(self):
        return str(self.test_date) + " " + str(self.user)


class Reservation(models.Model):
    user = models.ForeignKey("User", on_delete=CASCADE)
    date = models.DateField()
    establishment = models.ForeignKey("Establishment", on_delete=CASCADE)

    def __str__(self):
        return str(self.date) + " " + str(self.user) + " " + str(self.establishment)


class Establishment(models.Model):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name