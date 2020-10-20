from django.db import models


# bikeUser 모델 생성
class bikeUser(models.Model):
    username = models.CharField(max_length=64, verbose_name='사용자명')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    areaid = models.CharField(max_length=10, verbose_name='담당지역')
    register_dttm = models.DateField(auto_now_add=True, verbose_name='가입일자') # 자동으로 해당 시간이 추가됨

    def __str__(self):
        return self.username
