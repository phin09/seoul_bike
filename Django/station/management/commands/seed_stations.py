import os
import csv
import json
import requests
import pandas as pd
from sys import stdout

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from user.models import Users
from station.models import Stations


class Command(BaseCommand):
    help = "write stations to DataBase"

    def handle(self, *args, **kwargs):
        SEOUL_KEY = os.environ.get("SEOUL_KEY")

        api_urls = ["http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1/1000",
                    "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1001/2000",
                    "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/2001/3000"
                    ]

        try:
            # insert dataId(id in csv file), areaId data into the table area
            station_area = pd.read_csv(
                "initial_data/MergedStation_info.csv", encoding="utf-8")
            station_area = station_area.drop(
                station_area.columns[[0, 2, 3]], axis=1)
            station_area = station_area.fillna(44)  # 임시 default areaId 값
            station_area = station_area.replace(0, 44)  # 임시 default areaId 값
            station_area = station_area.astype({'cluster': int})

            geo = pd.read_csv('initial_data/geoProperties.csv')
            set_to_drop = set(
                station_area['id'].values) - set(geo['id'].values)
            st_lst = list(
                set(station_area['id'].values) - set_to_drop)  # 기준 목록

            for api_url in api_urls:
                api_result = requests.get(api_url)
                api_json = json.loads(api_result.content)
                api_dict = api_json["rentBikeStatus"]["row"]  # 긁어온 데이터

                for item in api_dict:   # api로부터 긁어오고 기준 목록으로 필터링한 대여소
                    stationCode = str(item['stationId'])
                    stationName = str(item['stationName'])
                    dataId = int(stationName.split('.')[0])
                    rackTotCnt=int(item['rackTotCnt'])
                    stationLatitude=float(item['stationLatitude'])
                    stationLongitude=float(item['stationLongitude'])

                    if dataId in st_lst:
                        geo_temp=geo[geo['id'] == dataId]
                        distance_hanriver=geo_temp['distance_hanriver']
                        distance_bikeroad=geo_temp['distance_bikeroad']
                        distance_subway=geo_temp['distance_subway']
                        distance_school_mid=geo_temp['distance_school_mid']
                        distance_school_high=geo_temp['distance_school_high']
                        distance_school_univ=geo_temp['distance_school_univ']
                        PopTot=geo_temp['PopTot']

                        df_temp=station_area[station_area['id'] == dataId]
                        cluster=df_temp['cluster']
                        # matching query does not exist 방지
                        check=Users.objects.filter(areaId=cluster)
                        if len(check) > 0:
                            areaId_obj=get_object_or_404(
                                Users, areaId=cluster)
                        else:
                            areaId_obj=Users.objects.get(
                                areaId=44)  # 임시 default areaId

                        try:    # create table area data for the first time
                            station=Stations.objects.create(
                                dataId=dataId,
                                stationCode=stationCode,
                                stationName=stationName,
                                stationLatitude=stationLatitude,
                                stationLongitude=stationLongitude,
                                rackTotCnt=rackTotCnt,
                                distance_hanriver=distance_hanriver,
                                distance_bikeroad=distance_bikeroad,
                                distance_subway=distance_subway,
                                distance_school_mid=distance_school_mid,
                                distance_school_high=distance_school_high,
                                distance_school_univ=distance_school_univ,
                                PopTot=PopTot,
                                areaId=areaId_obj,
                            )
                            station.save()
                        except Exception as e:
                            # 2078(id) 대여소 unique constraint failed: area.id 원인 불명

                            self.stdout.write(self.style.ERROR(e))
                        # except Exception as e:
                        #     print(e)
                        #     print(item)

        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

        self.stdout.write(self.style.SUCCESS("all the Stations write into DB"))
