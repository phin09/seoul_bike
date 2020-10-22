import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()

import pandas as pd
import json
import requests
import time
from bikeapp.models import station
from datetime import datetime as datetime

api_urls = ["http://openapi.seoul.go.kr:8088/736c62634a736b7339376a694c6665/json/bikeList/1/1000",
            "http://openapi.seoul.go.kr:8088/736c62634a736b7339376a694c6665/json/bikeList/1001/2000",
            "http://openapi.seoul.go.kr:8088/736c62634a736b7339376a694c6665/json/bikeList/2001/3000"
            ]

try:
    sb = pd.DataFrame()
    for api_url in api_urls:
        api_result = requests.get(api_url)
        api_json = json.loads(api_result.content)
        api_dict = api_json["rentBikeStatus"]["row"]
        api_dp = pd.DataFrame(api_dict)
        sb = pd.concat([sb, api_dp])

    st_dict = sb.to_dict(orient='records')
    st_dict_db = sb.to_dict()
    now = time.localtime()
    now_time = time.strftime("%Y/%m/%d %H:%M:%S", now)
    seoulbike = sb.drop_duplicates("stationId", keep="last")
    seoulbike.insert(7, "date", now_time)
    seoulbike = seoulbike.reset_index()

    seoulbike = seoulbike.drop('index', axis=1)
    st_dict_db = seoulbike.to_dict()
    # seoulbike.to_csv("test.csv", encoding="cp949")
    print(seoulbike)

except Exception as e:
    api = "Error..."

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
        # 생성
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
        # 수정
        # a=station.objects.update(
        #     rackTotCnt=rackTotCnt,
        #     stationName=stationName,
        #     parkingBikeTotCnt=parkingBikeTotCnt,
        #     shared=shared,
        #     stationLatitude=stationLatitude,
        #     stationLongitude=stationLongitude,
        #     stationId=stationId,
        #     date=date,
        # )
        a.save()
    except:
        pass

