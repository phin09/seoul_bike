import os
import requests
from sys import stdout
from datetime import date, timedelta, datetime
from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from weather.models import Weather


class Command(BaseCommand):
    help = "write weather data to DataBase"

    def handle(self, *args, **kwargs):
        weather_key = os.environ.get("WEATHER_KEY")

        weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst?serviceKey='   # ? : GET 방식

        result_dict = {}   # 조회한 데이터 넣을 dict

        try:
            target_time = datetime.now()
            hour = target_time.strftime('%H')
            minute = target_time.strftime('%M')
            result_dict['hour'] = hour  # table weather에 들어갈 column명
            fcst_time = hour + '00'

            today = date.today().strftime('%Y%m%d')    # 오늘 날짜를 '20201119' 형태로 변환

            # 11시 중 언제 조회하더라도 base time이 1030, fcst_time이 1100이 되도록.
            # base_time이 1100인 데이터는 11:40부터 조회할 수 있음.
            target_time = (target_time - timedelta(hours=1)).strftime('%H') + '30'
            if hour == '00':
                today = (date.today() - timedelta(days=1)).strftime('%Y%m%d') # 어제 날짜

            result_dict['year'] = int(today[:4])    # table weather에 들어갈 column명
            result_dict['month'] = int(today[4:6])  # table weather에 들어갈 column명
            result_dict['day'] = int(today[6:])     # table weather에 들어갈 column명

            weather_query_params = urlencode({
                quote_plus('numOfRows'): 60,
                quote_plus('pageNo'): "1",
                quote_plus('base_date'): today,
                quote_plus('base_time'): target_time,
                quote_plus('nx'): "60",
                quote_plus('ny'): "127",
            })

            weather_url_full = weather_url + weather_key + '&' + weather_query_params

            try:
                response = urlopen(weather_url_full).read()

            except HTTPError or requests.HTTPError as e:
                # urlopen return opener.open(url, data, timeout)로 인한 에러 메세지 보려면 HTTPError 삭제
                self.stdout.write(self.style.ERROR(e))
            else:   # except 실행하지 않았을 경우 실행
                xtree = ET.fromstring(response).find('body').find(
                    'items')  # 트리형태로 변환. items 아래 일시별 item tag 있음
                for item in xtree:  # 조회 결과 items 안의 item들에 각각 항목명과 값 있음
                    if item.find("fcstTime").text == fcst_time:  # 조회 결과 중 가장 이른 시간 예보만 수집
                        category = item.find("category").text   # category 태그 안에 항목명 있음
                        try:
                            val = float(item.find("fcstValue").text)    # 해당 항목의 값
                        except:
                            val = 0  # 결측치일 경우
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
                quote_plus('numOfRows'): "15",
                quote_plus('pageNo'): "1",
                quote_plus('base_date'): today,
                quote_plus('base_time'): fcst_time,
                quote_plus('nx'): "60",
                quote_plus('ny'): "127",
            })

            s06_url_full = s06_url + weather_key + '&' + s06_query_params

            try:
                response = urlopen(s06_url_full).read()
            except HTTPError or requests.HTTPError as e:
                # urlopen return opener.open(url, data, timeout)로 인한 에러 메세지 보려면 HTTPError 삭제
                self.stdout.write(self.style.ERROR(e))
            else:
                xtree = ET.fromstring(response).find('body').find(
                    'items')  # 트리형태로 변환. items 아래 일시별 item tag 있음
                for item in xtree:  # 조회 결과 items 안의 item들에 각각 항목명과 값 있음
                    category = item.find("category").text   # category 태그 안에 항목명 있음
                    if category == 'S06':
                        try:
                            val = float(item.find("fcstValue").text)    # 해당 항목의 값
                        except:
                            val = 0  # 결측치일 경우
                        result_dict[category] = val

            try:
                a = Weather.objects.create(
                    year=result_dict['year'],
                    month=result_dict['month'],
                    day=result_dict['day'],
                    hour=result_dict['hour'],
                    T1H=result_dict['T1H'],   # 기온
                    RN1=result_dict['RN1'],   # 1시간 강수량
                    SKY=result_dict['SKY'],
                    REH=result_dict['REH'],   # 습도
                    PTY=result_dict['PTY'],   # 강수형태
                    VEC=result_dict['VEC'],   # 풍향
                    WSD=result_dict['WSD'],   # 풍속
                    S06=result_dict['S06'],   # 6시간 신적설
                )
                a.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(e))

        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

        self.stdout.write(self.style.SUCCESS("weather data is updated into DB"))
