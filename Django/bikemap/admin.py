from django.contrib import admin

# Register your models here.

from . import models
@admin.register(models.StationNow)
class StaionNowAdmin(admin.ModelAdmin):
    list_display =('parkingBikeTotCnt', 'station', 'created_at')