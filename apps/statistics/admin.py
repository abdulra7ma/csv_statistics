# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Statistics, StatisticsCSVUploadedFile


@admin.register(StatisticsCSVUploadedFile)
class StatisticsCSVUploadedFileAdmin(admin.ModelAdmin):
    list_display = ("uuid", "created", "updated", "is_active", "file", "file_hash")
    list_filter = ("created", "updated", "is_active")


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "created",
        "updated",
        "is_active",
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
    )
    list_filter = ("created", "updated", "is_active")
