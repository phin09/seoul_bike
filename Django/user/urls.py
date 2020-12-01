from django.urls import path
from . import views

app_naame = "user"
urlpatterns = [
    # path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
