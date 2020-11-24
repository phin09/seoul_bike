'''
create table subway_tot

subwayTot.csv애서 dataid(id), month, day, tot_getoff, tot_ride
'''



import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from bikeapp.models import SubwayRideGetoff
subway_tot_df = pd.read_csv('subwayProperties.csv')

for i in range(subway_tot_df.shape[0]):
    dataId = int(subway_tot_df['id'][i])
    month = int(subway_tot_df['month'][i])
    hour = int(subway_tot_df['hour'][i])
    SubGetoff = int(subway_tot_df['SubGetoff'][i])
    SubRide = int(subway_tot_df['Subride'][i])
    print(subway_tot_df.iloc[i])
    # try:
    a = SubwayRideGetoff.objects.create(
        dataId=dataId,
        month=month,
        hour=hour,
        SubGetoff=SubGetoff,
        SubRide=SubRide,
    )
    a.save()
    # except:
    #     print('error')
    #     pass


# queryset = SubwayTot.objects.all()
# queryset.delete() # 일괄 delete 요청
