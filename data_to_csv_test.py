'''
table station_now, daily_station 업데이트하고 daily_station을 csv로 저장
update_station_now_and_daily_station.py 파일에 csv 저장하는 코드를 추가한 것
'''

import os, json, requests
import django
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from django.utils import dateformat, timezone
from time import sleep
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from seoulbike.settings import BASE_DIR
from bikeapp.models import StationNow, Area, DailyStation

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
k=0
for k in range(0, 2):
    try:
        for api_url in api_urls:
            api_result = requests.get(api_url)
            api_json = json.loads(api_result.content)
            api_dict = api_json["rentBikeStatus"]["row"]

            for item in api_dict:
                stationName = str(item['stationName'])
                id = int(stationName.split('.')[0])
                try:  # 대여소가 api에도 table area에도 있는 경우 -> update
                    check_obj = Area.objects.get(pk=id)
                    stationCode = str(item['stationId'])
                    rackTotCnt = int(item['rackTotCnt'])
                    parkingBikeTotCnt = int(item['parkingBikeTotCnt'])
                    stationLatitude = float(item['stationLatitude'])
                    stationLongitude = float(item['stationLongitude'])

                    try:  # update table station_now
                        station_obj = StationNow.objects.get(pk=stationCode)
                        station_obj.parkingBikeTotCnt = parkingBikeTotCnt
                        station_obj .created_at = timezone.localtime()
                        station_obj.save()
                    except Exception as e:
                        print(e)

                except Area.DoesNotExist:   # 대여소가 api에는 있지만 table area에 없는 경우 -> pass
                    pass
            # 대여소가 table area에는 있지만 api에는 없는 경우 -> table에 아예 들어가지 않음

    except Exception as e:
        print(e)

    try:
        queryset = StationNow.objects.all()
        for item in queryset:
            stationCode = item.stationCode
            # matching query does not exist 방지
            check = Area.objects.filter(stationCode=stationCode)
            if len(check) > 0:
                id = get_object_or_404(Area, stationCode=stationCode)
                parkingBikeTotCnt = int(item.parkingBikeTotCnt)
                formatted_date = dateformat.format(timezone.localtime(item.created_at), 'Y-m-d H:i')
                try:
                    c = DailyStation.objects.create(
                        dataId=id,
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

    # sleep(300)

# csv로 저장
with open('testdata.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'parkingBikeTotCnt', 'created_at']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for data in DailyStation.objects.all():
        writer.writerow({'id':int(data.dataId.id), 'parkingBikeTotCnt':data.parkingBikeTotCnt, 'created_at':data.created_at})


# station_now 데이터 일괄 삭제 후에는 create_station_now.py와 create_area.py 한번씩 돌려줘야 함
# queryset = StationNow.objects.all()
# queryset.delete() # 일괄 delete 요청

# queryset = DailyStation.objects.all()
# queryset.delete() # 일괄 delete 요청
