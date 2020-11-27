from django.db import models
from core import models as core_models

# Create your models here.


class StationNow(core_models.TimestampedModel):
    stationName = models.CharField(max_length=100)
    parkingBikeTotCnt = models.IntegerField(default=0)
    stationCode = models.CharField(max_length=10, primary_key=True)
    created_at = models.DateTimeField(default=timezone.localtime)
    dataId = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='dataId')

    class Meta:
        db_table = "station_now"  # custom table name


class DailyStation(core_models.TimestampedModel):   # pk=id는 index임
    ''' Model for '''
    
    parkingBikeTotCnt = models.IntegerField(default=0)
    created_at = models.CharField(max_length=20)

    dataId = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='dataId')

    class Meta:
        db_table = "daily_station"  # custom table name