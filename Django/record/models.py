from django.db import models
from django.utils import timezone

from station.models import Station
from core import models as core_models
from station.models import Station

# Create your models here.


class nowRecord(core_models.TimestampedModel):

    ''' Definition of StationNow Model '''

    parkingBikeTotCnt = models.IntegerField(default=0)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, db_column='station')

    class Meta:
        db_table = "record_now"  # custom table name

class predictedRecord(core_models.TimestampedModel):

    ''' Definition of StationNow Model '''

    predReturn = models.IntegerField(default=0)
    predRent = models.IntegerField(default=0)    
    station = models.ForeignKey(Station, on_delete=models.CASCADE, db_column='station')

    class Meta:
        db_table = "record_predict"  # custom table name



