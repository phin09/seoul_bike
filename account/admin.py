from django.contrib import admin
from .models import bikeUser
# Register your models here.

class bikeUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(bikeUser, bikeUserAdmin)