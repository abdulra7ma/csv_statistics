from apps.base.model.core import CoreModel
from django.db import models


class StatisticsCSVUploadedFile(CoreModel):
    """
    For uploaded CSV files
    """

    file = models.FileField(upload_to="csv", blank=False, null=True)
    file_hash = models.CharField(verbose_name="File Hash", max_length=256)


class CSVData(CoreModel):
    """
    Stores data from
    """

    priority = models.CharField(verbose_name="Priority", max_length=32)
    type = models.CharField(verbose_name="Type", max_length=32)
    aircraft = models.CharField(verbose_name="Aircraft", max_length=32)
    status = models.CharField(verbose_name="Status", max_length=32)
    _errors_count = models.IntegerField(verbose_name="Errors Count", default=0)
    _info_count = models.IntegerField(verbose_name="Info Count", default=0)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "type",
                ]
            ),
            models.Index(
                fields=[
                    "aircraft",
                ]
            ),
            models.Index(
                fields=[
                    "status",
                ]
            ),
        ]


class Statistics(CoreModel):
    """
    Defines the main attributes for a statistics object
    """

    aircraft = models.CharField(verbose_name="Aircraft", max_length=128, null=True)
    status = models.CharField(verbose_name="Status", max_length=128, null=True)
    type = models.CharField(verbose_name="Type", max_length=128, null=True)
    info_count = models.IntegerField(verbose_name="Info Count", default=0)
    errors_count = models.IntegerField(verbose_name="Errors Count", default=0)
    pre_legend = models.IntegerField(verbose_name="Pre legend", default=0)
    warning = models.IntegerField(verbose_name="Warning", default=0)
    paired_b = models.IntegerField(verbose_name="Paired B", default=0)
    legend = models.IntegerField(verbose_name="Legend", default=0)
    lower_b = models.IntegerField(verbose_name="lower B", default=0)
    repeat_legend = models.IntegerField(verbose_name="Repeat Legend", default=0)
    upper_a = models.IntegerField(verbose_name="Upper A", default=0)
    lower_a = models.IntegerField(verbose_name="Lower A", default=0)
    paired_a = models.IntegerField(verbose_name="paired A", default=0)
