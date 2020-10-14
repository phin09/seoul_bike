from django.shortcuts import render
from django.urls import path, include
import pandas as pd
import json
import requests
from time import ctime
import time
# Create your views here.

def index(request):
    return render(request, 'index.html')

def bikeMap(request):
    api_urls = ["http://openapi.seoul.go.kr:8088/736c62634a736b7339376a694c6665/json/bikeList/1/1000",
                "http://openapi.seoul.go.kr:8088/736c62634a736b7339376a694c6665/json/bikeList/1001/2000",
                "http://openapi.seoul.go.kr:8088/736c62634a736b7339376a694c6665/json/bikeList/2001/3000"
                ]
    try:
        seoulbike = pd.DataFrame()
        for api_url in api_urls:
            api_result = requests.get(api_url)
            api_json = json.loads(api_result.content)
            api_dict = api_json["rentBikeStatus"]["row"]
            api_dp = pd.DataFrame(api_dict)
            seoulbike = pd.concat([seoulbike, api_dp])

        st_dict = seoulbike.to_dict(orient='records')
        '''
        모델에 집어넣기
        '''

        # now = time.localtime()
        # now_time = time.strftime("%Y/%m/%d %H:%M:%S", now)
        # seoulbike = seoulbike.drop_duplicates("stationId", keep="last")
        # seoulbike.insert(7, "date", now_time)
        # seoulbike = seoulbike.reset_index()
        # seoulbike = seoulbike.drop('index', axis=1)
        # seoulbike.to_csv("test.csv", encoding="cp949")

    except Exception as e:
        api = "Error..."

    return render(request, 'map.html', {'api': api_result, 'api_dict': st_dict})