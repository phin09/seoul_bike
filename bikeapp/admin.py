from django.contrib import admin
from bikeapp.models import station


class stationAdmin(admin.ModelAdmin):
    pass


admin.site.register(station, stationAdmin)