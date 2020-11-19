# seoul_bike
django project for the Seoul public bicycle system  
&nbsp;  

**환경**   
Windows / Python 3.7 / Pycharm 2020.1 / pipenv / Django 3.1   
&nbsp;  

** 자동 실행 설정할 파일**   
10분마다: update_station_now_and_daily_station.py   
1시간마다(매 50분): update_weather.py
하루마다: table daily_station -> table station_to_stack 전처리. 모델 업데이트용 데이터 넣기
&nbsp;  

**DB 완전 초기화의 경우**   
* 삭제할 것   
db.sqlite3(sqlite3.exe 아님), app들 안에 있는 pycache, migrations 폴더
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py makemigrations (앱이름)
$ python manage.py migrate
```
* 초기 데이터 넣기 - 각 1회만 실행   
create_users.py   
create_station_now.py   
create_area.py   
* table 내 데이터 삭제시 주의   
삭제 후 fk 관계에 주의해 삭제한 table과 CASCADE 걸려있는 table의 create 파일 실행   