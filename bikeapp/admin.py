from django.contrib import admin
from bikeapp.models import station
# Register your models here.

class stationAdmin(admin.ModelAdmin):
    pass

admin.site.register(station, stationAdmin)