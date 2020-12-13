from django.db import models
from  user.models import Users

class Stations(models.Model):

    dataId = models.IntegerField(default=0, primary_key=True)
    stationCode = models.CharField(max_length=10)
    stationName = models.CharField(max_length=100)
    stationLatitude = models.FloatField(max_length=20)
    stationLongitude = models.FloatField(max_length=20)
    rackTotCnt = models.IntegerField(default=0)
    distance_hanriver = models.IntegerField(default=0)
    distance_bikeroad = models.IntegerField(default=0)
    distance_subway = models.IntegerField(default=0)
    distance_school_mid = models.IntegerField(default=0)
    distance_school_high = models.IntegerField(default=0)
    distance_school_univ = models.IntegerField(default=0)
    PopTot = models.IntegerField(default=0)

    areaId = models.ForeignKey(Users,related_name="stations", on_delete=models.PROTECT, db_column='areaId')

    class Meta:
        db_table = "station"  # custom table name


from django.db import models
from station.models import Stations

# Create your models here.


class SubwayTot(models.Model):

    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    tot_getoff = models.FloatField()
    tot_ride = models.FloatField()

    station = models.ForeignKey(
        Stations, on_delete=models.CASCADE)

    class Meta:
        db_table = "subway_tot"  # custom table name


class SubwayRideGetoff(models.Model):

    month = models.IntegerField(default=0)
    hour = models.IntegerField(default=0)
    SubGetoff = models.IntegerField()
    SubRide = models.IntegerField()

    station = models.ForeignKey(
        Stations,  on_delete=models.CASCADE)

    class Meta:
        db_table = "subway_RideGetoff"  # custom table name

