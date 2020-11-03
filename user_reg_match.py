'''
2020Oct20
전체 대여소를 그룹으로 묶기. 한 그룹당 대여소 20여개.
상시 업데이트하는 용도의 파일이 아니라 회원 관리 쪽에 들어갈 데이터를 만들어두는 용도.
입력 파일 : station_info.csv
출력 파일 : area.csv
출력 형태 : 102 그룹. 한 row가 한 개의 그룹(20여개의 위경도 tuple)
'''
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
import pandas as pd

df = pd.read_csv( './station_info.csv', encoding = 'utf-8' )

lat_lst_temp = df['stationLatitude'].values.tolist()
lon_lst_temp = df['stationLongitude'].values.tolist()
st_temp = df['stationId'].values.tolist()
lat_lon = [(lat_lst_temp[k], lon_lst_temp[k], st_temp[k]) for k in range(len(lat_lst_temp))]
lat_lst = sorted(lat_lon, key = lambda x : x[0])
lon_lst = sorted(lat_lon, key = lambda x : x[1])

result = []
flag = False
while True:
    temp = []
    while True:
        temp.append(lat_lst.pop(0))
        temp.append(lon_lst.pop(0))
        if len(set(temp)) >= 20: break
        if len(lat_lst) < 20:
            temp.extend(lat_lst)
            flag = True
            break
        lst_int = list(set(lat_lst) & set(lon_lst))
        lat_lst = sorted(lst_int, key=lambda x: x[0])
        lon_lst = sorted(lst_int, key=lambda x: x[1])
    result.append(list(set(temp)))
    if flag: break

area = pd.DataFrame(result)
# print(area)
# area = pd.read_csv("area.csv", encoding="utf-8")
user_area = pd.DataFrame(columns=['areaid', 'value'])
for i in range(len(area.columns)):
    for j in range(len(area)):
        user_area = user_area.append(pd.DataFrame([[j+1, area.iloc[j][i]]], columns=['areaid', 'value']))

user_area = user_area.astype({'value': 'str'})
# print(user_area)
user_area['value'] = user_area['value'].str.split('(').str[1]
user_area['value'] = user_area['value'].str.split(')').str[0]
user_area['stationLatitude'] = user_area['value'].str.split(', ').str[0]
user_area['stationLongitude'] = user_area['value'].str.split(', ').str[1]
user_area['stationId'] = user_area['value'].str.split(', ').str[2]
user_area['stationId'] = user_area['stationId'].str.split("'").str[1]
# 데이터프레임 타입 변경
user_area = user_area.astype({'areaid': 'int', 'stationLatitude': 'float', 'stationLongitude': 'float'})
# user_area.to_csv('area_id.csv', index=False)
# print(user_area.index)

# bikeuser
from django.forms import model_to_dict
from account.models import bikeUser
station = [model_to_dict(station) for station in bikeUser.objects.all()]
bikeuser = pd.Data Frame(station)
# 데이터프레임 타입 변경
bikeuser = bikeuser.astype({'areaid': 'int'})

stationUser = pd.merge(bikeuser, user_area,  on='areaid')
stationUser = stationUser.dropna(axis=0)
stationUser = stationUser.reset_index()
stationUser = stationUser[['username', 'areaid', 'stationId']]
stationUser.to_csv('./bikeapp/stationUser.csv', index=False, encoding="utf-8")
print(stationUser)

station_info = pd.read_csv( './station_info.csv', encoding='utf-8')

st_user = pd.merge(station_info, stationUser, on="stationId")
print(st_user)
st_user.to_csv('st_user.csv', index=False, encoding="utf-8")
# print(stationUser.info())


