from django.contrib import admin
from .models import Users

# Register your models here.


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'login_Id',
        'password',
        'areaId',
        'updated_at'
    )

    
        
