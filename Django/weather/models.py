from django.db import models

# Create your models here.

class Weather(models.Model):
    
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    hour = models.IntegerField(default=0)
    T1H = models.FloatField()   # 기온
    SKY = models.FloatField(default=0)
    RN1 = models.FloatField()   # 1시간 강수량
    REH = models.FloatField()   # 습도
    PTY = models.FloatField()   # 강수형태
    VEC = models.FloatField()   # 풍향
    WSD = models.FloatField()   # 풍속
    S06 = models.FloatField()   # 6시간 신적설

    class Meta:
        db_table = "weather"  # custom table name