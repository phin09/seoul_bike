from django.shortcuts import render
import pandas as pd
import os
import json
from seoulbike.settings import BASE_DIR
from django.core.exceptions import ImproperlyConfigured
import requests
import time
import sqlite3
from account.models import bikeUser
from django.forms import model_to_dict
from bikeapp.models import station


# def index(request):
#     # 로그인 session
#     user_pk = request.session.get('user')
#     res_data = {}
#     if user_pk:
#         bikeuser = bikeUser.objects.get(pk=user_pk)
#         res_data["id"] = bikeuser
#     return render(request, 'map.html', res_data)

def bikeMap(request):
    # 로그인 session
    user_pk = request.session.get('user')
    print(user_pk)
    if user_pk:
        bikearea = [model_to_dict(bike) for bike in bikeUser.objects.filter(pk=user_pk)]
        bikearea_user = pd.DataFrame(bikearea)

    # print(type(bikearea_user))
    user_area = bikearea_user.iloc[0, 2]
    # print(user_area)
    # bike data 불러오기
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

    SEOUL_KEY = get_secret("SEOUL_KEY")
    # KAKAO_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret("KAKAO_KEY")
    KAKAO_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret("KAKAO_KEY")
    KAKAO_SERVICES_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret("KAKAO_KEY") + "&libraries=services,clusterer,drawing"

    api_urls = ["http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1/1000",
                "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1001/2000",
                "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/2001/3000"
                ]
    try:
        seoulbike = pd.DataFrame()
        for api_url in api_urls:
            api_result = requests.get(api_url)
            api_json = json.loads(api_result.content)
            api_dict = api_json["rentBikeStatus"]["row"]
            api_dp = pd.DataFrame(api_dict)
            seoulbike = pd.concat([seoulbike, api_dp])

        now = time.localtime()
        now_time = time.strftime("%Y/%m/%d %H:%M:%S", now)
        seoulbike = seoulbike.drop_duplicates("stationId", keep="last")
        seoulbike.insert(7, "date", now_time)
        seoulbike = seoulbike.reset_index()
        seoulbike = seoulbike.drop('index', axis=1)
        # print(seoulbike.info())
        # 테스트 나중에 db에서 데이터 불러와야함
        stationUser = pd.read_csv("stationUser.csv", encoding="utf-8")
        # print(stationUser)
        st_user = pd.merge(seoulbike, stationUser, on="stationId")
        # print(st_user.info())
        st_user_result = st_user[st_user["areaid"] == int(user_area)]
        # print(st_user_result)
        st_dict = st_user_result.to_dict(orient='records')
        # print(type(st_dict))
        max = st_user_result.iloc[[0,1,2,3,4]]
        st_max = max.to_dict(orient='records')
        min = st_user_result.iloc[[-1,-2,-3,-4,-5]]
        st_min = min.to_dict(orient='records')


        # # print(st_user)
        # # sqlite3 db 'station' table에 데이터 반영
        # con = sqlite3.connect('./db.sqlite3')
        # cur = con.cursor()
        # # cur.execute("DELETE FROM station")
        # # station table에 데이터 넣기
        # seoulbike.to_sql('station', con, if_exists='replace')
        # # if_exists = 'fail' : 같은 이름의 Table이 존재할 경우 ValueError 가 남
        # # if_exists = 'replace': 같은 이름의 Table이 존재할 경우 기존 Table을 Drop하고 새로운 값을 Insert함
        # # if_exists = 'append': 같은 이름의 Table이 존재할 경우 기존 Table에 추가로 새로운 값을 Insert함
        # con.commit()
        # con.close()

        # sqlite3 db station table에 데이터 검색

        # seoulbike.to_csv("test.csv", encoding="cp949")


    except Exception as e:
    # except:
        pass
    #     api = "Error..."
        # # seoul = [model_to_dict(station) for station in station.objects.all()]
        # # seoulbike = pd.DataFrame(seoul)
        # # print(seoulbike)
        # seoulbike = pd.read_csv("station_info.csv", encoding="utf-8")
        # stationUser = pd.read_csv("stationUser.csv", encoding="utf-8")
        # # print(stationUser)
        # st_user = pd.merge(seoulbike, stationUser, on="stationId")
        # print(st_user.info())
        # st_user_result = st_user[st_user["areaid"] == int(user_area)]
        # # st_user_result.to_csv("st_user_result.csv", encoding="utf-8")
        # print(st_user_result)
        # st_dict = st_user_result.to_dict()
        #
        # print(st_dict.values())
        # return render(request, 'map.html', {'api_dict': st_dict, 'kakao_key': KAKAO_KEY})

    # return render(request, 'map.html', {'api_dict': st_dict, 'kakao_key': KAKAO_KEY, 'res_data': res_data})
    return render(request, 'index.html', {'api_dict': st_dict, 'kakao_key': KAKAO_KEY, 'st_min':st_min, 'st_max': st_max, 'KAKAO_SERVICES_KEY':KAKAO_SERVICES_KEY})


def stationSearch(request):
     search_key = request.GET['search_key']
     context = {'search_key': search_key}
     return render(request, 'test.html', context)


