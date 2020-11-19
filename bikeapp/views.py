# pylint: skip-file

import joblib

import lightgbm
import random
import numpy as np
from sklearn.preprocessing import StandardScaler

from django.utils import timezone
from django.http import HttpResponse
from django.forms import model_to_dict
from django.shortcuts import render

from account.models import Users
from bikeapp.models import StationNow, Area, SubwayRideGetoff, SubwayTot, Weather

from custom import get_secret
from update_weather import updateWeather


def bikeMap(request):

    # 로그인 session

    global user_area
    user_id = request.session.get('user').split(
        'e')[1]   # login시 입력한 아이디 값에서 숫자 추출
    # login시 입력한 아이디 값과 primary key(username)가 일치하는 object를 [dict]로 가져옴

    if user_id:
        user_area_lst = [model_to_dict(user)
                         for user in Users.objects.filter(pk=user_id)]
        user_area = user_area_lst[0]['areaId']   # areaId from table users

    # map.html로 넘길 kakao api key 불러오기
    # KAKAO_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret('secrets.json', "KAKAO_KEY")
    KAKAO_SERVICES_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + \
        get_secret('secrets.json', "KAKAO_KEY") + \
        "&libraries=services,clusterer,drawing"

    # st_dict는 지속적으로 업데이트 되는 값(parkingBikeTotCnt), fixed_dict는 위경도 등의 고정값
    queryset_area = Area.objects.filter(areaId=user_area)

    fixed_dict = [model_to_dict(query)
                  for query in queryset_area]    # list of dicts
    st_dict = []    # list of dicts
    for item in fixed_dict:
        query = StationNow.objects.filter(pk=item['stationCode'])
        st_dict += list(query.values('stationName',
                                     'parkingBikeTotCnt', 'stationCode'))

    

    # 데이터 업데이트를 위해서 shared, 예측값 등 출력할 column 추가해야 됨

    ''' Prediction '''
    # Value order
    '''
    'hour', 'year', 'month', 'day', 
    'ta', 'rn', 'ws', 'wd', 'hm', 'ss', 'icsr', 'dsnw', 'hr3Fhsc', 
    'rackTotCnt', 'stationLatitude', 'stationLongitude', 'pop_total', 'distance_subway', 
    'tot_ride', 'tot_getoff', 'SubwayRide', 'SubwayGetoff'
    '''

    now = timezone.localtime()

    date = [now.hour, now.year, now.month, now.day]

    Id = [area.dataId for area in queryset_area]

    weather = Weather.objects.filter(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour+1
    )
    if not weather:
        updateWeather()
        weather = Weather.objects.filter(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour+1
        )[0]
    else:
        weather = weather[0]

    ta = weather.T1H  # 온도
    rn = weather.RN1  # 강수량
    ws = weather.WSD  # 풍속
    wd = weather.VEC  # 풍향
    hm = weather.REH  # 습도
    ss = 1/(weather.SKY+1)
    icsr = 0  # 일사량 데이터를 구할 수 없음
    dsnw = weather.RN1  # 강수량(눈)
    hr3Fhsc = weather.S06  # 6시간 신적설량

    FP = weather.PTY  # Form of Precipitation
    '''
    FP(Form of Precipitation)
    없음(0), 비(1), 비/눈(2),, 소나기(4), 빗방울(5)
    눈(3), 빗방울/눈날림(6), 눈날림(7) 여기서 비/눈은 비와 눈이 섞여 오는 것을 의미 (진눈개비)
    '''
    w = [ta, rn, ws, wd, hm, ss, icsr, 0, hrdFhsc] if FP in [
        1, 2, 4, 5] else [ta, 0, ws, wd, hm, ss, icsr, dsnw, hr3Fhsc]

    Prop = []
    for i in Id:
        # geo = Area.objects.filter(dataId=i)[0]
        # subT = SubwayTot.objects.filter(
        #     dataId=i, month=now.month, day=now.day)[0]

        # subRG = SubwayRideGetoff.objects.filter(
        #     dataId=i, month=now.month, hour=now.hour)[0]

        # Prop.append([geo.rackTotCnt,
        #              geo.stationLatitude,
        #              geo.stationLongitude,
        #              geo.PopTot,
        #              geo.distance_subway,
        #              subT.tot_ride,
        #              subT.tot_getoff,
        #              subRG.SubGetoff,
        #              subRG.SubRide
        #              ])
        Prop.append([random.randint(-1000, 1000) / 1000 for i in range(9)])

    inputs = [date + w + p for p in Prop]

    rentModel = joblib.load('./Model/RentModel.pkl')
    returnModel = joblib.load('./Model/ReturnModel.pkl')

    inputs = np.array(inputs)
    predRent = rentModel.predict(inputs)
    predReturn = returnModel.predict(inputs)

    predAmount = np.around(predReturn - predRent)
    print(predAmount)

    payload = [(f, s, int(pred)) for f, s, pred in zip(fixed_dict, st_dict, predAmount)]

    st_plus = st_dict[:5]
    st_minus = st_dict[-5:]

    return render(request, 'index.html', {'api_dict': payload,
                                          'kakao_service_key': KAKAO_SERVICES_KEY,
                                          'st_plus': st_plus, 'st_minus': st_minus})
