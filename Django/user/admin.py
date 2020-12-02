from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'areaId')
