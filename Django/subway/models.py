from django.db import models

# Create your models here.
class SubwayTot(models.Model):
    dataId = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    tot_getoff = models.FloatField()
    tot_ride = models.FloatField()

    class Meta:
        db_table = "subway_tot"  # custom table name
        
class SubwayRideGetoff(models.Model):
    dataId = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    hour = models.IntegerField(default=0)
    SubGetoff = models.IntegerField()
    SubRide = models.IntegerField()

    class Meta:
        db_table = "subway_RideGetoff"  # custom table name