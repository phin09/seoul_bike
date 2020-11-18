# seoul_bike
django project for the Seoul public bicycle system  
&nbsp;  

**환경**   
Windows / Python 3.7 / Pycharm 2020.1 / pipenv / Django 3.1   
&nbsp;  

**실행 순서**   
* db 초기화 한 뒤 각 1회만 실행   
create_users.py   
create_station_now.py   
create_area.py   
* table 내 데이터 삭제시 주의   
users 또는 station_now 데이터를 삭제하면 area의 데이터도 삭제됨. 삭제한 테이블의 create파일 실행하고 create_area.py도 실행할 것.   
* 10분마다 실행   
update_station_now_and_daily_station.py   