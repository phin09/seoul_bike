from django.db import models
from django.utils import timezone

from station.models import Stations
from core import models as core_models


# Create your models here.

class StationNow(core_models.TimeStampedModel):

    ''' Definition of StationNow Model '''

    parkingBikeTotCnt = models.IntegerField(default=0)
    station = models.ForeignKey(Stations, on_delete=models.CASCADE, db_column='station', related_name ="stationNow")

    class Meta:
        db_table = "station_now"  # custom table name
