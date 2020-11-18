import sys
import os
from django.db import models
from django.utils import timezone
from account.models import Users

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# rackTotCnt  거치대 수
# stationName 대여소명
# id 또는 dataId 대여소 번호(stationName에서 추출)
# stationCode   대여소ID(ST-XXX)
# parkingBikeTotCnt 자전거주차총건수
# stationLatitude 위도
# stationLongitude    경도


class StationNow(models.Model):
    stationName = models.CharField(max_length=100)
    parkingBikeTotCnt = models.IntegerField(default=0)
    stationCode = models.CharField(max_length=10, primary_key=True)
    created_at = models.DateTimeField(default=timezone.localtime)
    class Meta:
        db_table = "station_now"  # custom table name

class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    stationCode = models.ForeignKey(StationNow, on_delete=models.CASCADE, db_column='stationCode')
    stationLatitude = models.FloatField(max_length=20)
    stationLongitude = models.FloatField(max_length=20)
    #areaId = models.IntegerField(default=80)    # 임시
    areaId = models.ForeignKey(Users, on_delete=models.PROTECT, db_column='areaId')
    rackTotCnt = models.IntegerField(default=0)
    distance_hanriver = models.IntegerField(default=0)
    distance_bikeroad = models.IntegerField(default=0)
    distance_subway = models.IntegerField(default=0)
    distance_school_mid = models.IntegerField(default=0)
    distance_school_high = models.IntegerField(default=0)
    distance_school_univ = models.IntegerField(default=0)
    PopTot = models.IntegerField(default=0)
    # geoProperties.csv에서 긁어넣기
    # 대여소 시/구/동 주소도 여기에 넣을지?
    class Meta:
        db_table = "area"  # custom table name


class DailyStation(models.Model):   # pk=id는 index임
    dataId = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='dataId')
    parkingBikeTotCnt = models.IntegerField(default=0)
    created_at = models.CharField(max_length=20)
    class Meta:
        db_table = "daily_station"  # custom table name


class Weather(models.Model):    # 실시간 업데이트할 API 찾아야
    ta = models.FloatField()
    rn = models.FloatField()
    ws = models.FloatField()
    wd = models.FloatField()
    hm = models.FloatField()
    ss = models.FloatField()
    icsr = models.FloatField()
    dsnw = models.FloatField()
    hr3Fhsc = models.FloatField()
    created_at = models.DateTimeField(default=timezone.localtime, editable=False)
    class Meta:
        db_table = "weather"  # custom table name


# subwayProperties.csv, subwayTot.csv 각기 table 만들어 저장하기. 모델 업데이트용.


# on_delete=models.PROTECT 참조값 사라져도 삭제하지 않음
# on_delete=models.SET_DEFAULT 참조값 사라지면 default(0)으로 변경