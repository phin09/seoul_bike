import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seoulbike.settings")
django.setup()

from bikeapp.models import station

import pandas as pd


from django.forms import model_to_dict
station = [model_to_dict(station) for station in station.objects.all()]
df = pd.DataFrame(station)
print(df)