from apps.statistics.api.serializers import StatisticsCSVUploadedFileSerializer, StatisticsSerializer
from apps.statistics.models import CSVData
from django.db.models import Count, Q, Sum
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
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        results = []

        fields = ["type", "aircraft", "status"]
        for field in fields:
            results += list(
                CSVData.objects.values(field).annotate(
                    info_count=Sum("_info_count"),
                    errors_count=Sum("_errors_count"),
                    pre_legend=Count("type", filter=Q(type="PreLegend")),
                    warning=Count("type", filter=Q(type="Warning")),
                    paired_b=Count("type", filter=Q(type="Paired B")),
                    legend=Count("type", filter=Q(type="Legend")),
                    lower_b=Count("type", filter=Q(type="Lower B")),
                    repeat_legend=Count("type", filter=Q(type="Repeat Legend")),
                    upper_a=Count("type", filter=Q(type="Upper A")),
                    lower_a=Count("type", filter=Q(type="Lower A")),
                    paired_a=Count("type", filter=Q(type="Paired A")),
                )
            )

        return results