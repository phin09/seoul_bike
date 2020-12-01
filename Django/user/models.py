from django.db import models
from django.utils.timezone import now

from core import models as core_models


class Users(core_models.TimeStampedModel):
    username = models.CharField(max_length=64, verbose_name='사용자명')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    name = models.CharField(max_length=64, default=None, null=True)
    areaId = models.IntegerField(
        default=44, verbose_name='담당지역', primary_key=True)

    class Meta:
        db_table = "users"  # custom table name

    def __str__(self):
        return self.username
