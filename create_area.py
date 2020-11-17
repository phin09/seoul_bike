'''
table area에 초기값 넣기
db 생성 후 한 번만 돌릴 코드
'''

import os, json, requests
import django
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from seoulbike.settings import BASE_DIR
from bikeapp.models import Area, StationNow
from account.models import Users

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
try:
    # insert areaId data into the table area
    station_area = pd.read_csv("./MergedStation_info.csv", encoding="utf-8")
    station_area = station_area.drop(station_area.columns[[0, 2, 3]], axis=1)
    station_area = station_area.fillna(44)  # 임시 default areaId 값
    station_area = station_area.replace(0, 44)  # 임시 default areaId 값
    station_area = station_area.astype({'cluster': int})
    st_lst = station_area['id'].tolist()    # 기준 목록
    station_area = station_area.to_dict(orient='records')  # list of dicts

    for api_url in api_urls:
        api_result = requests.get(api_url)
        api_json = json.loads(api_result.content)
        api_dict = api_json["rentBikeStatus"]["row"]

        for i in api_dict:
            stationName = str(i['stationName'])
            id = int(stationName.split('.')[0])
            if id not in st_lst:    # 기준 목록에 없다면 무시하도록 삭제
                api_dict.remove(i)

        for item in api_dict:   # api로부터 긁어오고 기준 목록으로 필터링한 대여소
            stationCode = str(item['stationId'])
            stationName = str(item['stationName'])
            id = int(stationName.split('.')[0])
            rackTotCnt = int(item['rackTotCnt'])
            parkingBikeTotCnt = int(item['parkingBikeTotCnt'])
            stationLatitude = float(item['stationLatitude'])
            stationLongitude = float(item['stationLongitude'])

            for area in station_area:
                id_temp = area['id']
                if id == id_temp:
                    cluster = area['cluster']
                    # matching query does not exist 방지
                    check = Users.objects.filter(areaId=cluster)
                    if len(check)>0:
                        areaId_obj = get_object_or_404(Users, areaId=cluster)
                    else:
                        areaId_obj = Users.objects.get(areaId=44)   # 임시 default areaId

            try:    # create table area for the first time
                b = Area.objects.create(
                    stationCode=get_object_or_404(StationNow, stationCode=stationCode),
                    id=id,
                    stationLatitude=stationLatitude,
                    stationLongitude=stationLongitude,
                    rackTotCnt=rackTotCnt,
                    areaId=areaId_obj,
                )
                b.save()
            except:
                pass    # 2078(id) 대여소 unique constraint failed: area.id 원인 불명
            # except Exception as e:
            #     print(e)
            #     print(item)

except Exception as e:
    print(e)

'''queryset = Area.objects.all()
queryset.delete() # 일괄 delete 요청'''