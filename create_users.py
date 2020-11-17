'''
user 여러개 만들기
db 생성 후 한 번만 돌릴 코드라 csv를 이용함
'''

import os
import django
import pandas as pd
from django.contrib.auth.hashers import make_password
from account.models import Users

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()

bikeuser = pd.read_csv("bikeuser1234.csv",encoding='cp949')

for i in range(bikeuser.shape[0]):
    username = str(bikeuser['username'][i])
    password = str(bikeuser['password'][i])
    areaid = str(bikeuser['areaid'][i])

    try:
       a = Users.objects.create(
            username=username,
            password=make_password(password),
            areaId=areaid,
        )
       a.save()

    except:
        pass

