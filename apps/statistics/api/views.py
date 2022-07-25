import csv

from apps.statistics.api.filters import StatisticsFilter
from apps.statistics.api.serializers import (
    StatisticsCSVUploadedFileSerializer, StatisticsSerializer)
from apps.statistics.models import Statistics
from django.http import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView


class UplaodCSVView(generics.CreateAPIView):
    """
    Accepts CSV file and save it locally
    """

    serializer_class = StatisticsCSVUploadedFileSerializer
    parser_classes = (MultiPartParser, FileUploadParser)


class StatisticsView(generics.ListAPIView):
    """
    Displays Statistics data
    """

    serializer_class = StatisticsSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = Statistics.objects.all()
    filter_class = StatisticsFilter


class ExportStatistics(APIView):
    """
    Export Statistics QuerySet to CSV File and send it as a Response.
    """

    def get(self, request, *args, **kwargs):
        file_fields = [
            f.name for f in Statistics._meta.fields if str(f.name) not in ["uuid", "is_active", "updated", "created"]
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export.csv"'

        writer = csv.DictWriter(response, fieldnames=file_fields)
        writer.writeheader()

        for row in Statistics.objects.all().values(*file_fields):
            writer.writerow(dict(row))

        return response
