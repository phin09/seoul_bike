'''
table area에 초기값 넣기

MergedStation_info.csv에서 기준 목록(dataId 필터링)
geoProperties.csv에 없는 대여소가 있으면 제거(dataId 필터링)
api에서 dataId, stationCode, stationLatitude, stationLongitude, rackTotCnt
table users에서 areaId
geoProperties.csv에서 distance_hanriver, distance_bikeroad, distance_subway, distance_school_mid,
                    distance_school_high, distance_school_univ, PopTot
'''

import json
import os
import requests
import django
import pandas as pd
from django.shortcuts import get_object_or_404

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from bikeapp.models import Area
from account.models import Users
from custom import get_secret

# 따릉이 api 호출
SEOUL_KEY = get_secret('secrets.json', "SEOUL_KEY")

api_urls = ["http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1/1000",
                "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1001/2000",
                "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/2001/3000"
                ]
try:
    # insert dataId(id in csv file), areaId data into the table area
    station_area = pd.read_csv("./MergedStation_info.csv", encoding="utf-8")
    station_area = station_area.drop(station_area.columns[[0, 2, 3]], axis=1)
    station_area = station_area.fillna(44)  # 임시 default areaId 값
    station_area = station_area.replace(0, 44)  # 임시 default areaId 값
    station_area = station_area.astype({'cluster': int})
    geo = pd.read_csv('geoProperties.csv')
    set_to_drop = set(station_area['id'].values) - set(geo['id'].values)
    st_lst = list(set(station_area['id'].values) - set_to_drop) # 기준 목록

    for api_url in api_urls:
        api_result = requests.get(api_url)
        api_json = json.loads(api_result.content)
        api_dict = api_json["rentBikeStatus"]["row"]

        for item in api_dict:   # api로부터 긁어오고 기준 목록으로 필터링한 대여소
            stationCode = str(item['stationId'])
            stationName = str(item['stationName'])
            dataId = int(stationName.split('.')[0])
            rackTotCnt = int(item['rackTotCnt'])
            stationLatitude = float(item['stationLatitude'])
            stationLongitude = float(item['stationLongitude'])

            if dataId in st_lst:
                geo_temp = geo[geo['id'] == dataId]
                distance_hanriver = geo_temp['distance_hanriver']
                distance_bikeroad = geo_temp['distance_bikeroad']
                distance_subway = geo_temp['distance_subway']
                distance_school_mid = geo_temp['distance_school_mid']
                distance_school_high = geo_temp['distance_school_high']
                distance_school_univ = geo_temp['distance_school_univ']
                PopTot = geo_temp['PopTot']

                df_temp = station_area[station_area['id'] == dataId]
                cluster = df_temp['cluster']
                # matching query does not exist 방지
                check = Users.objects.filter(areaId=cluster)
                if len(check) > 0:
                    areaId_obj = get_object_or_404(Users, areaId=cluster)
                else:
                    areaId_obj = Users.objects.get(areaId=44)  # 임시 default areaId

                try:    # create table area data for the first time
                    b = Area.objects.create(
                        stationCode=stationCode,
                        dataId=dataId,
                        stationLatitude=stationLatitude,
                        stationLongitude=stationLongitude,
                        rackTotCnt=rackTotCnt,
                        areaId=areaId_obj,
                        distance_hanriver=distance_hanriver,
                        distance_bikeroad=distance_bikeroad,
                        distance_subway=distance_subway,
                        distance_school_mid=distance_school_mid,
                        distance_school_high=distance_school_high,
                        distance_school_univ=distance_school_univ,
                        PopTot=PopTot,
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