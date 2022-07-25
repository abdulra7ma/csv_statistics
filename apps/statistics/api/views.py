from apps.statistics.api.serializers import (
    StatisticsCSVUploadedFileSerializer, StatisticsSerializer)
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
        results = CSVData.objects.raw(
            """
            SELECT
                1 as uuid,
                "statistics_csvdata"."aircraft",
                "statistics_csvdata"."type",
                "statistics_csvdata"."status",
                SUM("statistics_csvdata"."_info_count") AS "info_count",
                SUM("statistics_csvdata"."_errors_count") AS "errors_count",
                COUNT("statistics_csvdata"."type") FILTER (
                WHERE
                "statistics_csvdata"."type" = 'PreLegend') AS "pre_legend",
                COUNT("statistics_csvdata"."type") FILTER (
                WHERE
                "statistics_csvdata"."type" = 'Warning') AS "warning",
                COUNT("statistics_csvdata"."type") FILTER (
                WHERE
                "statistics_csvdata"."type" = 'Paired B') AS "paired_b",
                COUNT("statistics_csvdata"."type") FILTER (
                WHERE
                "statistics_csvdata"."type" = 'Legend') AS "legend",
                COUNT("statistics_csvdata"."type") FILTER (
                WHERE
                "statistics_csvdata"."type" = 'Lower B') AS "lower_b",
                COUNT("statistics_csvdata"."type") FILTER (
                WHERE
                "statistics_csvdata"."type" = 'Repeat Legend') AS "repeat_legend",
                COUNT("statistics_csvdata"."type") FILTER (
                WHERE
                "statistics_csvdata"."type" = 'Upper A') AS "upper_a",
                COUNT("statistics_csvdata"."type") FILTER (
                WHERE
                "statistics_csvdata"."type" = 'Lower A') AS "lower_a",
                COUNT("statistics_csvdata"."type") FILTER (
                WHERE
                "statistics_csvdata"."type" = 'Paired A') AS "paired_a" 
            FROM
                "statistics_csvdata" 
            GROUP BY
                GROUPING SETS ("statistics_csvdata"."aircraft", "statistics_csvdata"."type", "statistics_csvdata"."status")
            """
        )

        return results
