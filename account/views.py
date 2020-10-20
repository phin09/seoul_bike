from django.shortcuts import render, redirect
from .models import bikeUser
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.

# 회원 가입
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST" and 'btnform1' in request.POST:
        #회원가입 처리 코드
        # username = request.POST['username']
        # password = request.POST['password']
        # re_password = request.POST['re_password']
        # areaid = request.POST['areaid']

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        areaid = request.POST.get('areaid', None)

        res_data = {}
        try:
            bikeUser.objects.get(username=username)
            res_data['error'] = '중복된 아이디입니다.'

        except bikeUser.DoesNotExist:
            if not (username and password and re_password and areaid):
                res_data['error'] = "모든 정보를 입력해 주세요."
            elif password != re_password:
                res_data['error'] = "비밀번호가 틀립니다. 다시 입력해주세요"
            # 같으면 저장
            else:
                #위 정보들로 인스턴스 생성
                bikeuser = bikeUser(
                    username=username,
                    password=make_password(password),
                    areaid=areaid,
                )
                #저장
                bikeuser.save()
                return redirect('/')
        return render(request, 'register.html', res_data)
    elif request.method == "POST" and 'btnform2' in request.POST:
        return redirect('/')

# 로그인
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST" and 'btnform1' in request.POST:
        # 전송받은 아이디와 비밀번호 확인
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 유효성 처리
        res_data = {}
        if not (username and password):
            res_data['error'] = "아이디를 입력해주세요."
        else:
            # 기존(DB)에 있는 bikeUser 모델과 같은 값인 걸 가져온다.
            try:
                bikeuser = bikeUser.objects.get(username=username)

            #위 정보들로 인스턴스 생성
                if check_password(password, bikeuser.password):
                    request.session['user'] = bikeuser.id
                    return redirect('index/')
                else:
                    res_data['error'] = "가입하지 않은 아이디이거나, 잘못된 비밀번호입니다."
            except bikeUser.DoesNotExist:
                res_data['error'] = '가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.'

        return render(request, 'login.html', res_data)

    elif request.method == "POST" and 'btnform2' in request.POST:
        return redirect('user/register/')

#로그아웃
def logout(request):
    if request.session['user']: #로그인 중이면
       del(request.session['user'])

    return redirect('/') #로그인 페이지로
