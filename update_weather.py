'''
update table weather
있는 데이터를 갱신하는 게 아니라 쌓는 코드.
이후 table 내 데이터 전부를 하둡으로 옮기는 작업 필요.

매시 45분 이후에 호출해서 시간별 초단기예보 데이터 수집.
target_time 맨 윗줄에 timedelta 넣은 건 45분 이전에 실행한 경우 이전 타임의 데이터를 수집하기 위함
시간 지정해서 자동 실행할 경우에는 삭제하기

사용한 data(출처 명시 필요)
https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15057682
'''

import os
import django
import requests

from datetime import date, timedelta, datetime
from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from bikeapp.models import Weather
from custom import get_secret

weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst?serviceKey='   # ? : GET 방식
weather_key = get_secret('secrets.json', "WEATHER_KEY")

result_dict = {}   # 조회한 데이터 넣을 dict

today = date.today().strftime('%Y%m%d')    # 오늘 날짜를 '20201119' 형태로 변환
result_dict['year'] = int(today[:4])    # table weather에 들어갈 column명
result_dict['month'] = int(today[4:6])  # table weather에 들어갈 column명
result_dict['day'] = int(today[6:])     # table weather에 들어갈 column명

target_time = datetime.now() #- timedelta(hours=1)   # timedelta는 45분 이전 테스트용. 실제 실행 시엔 지우고 실행 시간을 40분 이후로 설정.
fcst_time = (target_time + timedelta(hours=1)).strftime('%H')
result_dict['hour'] = int(fcst_time)   # table weather에 들어갈 column명
fcst_time =  fcst_time + '00'
target_time = target_time.strftime('%H')
target_time = target_time + '30'
# base_time이 1100인 데이터는 11:40부터 조회할 수 있음.

weather_query_params = urlencode({
            quote_plus('numOfRows') : 60,
            quote_plus('pageNo') : "1",
            quote_plus('base_date') : today,
            quote_plus('base_time') : target_time,
            quote_plus('nx') : "60",
            quote_plus('ny') : "127",
         })

weather_url_full = weather_url + weather_key + '&' + weather_query_params
print(weather_url_full)

try:
    response = urlopen( weather_url_full ).read()
except HTTPError or requests.HTTPError as e:
    # urlopen return opener.open(url, data, timeout)로 인한 에러 메세지 보려면 HTTPError 삭제
    print(e)
else:
    xtree = ET.fromstring(response).find('body').find('items')  # 트리형태로 변환. items 아래 일시별 item tag 있음
    for item in xtree:  # 조회 결과 items 안의 item들에 각각 항목명과 값 있음
        if item.find("fcstTime").text == fcst_time: # 조회 결과 중 가장 이른 시간 예보만 수집
            category = item.find("category").text   # category 태그 안에 항목명 있음
            try:
                val = float(item.find("fcstValue").text)    # 해당 항목의 값
            except:
                val = 0 # 결측치일 경우
            result_dict[category] = val

# S06
s06_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey='

target_time = int(datetime.now().strftime('%H'))
if target_time == 0:
    fcst_time = '2300'
elif target_time == 1 or target_time == 2:
    today = (date.today() - timedelta(days=1)).strftime('%Y%m%d')
    fcst_time = '2300'
elif target_time == 3 or target_time == 4 or target_time == 5:
    fcst_time = '0200'
elif target_time == 6 or target_time == 7 or target_time == 8:
    fcst_time = '0500'
elif target_time == 9 or target_time == 10 or target_time == 11:
    fcst_time = '0800'
elif target_time == 12 or target_time == 13 or target_time == 14:
    fcst_time = '1100'
elif target_time == 15 or target_time == 16 or target_time == 17:
    fcst_time = '1400'
elif target_time == 18 or target_time == 19 or target_time == 20:
    fcst_time = '1700'
elif target_time == 21 or target_time == 22 or target_time == 23:
    fcst_time = '2000'

s06_query_params = urlencode({
            quote_plus('numOfRows') : "15",
            quote_plus('pageNo') : "1",
            quote_plus('base_date') : today,
            quote_plus('base_time') : fcst_time,
            quote_plus('nx') : "60",
            quote_plus('ny') : "127",
         })

s06_url_full = s06_url + weather_key + '&' + s06_query_params
print(s06_url_full)

try:
    response = urlopen( s06_url_full ).read()
except HTTPError or requests.HTTPError as e:
    # urlopen return opener.open(url, data, timeout)로 인한 에러 메세지 보려면 HTTPError 삭제
    print(e)
else:
    xtree = ET.fromstring(response).find('body').find('items')  # 트리형태로 변환. items 아래 일시별 item tag 있음
    for item in xtree:  # 조회 결과 items 안의 item들에 각각 항목명과 값 있음
        category = item.find("category").text   # category 태그 안에 항목명 있음
        if category == 'S06':
            try:
                val = float(item.find("fcstValue").text)    # 해당 항목의 값
            except:
                val = 0 # 결측치일 경우
            result_dict[category] = val


try:
    a = Weather.objects.create(
        year=result_dict['year'],
        month=result_dict['month'],
        day=result_dict['day'],
        hour=result_dict['hour'],
        T1H=result_dict['T1H'],   # 기온
        RN1=result_dict['RN1'],   # 1시간 강수량
        REH=result_dict['REH'],   # 습도
        PTY=result_dict['PTY'],   # 강수형태
        VEC=result_dict['VEC'],   # 풍향
        WSD=result_dict['WSD'],   # 풍속
        S06=result_dict['S06'],   # 6시간 신적설
    )
    a.save()
except Exception as e:
    print(e)


# queryset = Weather.objects.all()
# queryset.delete() # 일괄 delete 요청