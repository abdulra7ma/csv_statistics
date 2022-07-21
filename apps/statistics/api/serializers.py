# Django imports
import os

from apps.statistics.models import StatisticsCSVUploadedFile
from django.conf import settings
from django.contrib.sites.models import Site

# external imports
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator


class StatisticsCSVUploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsCSVUploadedFile
        fields = ["file"]
        extra_kwargs = {
            "file": {"write_only": True},
        }

    def validate_file(self, file):
        ALLOWED_FILE_FORMATS = ["csv"]


        if file.name.split(".")[-1].lower() not in ALLOWED_FILE_FORMATS:
            raise serializers.ValidationError(
                detail="file format not supported please submit .",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return file
