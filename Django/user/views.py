from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from . import models

# 사용자 자체 가입을 막고 user_create.py로 102개 계정을 생성함


def login(request):
    if request.method == "GET":
        return render(request, 'user/home.html')

    elif request.method == "POST":
        # 전송받은 아이디와 비밀번호 확인
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 유효성 처리
        context = {}

        if not (username and password):
            context['error'] = "아이디와 비밀번호를 입력해주세요."

        else:
            # 기존(DB)에 있는 Users 모델과 같은 값인 걸 가져온다.
            try:
                user = models.Users.objects.get(username=username)

            # 위 정보들로 인스턴스 생성
                if check_password(password, user.password):
                    # request.session['user'] = bikeuser.id
                    request.session['user'] = user.username
                    return redirect('../main')
                else:
                    context['error'] = "가입하지 않은 아이디이거나, 잘못된 비밀번호입니다."
            except models.Users.DoesNotExist:
                context['error'] = '가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.'

        return render(request, 'user/home.html', context)


# 로그아웃
def logout(request):
    if request.session['user']:  # 로그인 중이면
        del(request.session['user'])

    return redirect('/')  # 로그인 페이지로
