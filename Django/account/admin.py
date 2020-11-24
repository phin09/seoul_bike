from django.contrib import admin
from .models import Users
# Register your models here.

class bikeUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Users, bikeUserAdmin)