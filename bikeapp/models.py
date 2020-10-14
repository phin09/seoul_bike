from django.db import models

# Create your models here.


class station(models.Model):
    rackTotCnt = models.IntegerField()
    stationName = models.CharField(max_length=100)
    parkingBikeTotCnt = models.IntegerField()
    shared = models.IntegerField()
    stationLatitude = models.FloatField()
    stationLongitude = models.FloatField()
    stationId = models.IntegerField(primary_key=True)
    date = models.DateTimeField(null=True)

    #rackTotCnt  거치대 수
    #stationName 대여소명
    #parkingBikeTotCnt 자전거주차총건수
    #shared  거치율
    #stationLatitude 위도
    #stationLongitude    경도
    #stationId   대여소ID
    #date    기준시작일자



