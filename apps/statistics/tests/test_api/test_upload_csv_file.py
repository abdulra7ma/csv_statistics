
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.translation import gettext
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import pytest

UPLOAD_CSV_PATH = reverse("uplaod-csv")


@pytest.mark.django_db
def test_upload_unvalid_csv_file(api_client, mocker):
    file = SimpleUploadedFile("test.csv", content="", content_type="text/csv")

    
