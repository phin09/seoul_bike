from django.db import models

# Create your models here.


class StationNow(models.Model):
    stationName = models.CharField(max_length=100)
    parkingBikeTotCnt = models.IntegerField(default=0)
    dataId = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='dataId')
    stationCode = models.CharField(max_length=10, primary_key=True)
    created_at = models.DateTimeField(default=timezone.localtime)

    class Meta:
        db_table = "station_now"  # custom table name


class DailyStation(models.Model):   # pk=id는 index임
    ''' Model for '''
    dataId = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='dataId')
    parkingBikeTotCnt = models.IntegerField(default=0)
    created_at = models.CharField(max_length=20)

    class Meta:
        db_table = "daily_station"  # custom table name