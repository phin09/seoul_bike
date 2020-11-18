from django.shortcuts import render
from django.forms import model_to_dict

from account.models import Users
from bikeapp.models import StationNow, Area
from custom import get_secret
from django.http import HttpResponse

def bikeMap(request):
    # 로그인 session
    global user_area
    user_id = request.session.get('user').split('e')[1]   # login시 입력한 아이디 값에서 숫자 추출
    if user_id: # login시 입력한 아이디 값과 primary key(username)가 일치하는 object를 [dict]로 가져옴
        user_area_lst = [model_to_dict(user) for user in Users.objects.filter(pk=user_id)]
        user_area = user_area_lst[0]['areaId']   # areaId from table users

    # map.html로 넘길 kakao api key 불러오기
    # KAKAO_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret('secrets.json', "KAKAO_KEY")
    KAKAO_SERVICES_KEY = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + get_secret('secrets.json',
        "KAKAO_KEY") + "&libraries=services,clusterer,drawing"

    # st_dict는 지속적으로 업데이트 되는 값(parkingBikeTotCnt), fixed_dict는 위경도 등의 고정값
    queryset_area = Area.objects.filter(areaId=user_area)
    fixed_dict = [model_to_dict(query) for query in queryset_area]    # list of dicts
    st_dict = []    # list of dicts
    for item in fixed_dict:
        query = StationNow.objects.filter(pk=item['stationCode'])
        st_dict = st_dict + list(query.values('stationName', 'parkingBikeTotCnt', 'stationCode'))

    payload = [(f, s) for f, s in zip(fixed_dict, st_dict)]
    
    # 데이터 업데이트를 위해서 shared, 예측값 등 출력할 column 추가해야 됨
    # return HttpResponse(st_dict)

    # 임시
    st_plus = st_dict[:5]
    st_minus = st_dict[-5:]

    return render(request, 'index.html', {'api_dict': payload,
                                          'kakao_service_key': KAKAO_SERVICES_KEY,
                                          'st_plus': st_plus, 'st_minus': st_minus})
