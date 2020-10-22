import pandas as pd
import json
import requests
import time
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
import django
django.setup()
import sqlite3
from bikeapp.models import station
from account.models import bikeUser
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    seoulbike.to_csv("test.csv", encoding="cp949")

except Exception as e:
    api = "Error..."

# for i in range(seoulbike.shape[0]):
#     rackTotCnt = int(seoulbike['rackTotCnt'][i])
#     stationName = seoulbike['stationName'][i]
#     parkingBikeTotCnt = int(seoulbike['parkingBikeTotCnt'][i])
#     shared = int(seoulbike['shared'][i])
#     lattitude = float(seoulbike['stationLatitude'][i])
#     longitude = float(seoulbike['stationLongitude'][i])
#     stationId = seoulbike['stationId'][i]
#     date = seoulbike['date'][i]
#     try:
#         station.objects.create(
#             rackTotCnt = rackTotCnt,
#             stationName = stationName,
#             parkingBikeTotCnt = parkingBikeTotCnt,
#             shared = shared,
#             lattitude = lattitude,
#             longitude = longitude,
#             stationId = stationId,
#             date = date,
#         )
#     except:
#         pass
#
# if __name__=='__main__':
#
#     for rTC, sName, pB, s, l, lo, sI, date in st_dict_db.items():
#         station(rackTotCnt=rTC, stationName=sName, parkingBikeTotCnt=pB, shared=s, stationLatitude=l, stationLongitude=lo, stationId=sI, date=date).save()


con = sqlite3.connect('./db.sqlite3')
cur = con.cursor()
cur.execute("DELETE FROM bikeUser")
#station table에 데이터 넣기
# seoulbike.to_sql('station', con, if_exists='replace')
# if_exists = 'fail' : 같은 이름의 Table이 존재할 경우 ValueError 가 남
# if_exists = 'replace': 같은 이름의 Table이 존재할 경우 기존 Table을 Drop하고 새로운 값을 Insert함
# if_exists = 'append': 같은 이름의 Table이 존재할 경우 기존 Table에 추가로 새로운 값을 Insert함
con.commit()
con.close()




