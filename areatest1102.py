import sqlite3
import pandas as pd
import os, json, requests, time
from seoulbike.settings import BASE_DIR
from django.core.exceptions import ImproperlyConfigured

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        # print("check: ", secrets[setting])
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable in secrets.json".format(setting)
        raise ImproperlyConfigured(error_msg)


SEOUL_KEY = get_secret("SEOUL_KEY")

api_urls = ["http://openapi.seoul.go.kr:8088/" + SEOUL_KEY + "/json/bikeList/1/1000",
            "http://openapi.seoul.go.kr:8088/" + SEOUL_KEY + "/json/bikeList/1001/2000",
            "http://openapi.seoul.go.kr:8088/" + SEOUL_KEY + "/json/bikeList/2001/3000"
            ]

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


#seoulbike = pd.read_csv("./station_info.csv", encoding="utf-8")
seoulbike['id'] = seoulbike['stationName'].str.split('.').str[0]
seoulbike = seoulbike.astype({'id':int})
station_area = pd.read_csv("./MergedStation_info.csv", encoding="utf-8")
station_area = station_area.drop(station_area.columns[[0, 2, 3]], axis=1)
station_area = station_area.fillna(0)
station_area = station_area.astype({'cluster':int})
#print(seoulbike.info())
print(station_area.info())
st_user = pd.merge(seoulbike, station_area, on="id", how="left")
#st_user = st_user.drop(st_user.columns[[9, 10, 11]], axis=1)   # api 끌어와서 바로 사용했을 경우 - unnamed, 중복 열 삭제
print(st_user.info())
con = sqlite3.connect('./db.sqlite3')
st_user.to_sql('station', con, if_exists='replace')
con.commit()
cur = con.cursor()
query = cur.execute(("select * from station where cluster=1"))
cols = [column[0] for column in query.description]
bike_load = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
con.close()
st_dict = bike_load.to_dict(orient='records')
#print(st_dict)



'''stationUser = pd.read_csv("stationUser.csv", encoding="utf-8")
st_user = pd.merge(seoulbike, stationUser, on="stationId")
st_user_result = st_user[st_user["areaid"] == int(1)]
st_dict = st_user_result.to_dict(orient='records')
max = st_user_result.iloc[[0, 1, 2, 3, 4]]
st_max = max.to_dict(orient='records')
min = st_user_result.iloc[[-1, -2, -3, -4, -5]]
st_min = min.to_dict(orient='records')

print(st_user_result.info())
print(st_dict)'''
