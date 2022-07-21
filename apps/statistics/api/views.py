from apps.statistics.api.serializers import (
    StatisticsCSVUploadedFileSerializer, StatisticsSerializer)
from apps.statistics.models import Statistics
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FileUploadParser, MultiPartParser


class UplaodCSVView(generics.CreateAPIView):
    serializer_class = StatisticsCSVUploadedFileSerializer
    parser_classes = (MultiPartParser, FileUploadParser)


class StatisticsView(generics.ListAPIView):
    serializer_class = StatisticsSerializer
    pagination_class = LimitOffsetPagination
    queryset = Statistics.objects.all()

    def get_queryset(self):
        return super().get_queryset()
