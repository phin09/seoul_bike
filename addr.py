# -*- coding:utf-8 -*-
import pandas as pd
import json
import requests
import time
import sqlite3
import sys
import io
from seoulbike.settings import get_secret

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


## 실시간 대여소 정보 api 데이터 불러오기
SEOUL_KEY = get_secret("SEOUL_KEY")
api_urls = ["http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1/1000",
            "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/1001/2000",
            "http://openapi.seoul.go.kr:8088/"+SEOUL_KEY+"/json/bikeList/2001/3000"
            ]
## json dataframe 전환 및 date 칼럼 추가
try:
    sb = pd.DataFrame()
    for api_url in api_urls:
        api_result = requests.get(api_url)
        api_json = json.loads(api_result.content)
        api_dict = api_json["rentBikeStatus"]["row"]
        api_dp = pd.DataFrame(api_dict)
        sb = pd.concat([sb, api_dp])

    st_dict = sb.to_dict(orient='records')
    st_dict_db = sb.to_dict()
    now = time.localtime()
    now_time = time.strftime("%Y/%m/%d %H:%M:%S", now)
    seoulbike = sb.drop_duplicates("stationId", keep="last")
    seoulbike.insert(7, "date", now_time)
    seoulbike = seoulbike.reset_index()

    seoulbike = seoulbike.drop('index', axis=1)
    seoulbike.to_csv("test.csv", encoding="utf-8")

    # st_dict_db = seoulbike.to_dict()


except Exception as e:
    api = "Error..."
#
# # sqlite3 db 'station' table data load
# con = sqlite3.connect('./db.sqlite3')
# cur = con.cursor()
# query = cur.execute(("select * from station"))
# cols = [column[0] for column in query.description]
# seoulbike = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
# con.close()
# # st_dict = bike_load.to_dict(orient='records')


# 실시간 대여소 좌표 정보를 이용하여 카카오 api로 주소 데이터 받아오기
# count = 0
address = []
region_1depth_name = []
region_2depth_name = []
region_3depth_name = []
main_address_no = []
sub_address_no = []
for i in seoulbike.index:
    x = str(seoulbike.iloc[i][5])
    y = str(seoulbike.iloc[i][4])
    addr = 'x=' + x + '&y=' + y
    #     print(addr)
    url = "https://dapi.kakao.com/v2/local/geo/coord2address.json?" + addr + "&input_coord=WGS84"
    url = url.encode('utf-8')
    headers = {"Authorization": "KakaoAK 64410314a85c61eacee3cb9c01c6ed74"}
    api_test = requests.get(url, headers=headers)

    url_text = json.loads(api_test.text)
    api_meta = url_text["meta"]
    #     print(api_meta)
    api_documents = url_text["documents"]
    #     print(api_documents)
    cs = int(api_meta['total_count'])
    #     print(type(cs))
    if cs == 0:
        address.append('null')
        region_1depth_name.append('null')
        region_2depth_name.append('null')
        region_3depth_name.append('null')
        main_address_no.append('null')
        sub_address_no.append('null')

    else:
        for add in api_documents:
            address.append(add['address']['address_name'])
            region_1depth_name.append(add['address']['region_1depth_name'])
            region_2depth_name.append(add['address']['region_2depth_name'])
            region_3depth_name.append(add['address']['region_3depth_name'])
            main_address_no.append(add['address']['main_address_no'])
            sub_address_no.append(add['address']['sub_address_no'])

address_df = pd.DataFrame({"address_name":address, "region_1depth_name":region_1depth_name, "region_2depth_name":region_2depth_name, "region_3depth_name":region_3depth_name, "main_address_no":main_address_no, "sub_address_no":sub_address_no})
# print(len(name))
# print(len(address))
# print(len(region_1depth_name))
# print(len(region_2depth_name))
# print(len(region_3depth_name))
# print(len(main_address_no))
# print(len(sub_address_no))
# print(address_df)
station_info = pd.concat([seoulbike, address_df], axis=1)
##station name 재정의
station_info['id'] = station_info['stationName'].str.split('.').str[0]
station_info['stationName'] = station_info['stationName'].str.split('.', 1).str[1]
station_info['stationName'] = station_info['stationName'].str.lstrip()
# rackTotCnt : 거치대 수
# stationName : 거치대
# parkingBikeTotCnt : 현재 거치 수
# shared # 거치율
# stationLatitude : 거치대 위도
# stationLongitude : 거치대 경도
# stationId : 거치대 id /
# date : api 받아온 날짜
# address_name : 거치대 주소
# region_1depth_name : 거치대 주소 시
# region_2depth_name : 거치대 주소 구
# region_3depth_name : 거치대 주소 동
# main_address_no : 거치대 주소 주번지
# sub_address_no : 거치대 주소 부번지

## 칼럼 재정의
station_info_save = station_info[['stationId', 'id', 'stationName', 'rackTotCnt', 'stationLatitude', 'stationLongitude', 'address_name', 'region_1depth_name', 'region_2depth_name', 'region_3depth_name', 'main_address_no', 'sub_address_no']]
print(station_info)
station_info_save.to_csv("station_info.csv", encoding="utf-8")
# station_info_save.to_csv("station_info1.csv", encoding="cp949")