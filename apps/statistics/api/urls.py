# Django imports
from django.urls import path
from apps.statistics.api.views import UplaodCSVView, StatisticsView, ExportStatistics


urlpatterns = [
    path("upload-csv", UplaodCSVView.as_view(), name="uplaod-csv"),
    path("export-csv", ExportStatistics.as_view(), name="uplaod-csv"),
    path("", StatisticsView.as_view(), name="statistics"),
]
