'''
update table station_now
10분마다 돌리기
'''

import os, json, requests
import django
import django
from django.core.exceptions import ImproperlyConfigured

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from seoulbike.settings import BASE_DIR
from bikeapp.models import StationNow, Area

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
                    station_obj.save()
                except Exception as e:
                    print(e)

            except Area.DoesNotExist:   # 대여소가 api에는 있지만 table area에 없는 경우 -> pass
                pass
        # 대여소가 table area에는 있지만 api에는 없는 경우 -> table에 아예 들어가지 않음

except Exception as e:
    print(e)