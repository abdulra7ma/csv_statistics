import os

import pytest
from apps.statistics.models import StatisticsCSVUploadedFile, CSVData
from django.core.files import File


@pytest.mark.django_db
def test_csvdata_object_creation(django_settings):
    assert StatisticsCSVUploadedFile.objects.count() == 0
    assert CSVData.objects.count() == 0

    csv_file_path = os.path.join(
        django_settings.PROJECT_ROOT, "apps", "statistics", "tests", "data", "valid_test_file.csv"
    )

    with open(csv_file_path, "rb") as file:
        csv_data = StatisticsCSVUploadedFile.objects.create(file=File(file, name=os.path.basename(file.name)))

    assert StatisticsCSVUploadedFile.objects.count() == 1
    assert CSVData.objects.count() > 0

    os.remove(csv_data.file.path)


@pytest.mark.django_db
def test_csvdata_object_creation_failure():
    assert StatisticsCSVUploadedFile.objects.count() == 0

    with pytest.raises(ValueError) as exc_info:
        StatisticsCSVUploadedFile.objects.create()

    assert str(exc_info.value) == "The 'file' attribute has no file associated with it."
    assert StatisticsCSVUploadedFile.objects.count() == 1
