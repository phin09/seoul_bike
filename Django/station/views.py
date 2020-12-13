import json

from django.shortcuts import render
from django.core.serializers import serialize 
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse, JsonResponse

from . import models 
from bikemap import models as bikemap_models
from core import models as core_models
# Create your views here.
def stationInfo(request):
    pk = request.POST.get('pk')
    station = models.Stations.objects.get(pk=pk)
    parkTot = bikemap_models.StationNow.objects.values_list('parkingBikeTotCnt', 'created_at', named=True).filter(station=station)
    parkTot = parkTot.order_by('created_at').last()
    parkTot = json.dumps(parkTot, cls=DjangoJSONEncoder)
    #object 유무에 따른 에러처리
    ser_station = serialize('json', [station,])
    
    
    return JsonResponse({'station' : ser_station, 'parkTot':parkTot})