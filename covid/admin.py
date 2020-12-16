from django.contrib import admin
from .models import Covid, User, Reservation, Establishment

# Register your models here.
admin.site.register(Covid)
admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(Establishment)