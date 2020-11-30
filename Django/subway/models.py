from django.db import models

from station.models import Station

# Create your models here.
class SubwayTot(models.Model):

    
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    tot_getoff = models.FloatField()
    tot_ride = models.FloatField()

    station = models.ForeignKey(Station, on_delete =models.CASCADE)

    class Meta:
        db_table = "subway_tot"  # custom table name
        
class SubwayRideGetoff(models.Model):

    month = models.IntegerField(default=0)
    hour = models.IntegerField(default=0)
    SubGetoff = models.IntegerField()
    SubRide = models.IntegerField()

    station = models.ForeignKey(Station, on_delete =models.CASCADE)

    class Meta:
        db_table = "subway_RideGetoff"  # custom table name