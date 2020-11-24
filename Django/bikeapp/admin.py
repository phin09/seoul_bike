from django.contrib import admin
from bikeapp.models import StationNow


class stationAdmin(admin.ModelAdmin):
    pass


admin.site.register(StationNow, stationAdmin)