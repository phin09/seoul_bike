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


def index(request):
    # 로그인 session
    user_pk = request.session.get('user')
    res_data = {}
    if user_pk:
        bikeuser = bikeUser.objects.get(pk=user_pk)
        res_data["id"] = bikeuser
    return render(request, 'index.html', res_data)

def bikeMap(request):
    # 로그인 session
    user_pk = request.session.get('user')
    res_data = {}
    if user_pk:
        bikeuser = bikeUser.objects.get(pk=user_pk)
        res_data["id"] = bikeuser


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
    KAKAO_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret("KAKAO_KEY")

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

        # sqlite3 db 'station' table에 데이터 반영
        con = sqlite3.connect('./db.sqlite3')
        cur = con.cursor()
        # cur.execute("DELETE FROM station")
        # station table에 데이터 넣기
        seoulbike.to_sql('station', con, if_exists='replace')
        # if_exists = 'fail' : 같은 이름의 Table이 존재할 경우 ValueError 가 남
        # if_exists = 'replace': 같은 이름의 Table이 존재할 경우 기존 Table을 Drop하고 새로운 값을 Insert함
        # if_exists = 'append': 같은 이름의 Table이 존재할 경우 기존 Table에 추가로 새로운 값을 Insert함
        con.commit()
        con.close()

        # sqlite3 db station table에 데이터 검색


        seoulbike.to_csv("test.csv", encoding="cp949")


    except Exception as e:
        api = "Error..."
    # sqlite3 db 'station' table data load
    con = sqlite3.connect('./db.sqlite3')
    cur = con.cursor()
    query = cur.execute(("select * from station"))
    cols = [column[0] for column in query.description]
    bike_load = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    con.close()
    st_dict = bike_load.to_dict(orient='records')

    return render(request, 'map.html', {'api_dict': st_dict, 'kakao_key': KAKAO_KEY, 'res_data': res_data})

