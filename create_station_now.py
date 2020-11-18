'''
table station_now에 초기값 넣기
'''

import os, json, requests
import django
from django.core.exceptions import ImproperlyConfigured
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from seoulbike.settings import BASE_DIR
from bikeapp.models import StationNow

# api key 불러오기
secret_file = os.path.join(BASE_DIR, 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable in secrets.json".format(setting)
        raise ImproperlyConfigured(error_msg)


# 따릉이 api 호출
SEOUL_KEY = get_secret("SEOUL_KEY")

api_urls = ["http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1/1000",
                "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1001/2000",
                "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/2001/3000"
                ]

# 기준 목록
station_area = pd.read_csv("./MergedStation_info.csv", encoding="utf-8")
st_lst = station_area['id'].tolist()

try:
    for api_url in api_urls:
        api_result = requests.get(api_url)
        api_json = json.loads(api_result.content)
        api_dict = api_json["rentBikeStatus"]["row"]

        for item in api_dict:
            stationCode = str(item['stationId'])
            stationName = str(item['stationName'])
            id = int(stationName.split('.')[0])
            rackTotCnt = int(item['rackTotCnt'])
            parkingBikeTotCnt = int(item['parkingBikeTotCnt'])
            stationLatitude = float(item['stationLatitude'])
            stationLongitude = float(item['stationLongitude'])

            try:  # create table station_now for the first time
                a = StationNow.objects.create(
                    stationCode=stationCode,
                    stationName=stationName,
                    parkingBikeTotCnt=parkingBikeTotCnt,
                )
                a.save()
            except:
                pass    # 2078(id) 대여소 unique constraint failed: area.id 원인 불명
            # except Exception as e:
            #     print(e)
            #     print(item)

except Exception as e:
    print(e)

# queryset = StationNow.objects.all()
# queryset.delete() # 일괄 delete 요청