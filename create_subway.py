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

subway_tot_df = pd.read_csv('subwayTot.csv')

for i in range(subway_tot_df.shape[0]):
    dataId = int(subway_tot_df['id'][i])
    month = int(subway_tot_df['month'][i])
    day = int(subway_tot_df['day'][i])
    tot_getoff = float(subway_tot_df['tot_getoff'][i])
    tot_ride = float(subway_tot_df['tot_ride'][i])

    try:
        a = SubwayTot.objects.create(
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