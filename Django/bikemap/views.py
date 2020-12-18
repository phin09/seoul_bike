# pylint: skip-file

import os
import joblib
import pickle
import random
from collections import namedtuple

import lightgbm
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from django.utils import timezone
from django.http import HttpResponse
from django.forms import model_to_dict
from django.shortcuts import render

# from user.models import Users
# from .models import StationNow, Area, SubwayRideGetoff, SubwayTot, Weather

from station.models import Stations
from bikemap.models import StationNow
from weather.models import Weather


def main(request):

    KAKAO_API_KEY = os.environ.get("KAKAO_KEY")

    # st_dict는 지속적으로 업데이트 되는 값(parkingBikeTotCnt), fixed_dict는 위경도 등의 고정값니다
    areaId = int(request.session.get('user')[4:])
    stations = Stations.objects.filter(areaId=areaId)
    parkTot = [StationNow.objects.filter(station=station).order_by('created_at').last() for station in stations]
   

    return render(request, 'bikemap/main.html', context={
        'kakao_api_key': KAKAO_API_KEY,
        'bikeCounts' : parkTot
    })
    
    # # 데이터 업데이트를 위해서 shared, 예측값 등 출력할 column 추가해야 됨

    # ''' Prediction '''
    # # Value order
    # '''
    # 'hour', 'year', 'month', 'day', 
    # 'ta', 'rn', 'ws', 'wd', 'hm', 'ss', 'icsr', 'dsnw', 'hr3Fhsc', 
    # 'rackTotCnt', 'stationLatitude', 'stationLongitude', 'pop_total', 'distance_subway', 
    # 'tot_ride', 'tot_getoff', 'SubwayRide', 'SubwayGetoff'
    # '''

    # now = timezone.localtime()

    # date = [now.hour, now.year, now.month, now.day]

    # Id = [area.dataId for area in queryset_area]

    # weather = Weather.objects.filter(
    #     year=now.year,
    #     month=now.month,
    #     day=now.day,
    #     hour=now.hour+1
    # )
    # if not weather:
    #     weather = Weather.objects.filter(
    #         year=now.year,
    #         month=now.month,
    #         day=now.day,
    #         hour=now.hour+1
    #     )[0]
    # else:
    #     weather = weather[0]

    # ta = weather.T1H  # 온도
    # rn = weather.RN1  # 강수량
    # ws = weather.WSD  # 풍속
    # wd = weather.VEC  # 풍향
    # hm = weather.REH  # 습도
    # ss = 1/(weather.SKY+1)
    # icsr = 0  # 일사량 데이터를 구할 수 없음
    # dsnw = weather.RN1  # 강수량(눈)
    # hr3Fhsc = weather.S06  # 6시간 신적설량

    # FP = weather.PTY  # Form of Precipitation

    # '''
    # FP(Form of Precipitation)
    # 없음(0), 비(1), 비/눈(2),, 소나기(4), 빗방울(5)
    # 눈(3), 빗방울/눈날림(6), 눈날림(7) 여기서 비/눈은 비와 눈이 섞여 오는 것을 의미 (진눈개비)
    # '''
    # w = [ta, rn, ws, wd, hm, ss, icsr, 0, hr3Fhsc] if FP in [
    #     1, 2, 4, 5] else [ta, 0, ws, wd, hm, ss, icsr, dsnw, hr3Fhsc]

    # Prop = []
    # for i in Id:
    #     geo = Area.objects.filter(dataId=i)
    #     subT = SubwayTot.objects.filter(dataId=i, month=now.month, day=now.day)
    #     subRG = SubwayRideGetoff.objects.filter(
    #         dataId=i, month=now.month, hour=now.hour)

    #     geoTuple = namedtuple('geo', ('rackTotCnt', 'stationLatitude',
    #                                   'stationLongitude', 'PopTot', 'distance_subway'))
    #     subTuple = namedtuple('subT', ('tot_ride', 'tot_getoff'))
    #     rgTuple = namedtuple('subRG', ('SubGetoff', 'SubRide'))

    #     geo = geo[0] if geo else geoTuple(0, 0, 0, 0)
    #     subT = subT[0] if subT else subTuple(0, 0)
    #     subRG = subRG[0] if subRG else rgTuple(0, 0)

    #     Prop.append([geo.rackTotCnt,
    #                  geo.stationLatitude,
    #                  geo.stationLongitude,
    #                  geo.PopTot,
    #                  geo.distance_subway,
    #                  subT.tot_ride,
    #                  subT.tot_getoff,
    #                  subRG.SubGetoff,
    #                  subRG.SubRide])

    # Prop = [w + p for p in Prop]
    # cols = ['ta',
    #         'rn',
    #         'ws',
    #         'wd',
    #         'hm',
    #         'ss',
    #         'icsr',
    #         'dsnw',
    #         'hr3Fhsc',
    #         'rackTotCnt',
    #         'stationLatitude',
    #         'stationLongitude',
    #         'pop_total',
    #         'distance_subway',
    #         'tot_ride',
    #         'tot_getoff',
    #         'SubwayRide',
    #         'SubwayGetoff']

    # scaler = joblib.load('./Model/scaler.sav')
    # ScaledProp = scaler.transform(Prop)

    # inputs = [date + list(p) for p in Prop]

    # rentModel = joblib.load('./Model/RentModel.pkl')
    # returnModel = joblib.load('./Model/ReturnModel.pkl')

    # predRent = rentModel.predict(inputs)
    # predReturn = returnModel.predict(inputs)
    # predAmount = np.around(predReturn - predRent)

    # payload = [(f, s, int(pred))
    #            for f, s, pred in zip(fixed_dict, st_dict, predAmount)]

    # st_plus = st_dict[:5]
    # st_minus = st_dict[-5:]

    # return render(request, 'index.html', {'api_dict': payload,
    #                                       'kakao_service_key': KAKAO_SERVICES_KEY,
    #                                       'st_plus': st_plus,
    #                                       'st_minus': st_minus})
