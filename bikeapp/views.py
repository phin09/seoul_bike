from django.shortcuts import render, get_object_or_404
import pandas as pd
import os
import json
from seoulbike.settings import BASE_DIR
from django.core.exceptions import ImproperlyConfigured
import requests
import time
import sqlite3
from account.models import Users
from bikeapp.models import StationNow, Area
from django.forms import model_to_dict

from django.http import HttpResponse


def bikeMap(request):
    # 로그인 session
    global user_area
    user_id = request.session.get('user').split('e')[1]   # login시 입력한 아이디 값에서 숫자 추출
    if user_id: # login시 입력한 아이디 값과 primary key(username)가 일치하는 object를 [dict]로 가져옴
        user_area_lst = [model_to_dict(user) for user in Users.objects.filter(pk=user_id)]
        user_area = user_area_lst[0]['areaId']   # areaId from table users

    # api key 불러오기
    secret_file = os.path.join(BASE_DIR, 'secrets.json')
    with open(secret_file) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        try:
            #print("check: ", secrets[setting])
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable in secrets.json".format(setting)
            raise ImproperlyConfigured(error_msg)

    # 따릉이 api 호출
    SEOUL_KEY = get_secret("SEOUL_KEY")

    # map.html로 넘길 kakao api key 불러오기
    #KAKAO_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret("KAKAO_KEY")
    KAKAO_SERVICES_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret("KAKAO_KEY") + "&libraries=services,clusterer,drawing"

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
                id = int(stationName.split('.')[0])
                parkingBikeTotCnt = int(item['parkingBikeTotCnt'])

                try:    # update table station_now
                    station_obj = StationNow.objects.get(pk=stationCode)
                    station_obj.parkingBikeTotCnt = parkingBikeTotCnt
                    station_obj.save()
                except Exception as e:
                    print(e)

    except Exception as e:
        print("Error...")

    queryset = StationNow.objects.all()
    user_stations_dict = [model_to_dict(query) for query in queryset]
    stations_dp = pd.DataFrame(user_stations_dict)

    queryset_area = Area.objects.all()
    station_fixed_value_dict = [model_to_dict(query) for query in queryset_area]
    fixed_dp = pd.DataFrame(station_fixed_value_dict)
    temp_dp = pd.merge(stations_dp, fixed_dp, on="stationCode")
    # 데이터 업데이트를 위해서 shared column 추가해야 됨
    st_dict = temp_dp.to_dict(orient='records')
    # return HttpResponse(st_dict)

    # 임시
    plus = temp_dp.iloc[[0, 1, 2, 3, 4]]
    st_plus = plus.to_dict(orient='records')
    minus = temp_dp.iloc[[-1, -2, -3, -4, -5]]
    st_minus = minus.to_dict(orient='records')
    #print(st_plus)
    return render(request, 'index.html', {'api_dict': st_dict, 'kakao_service_key':KAKAO_SERVICES_KEY,
                                          'st_plus':st_plus, 'st_minus':st_minus})

def stationSearch(request):
     search_key = request.GET['search_key']
     context = {'search_key': search_key}
     return render(request, 'test.html', context)


