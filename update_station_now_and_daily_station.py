'''
update table station_now, daily_station

daily_station은 station_now의 데이터를 쌓은 table
자동실행 설정 없이 실행 횟수 지정해 daily_station을 csv로 저장하는 코드는 data_to_csv_test.py
'''

import json
import os
import requests
import django
from django.shortcuts import get_object_or_404
from django.utils import dateformat, timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from bikeapp.models import StationNow, Area, DailyStation
from custom import get_secret

# 따릉이 api 호출
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
            stationName = str(item['stationName'])
            dataId = int(stationName.split('.')[0])
            try:  # 대여소가 api에도 table area에도 있는 경우 -> update
                check_obj = Area.objects.get(pk=dataId)
                stationCode = str(item['stationId'])
                parkingBikeTotCnt = int(item['parkingBikeTotCnt'])

                try:  # update table station_now
                    station_obj = StationNow.objects.get(pk=stationCode)
                    station_obj.parkingBikeTotCnt = parkingBikeTotCnt
                    station_obj .created_at = timezone.localtime()
                    station_obj.save()
                except Exception as e:
                    print(e)

            except Area.DoesNotExist:   # 대여소가 api에는 있지만 table area에 없는 경우 -> pass
                pass

except Exception as e:
    print(e)

try:    # update table daily_station
    queryset = StationNow.objects.all()
    for item in queryset:
        stationCode = item.stationCode
        # matching query does not exist 방지
        check = Area.objects.filter(stationCode=stationCode)
        if len(check) > 0:
            dataId = get_object_or_404(Area, stationCode=stationCode)
            parkingBikeTotCnt = int(item.parkingBikeTotCnt)
            formatted_date = dateformat.format(timezone.localtime(item.created_at), 'Y-m-d H:i')
            try:
                c = DailyStation.objects.create(
                    dataId=dataId,
                    parkingBikeTotCnt=parkingBikeTotCnt,
                    created_at=formatted_date,
                )
                c.save()
            except Exception as e:
                print(e)
        else:
            pass

except Exception as e:
    print(e)


# queryset = DailyStation.objects.all()
# queryset.delete() # 일괄 delete 요청
