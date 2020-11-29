import csv
from sys import stdout

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

import user.models as user_model

NAME = "USER"

class Command(BaseCommand):
    help = "read user.csv and write to Database"

    def handle(self, *args, **kwargs):
        with open('./users.csv', newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',', quotechar='|')

            for idx, row in enumerate(rows):
                if idx == 0:
                    continue

                login_Id = row[0]
                password = make_password(row[1])
                areaId = int(row[2])

                obj = user_model.Users.objects.create(
                    login_Id=login_Id,
                    password=password,
                    areaId=areaId
                )
                obj.save()

        self.stdout.write(self.style.SUCCESS("all the Users write into DB"))
