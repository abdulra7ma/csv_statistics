from apps.statistics.api.filters import StatisticsFilter
from apps.statistics.api.serializers import StatisticsCSVUploadedFileSerializer, StatisticsSerializer
from apps.statistics.models import Statistics
from django_filters import rest_framework as filters
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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StatisticsFilter
