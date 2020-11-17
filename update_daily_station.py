'''
update table daily_station
update_station_now 이후에 돌리기(매 10분)
'''

import os
import django
from django.shortcuts import get_object_or_404
from django.utils import dateformat, timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()
from seoulbike.settings import BASE_DIR
from bikeapp.models import StationNow, DailyStation, Area

try:
    queryset = StationNow.objects.all()
    for item in queryset:
        stationCode = item.stationCode
        # matching query does not exist 방지
        check = Area.objects.filter(stationCode=stationCode)
        if len(check) > 0:
            id = get_object_or_404(Area, stationCode=stationCode)
            parkingBikeTotCnt = int(item.parkingBikeTotCnt)
            formatted_date = dateformat.format(timezone.localtime(item.created_at), 'Y-m-d H:i')
            try:
                c = DailyStation.objects.create(
                    dataId=id,
                    parkingBikeTotCnt=parkingBikeTotCnt,
                    created_at=formatted_date,
                )
                c.save()
            except Exception as e:
                print(e)
        else:
            pass

except Exception as e:
    print(e)

# queryset = DailyStation.objects.all()
# queryset.delete() # 일괄 delete 요청