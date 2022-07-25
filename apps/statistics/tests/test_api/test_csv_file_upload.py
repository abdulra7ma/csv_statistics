import os

import pytest
from apps.statistics.models import CSVData, StatisticsCSVUploadedFile
from apps.statistics.utils._tests.file_upload import file_upload_csv
from django.urls import reverse
from rest_framework import status

UPLOAD_CSV_FILE_ENDPOINT = reverse("uplaod-csv")


@pytest.mark.django_db
def test_upload_csv_file_success(api_client, django_settings):
    valid_csv_file_path = os.path.join(
        django_settings.PROJECT_ROOT, "apps", "statistics", "tests", "data", "valid_test_file.csv"
    )
    file_data = file_upload_csv(valid_csv_file_path)

    headers = {
        "HTTP_CONTENT_TYPE": "multipart/form-data",
        "HTTP_CONTENT_DISPOSITION": "attachment; filename=" + valid_csv_file_path.split("/")[-1],
    }

    assert StatisticsCSVUploadedFile.objects.count() == 0

    response = api_client.post(UPLOAD_CSV_FILE_ENDPOINT, data={"file": file_data}, **headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert StatisticsCSVUploadedFile.objects.count() == 1

    os.remove(StatisticsCSVUploadedFile.objects.last().file.path)


@pytest.mark.django_db
def test_upload_csv_file_without_including_the_file(api_client):
    response = api_client.post(UPLOAD_CSV_FILE_ENDPOINT)

    assert CSVData.objects.count() == 0
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data["non_field_errors"][0]) == "file not found"
    assert CSVData.objects.count() == 0
