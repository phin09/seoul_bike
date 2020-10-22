import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()

import pandas as pd
from django.contrib.auth.hashers import make_password
import json
import requests
import time
from account.models import bikeUser
from bikeapp.models import station

# bikeuser = pd.read_csv("bikeuser.csv",encoding='cp949')
#
# for i in range(bikeuser.shape[0]):
#     username = str(bikeuser['id'][i])
#     password = str(bikeuser['password'][i])
#     areaid = str(bikeuser['area'][i])
#
#
#     try:
#        a = bikeUser.objects.create(
#             username=username,
#             password=make_password(password),
#             areaid=areaid,
#         )
#        a.save()
#
#     except:
#         pass
#
# from django.forms import model_to_dict
# bikeuser = [model_to_dict(bikeUser) for bikeUser in bikeUser.objects.all()]
# df = pd.DataFrame(bikeuser)
# print(df)
#
queryset = station.objects.all()
queryset.delete() # 일괄 delete 요청