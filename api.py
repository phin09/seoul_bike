import os
import django
from seoulbike.settings import BASE_DIR
from django.core.exceptions import ImproperlyConfigured
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()

import pandas as pd
import json
import requests
import time
from bikeapp.models import station
from datetime import datetime as datetime

# bike data 불러오기
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        # print("check: ", secrets[setting])
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable in secrets.json".format(setting)
        raise ImproperlyConfigured(error_msg)


SEOUL_KEY = get_secret("SEOUL_KEY")
KAKAO_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret("KAKAO_KEY")

api_urls = ["http://openapi.seoul.go.kr:8088/" + SEOUL_KEY + "/json/bikeList/1/1000",
            "http://openapi.seoul.go.kr:8088/" + SEOUL_KEY + "/json/bikeList/1001/2000",
            "http://openapi.seoul.go.kr:8088/" + SEOUL_KEY + "/json/bikeList/2001/3000"
            ]
try:
    seoulbike = pd.DataFrame()
    for api_url in api_urls:
        api_result = requests.get(api_url)
        api_json = json.loads(api_result.content)
        api_dict = api_json["rentBikeStatus"]["row"]
        api_dp = pd.DataFrame(api_dict)
        seoulbike = pd.concat([seoulbike, api_dp])

    now = time.localtime()
    now_time = time.strftime("%Y/%m/%d %H:%M:%S", now)
    seoulbike = seoulbike.drop_duplicates("stationId", keep="last")
    seoulbike.insert(7, "date", now_time)
    seoulbike = seoulbike.reset_index()
    seoulbike = seoulbike.drop('index', axis=1)
    # st_dict_db = seoulbike.to_dict()
    # seoulbike.to_csv("test.csv", encoding="cp949")
    print(seoulbike)

except Exception as e:
    api = "Error..."

# # station 테이블 삭제
station_del = station.objects.all()
station_del.delete()
for i in range(seoulbike.shape[0]):
    rackTotCnt = int(seoulbike['rackTotCnt'][i])
    stationName = seoulbike['stationName'][i]
    parkingBikeTotCnt = int(seoulbike['parkingBikeTotCnt'][i])
    shared = int(seoulbike['shared'][i])
    stationLatitude = float(seoulbike['stationLatitude'][i])
    stationLongitude = float(seoulbike['stationLongitude'][i])
    stationId = seoulbike['stationId'][i]
    # print(seoulbike['date'][i])
    date = seoulbike['date'][i]
    date = datetime.strptime(seoulbike['date'][i], '%Y/%m/%d %H:%M:%S')

    try:
        #생성
        a=station.objects.create(
            rackTotCnt=rackTotCnt,
            stationName=stationName,
            parkingBikeTotCnt=parkingBikeTotCnt,
            shared=shared,
            stationLatitude=stationLatitude,
            stationLongitude=stationLongitude,
            stationId=stationId,
            date=date,
        )
        a.save()
        print("성공")
    except:
        print("실패")


