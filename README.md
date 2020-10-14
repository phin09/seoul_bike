# seoul_bike
django project   
&nbsp;  

**기준**   
Windows / Python 3.7 / Pycharm 2020.1 / Django 3.1   
python 2가 없고 3만 있는 환경   
$ → 콘솔에서 입력   
&nbsp;  

**pipenv 사용**   
* pip 업그레이드
```
$ python -m pip install --upgrade pip
```
* pipenv 설치
```
$ pip install --user pipenv
```
* 옵션 확인
```
$ pipenv
```
* 가상환경을 만들 프로젝트 폴더로 들어간 뒤 python 3.7 기반 가상환경 설치
```
$ pipenv --python 3.7
```
* 가상환경 실행
```
$ pipenv shell
```
* django, pandas, requests 설치
```
$ pipenv install django 3.1
$ pipenv install pandas
$ pipenv install requests
```
* 가상환경 위치 확인
```
$ pipenv --venv
```
* python interpreter 위치 확인
```
$ pipenv --py
```
또는 가상환경 위치\Scripts\python.exe   
&nbsp;  

**.gitignore 만들기**   
1. 인터넷에서 gitignore.io 들어가기
2. 사용하는 OS, IDE, 언어, 프레임워크(windows, pycharm, python, django) 입력하고 create 버튼 클릭
3. 결과창 내용 전부 복사
4. manage.py가 있는 프로젝트 내 최상위 폴더 경로에 txt 파일 만들고 그 안에 붙여넣기
5. 파일 > 다른 이름으로 저장 > 파일 형식을 모든 파일로 하고 파일 이름은 .gitignore. 로 넣기(gitignore 앞뒤로 . 필수)
6. 4의 txt 파일 삭제(또는 4~6대신 빈 메모장에서 4의 경로로 지정해 5번 형식, 이름대로 저장하기)   
&nbsp;  

**django secret key 분리해서 숨기기**   
https://inma.tistory.com/83 참고   
여기서 만든 secrets.json을 .gitignore에 넣기   
&nbsp;  

**pycharm에서 interpreter 설정**   
* 지정 안 된 프로젝트일 경우(e.g. 다른 사람이 만든 프로젝트를 열기만 함) 상단에 안내라인이 뜸. pipenv가 이미 되어있는 프로젝트의 경우 해당 경로로 설정.
* 이미 다른 interpreter를 사용하던 프로젝트일 경우 File > Settings > Project: > Project Interpreter에서 interpreter 변경. 목록에 안 뜨는 경우 Show all에서 추가하기.
&nbsp;  

**이 repository clone하고 시작하기**   
```
$ git clone https://github.com/phin09/seoul_bike
```
clone하면 곱게 폴더로 묶여서 다운됨. 다운 받은 프로젝트 폴더 안에서 git bash 열기.   
&nbsp;  

