from django.db import models
from django.utils import timezone

from station.models import Station
from core import models as core_models
from station.models import Station

# Create your models here.


class StationNow(core_models.TimestampedModel):

    ''' Definition of StationNow Model '''

    stationName = models.CharField(max_length=100)
    parkingBikeTotCnt = models.IntegerField(default=0)
    stationCode = models.CharField(max_length=10, primary_key=True)

    dataId = models.ForeignKey(
        Station, on_delete=models.CASCADE, db_column='dataId')

    class Meta:
        db_table = "station_now"  # custom table name


class DailyStation(core_models.TimestampedModel):   # pk=id는 index임

    ''' Definition of DailyStation Model '''

    parkingBikeTotCnt = models.IntegerField(default=0)
    dataId = models.ForeignKey(
        Station, on_delete=models.CASCADE, db_column='dataId')

    class Meta:
        db_table = "daily_station"  # custom table name
