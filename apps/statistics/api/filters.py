from django_filters import rest_framework as filters
from apps.statistics.models import Statistics


class StatisticsFilter(filters.FilterSet):
    class Meta:
        model = Statistics
        fields = [
            "aircraft",
            "status",
            "type",
            "info_count",
            "errors_count",
            "pre_legend",
            "warning",
            "paired_b",
            "legend",
            "lower_b",
            "repeat_legend",
            "upper_a",
            "lower_a",
            "paired_a",
        ]
