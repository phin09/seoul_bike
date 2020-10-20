#
# import os
# import django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
# django.setup()
#
#
# from django.contrib.auth.models import User
#
#
# from bikeapp.models import station
# from account.models import bikeUser
#
# station = station.objects.all()
# print(station)
#
# for i in range(df.shape[0]):
#
#     address = df['대여소주소'][i]
#     lattitude = float(df['위도'][i])
#     longitude = float(df['경도'][i])
#     max_hold = int(extractNumber(df['거치대수'][i]))
#     date = extractDate(df['기준시작일자'][i])
#
#     try:
#         bikeUser.objects.create(
#             id=i,
#             address=address,
#             lattitude=lattitude,
#             longitude=longitude,
#             max_hold=max_hold,
#         )
#     except:
#         pass