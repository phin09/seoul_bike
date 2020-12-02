from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.Stations)
class StationAdmin(admin.ModelAdmin):
    list_display = (
        "dataId",
        "stationCode",
        "stationName",
        "stationLatitude",
        "stationLongitude",
        "rackTotCnt",
        "distance_hanriver",
        "distance_bikeroad",
        "distance_subway",
        "distance_school_mid",
        "distance_school_high",
        "distance_school_univ",
        "PopTot",
        "areaId",

    )
