'''
2020Oct20
전체 대여소를 그룹으로 묶기. 한 그룹당 대여소 20여개.
상시 업데이트하는 용도의 파일이 아니라 회원 관리 쪽에 들어갈 데이터를 만들어두는 용도.
입력 파일 : station_info.csv
출력 파일 : area.csv
출력 형태 : 102 그룹. 한 row가 한 개의 그룹(20여개의 위경도 tuple)
'''
import pandas as pd

df = pd.read_csv( './station_info.csv', encoding = 'utf-8' )

lat_lst_temp = df['stationLatitude'].values.tolist()
lon_lst_temp = df['stationLongitude'].values.tolist()
lat_lon = [(lat_lst_temp[k], lon_lst_temp[k]) for k in range(len(lat_lst_temp))]
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

df_result = pd.DataFrame(result)
df_result.to_csv( 'area.csv', index = False )