'''
table station_now에 초기값 넣기

table area에서 areaId
api에서 stationName, parkingBikeTotCnt, stationCode
초기값의 created_at은 model의 default로 자동생성
'''




import json
import os
import requests
import django
from django.shortcuts import get_object_or_404

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from bikeapp.models import StationNow, Area
from custom import get_secret   

SEOUL_KEY = get_secret('secrets.json', "SEOUL_KEY")

api_urls = ["http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1/1000",
                "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1001/2000",
                "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/2001/3000"
                ]

try:
    for api_url in api_urls:
        api_result = requests.get(api_url)
        api_json = json.loads(api_result.content)
        api_dict = api_json["rentBikeStatus"]["row"]

        for item in api_dict:
            stationCode = str(item['stationId'])
            stationName = str(item['stationName'])
            dataId = int(stationName.split('.')[0])
            parkingBikeTotCnt = int(item['parkingBikeTotCnt'])

            try:  # create table station_now data for the first time
                a = StationNow.objects.create(
                    dataId=get_object_or_404(Area, dataId=dataId),
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