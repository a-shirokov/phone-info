import csv
from contextlib import closing
from itertools import islice

import requests
from django.apps import apps as dj_apps
from django.db import transaction

PhoneNumbering = dj_apps.get_model('phone_numbering', 'PhoneNumbering')


def load_data(source, batch_size=500):
    with closing(requests.get(source, verify=False, stream=True)) as r:
        f = (line.decode('utf-8') for line in r.iter_lines())
        reader = csv.reader(f, delimiter=';', quotechar='"')

        objs = (
            PhoneNumbering(
                code=int(row[0]),
                start=int(row[1]),
                end=int(row[2]),
                count=int(row[3]),
                operator_name=row[4],
                region_name=row[5],
            )
            for row in reader
            if all([row[0].isdigit(),
                    row[1].isdigit(),
                    row[2].isdigit(),
                    row[3].isdigit()])
        )
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break

            with transaction.atomic():
                PhoneNumbering.objects.bulk_create(
                    batch, batch_size
                )
