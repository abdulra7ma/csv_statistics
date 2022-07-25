import csv

from apps.statistics.models import CSVData
from django.db import transaction


def load_csv_data_to_csv_data_model(file_path) -> None:
    with open(file_path, "r") as csv_file:
        data = csv.reader(csv_file, delimiter=",")
        next(data)

        with transaction.atomic():
            for row in data:
                CSVData.objects.create(
                    priority=row[0],
                    type=row[1],
                    aircraft=row[2],
                    status=row[3],
                    _errors_count=row[4],
                    _info_count=row[5],
                )
    return
