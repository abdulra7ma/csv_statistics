# Django imports
from django.urls import path
from apps.statistics.api.views import UplaodCSVView, StatisticsView

urlpatterns = [
    path("upload-csv", UplaodCSVView.as_view(), name="uplaod-csv-api"),
    path("", StatisticsView.as_view(), name="statistics-api"),
]
