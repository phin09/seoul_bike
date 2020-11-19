'''
create table subway_tot

subwayTot.csv애서 dataid(id), month, day, tot_getoff, tot_ride
'''

import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from bikeapp.models import SubwayTot

subway_tot_df = pd.read_csv('subwayProperties.csv')

for i in range(subway_tot_df.shape[0]):
    dataId = int(subway_tot_df['id'][i])
    month = int(subway_tot_df['month'][i])
    hour = int(subway_tot_df['hour'][i])
    SubGetoff = int(subway_tot_df['SubGetoff'][i])
    SubRide = int(subway_tot_df['Subride'][i])

    try:
        a = SubwayRid.objects.create(
            dataId=dataId,
            month=month,
            day=day,
            tot_getoff=tot_getoff,
            tot_ride=tot_ride,
        )
        a.save()
    except:
        pass


# queryset = SubwayTot.objects.all()
# queryset.delete() # 일괄 delete 요청