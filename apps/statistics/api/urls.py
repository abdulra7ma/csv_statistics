# Django imports
from django.urls import path
from apps.statistics.api.views import UplaodCSVView

urlpatterns = [path("upload-csv", UplaodCSVView.as_view(), name="uplaod-csv-api")]
