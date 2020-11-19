import os
import time
import joblib
import lightgbm
import pandas as pd
import numpy as np
from django_pandas.io import read_frame

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seoulbike.settings')

import django
django.setup()

from bikeapp.models import StationNow, Area, SubwayTot

a=np.array([
       [ 1.90000000e+01,  2.01700000e+03,  6.00000000e+00,
         1.70000000e+01,  7.09310032e-01, -5.18746724e-02,
         2.45408953e+00,  7.16214646e-01, -7.56275388e-02,
         9.29612816e-01, -2.75663887e-01, -4.45937197e-02,
        -1.04216894e-02,  1.22563920e+00, -1.13818423e+00,
         1.60854724e-01, -4.49490271e-01, -5.93986029e-01,
        -1.53515970e-01,  4.46586263e-01,  2.25155752e-01,
         8.19746334e-01] for i in range9])

start = time.time()
rentModel = joblib.load('../Model/RentModel.pkl')
returnModel = joblib.load('../Model/ReturnModel.pkl')

rentPred = rentModel.predict(a)
returnPred = returnModel.predict(a)

predAmount = np.int32(rentPred - returnPred)
for i in predAmount:
    print(i)
