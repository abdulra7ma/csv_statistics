import os

from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.statistics.models import CSVData, Statistics, StatisticsCSVUploadedFile
from apps.statistics.statistics import FLightStatistics
from apps.statistics.utils.file_hash import generate_file_hash
from apps.statistics.utils.load_data import load_csv_data_to_csv_data_model


@receiver(post_save, sender=StatisticsCSVUploadedFile)
@transaction.atomic
def apply_statistics_over_csv_file_after_creation(sender, instance, created, **kwargs) -> None:
    """
    Runs the FLightStatistics class after the creation of StatisticsCSVUploadedFile instance
    """

    if created:
        file_hash = generate_file_hash(instance.file.path)
        file_hash_similar_objs = StatisticsCSVUploadedFile.objects.filter(file_hash=file_hash)

        # if there are  similar hashs with the newly created hash
        # that's obviously mean we have generate statictics for such a file before
        # so there is no need to perform such calculations again
        if not file_hash_similar_objs.exists():
            csv_file_path = instance.file.path
            loaded_objects_ids = load_csv_data_to_csv_data_model(csv_file_path)

            # calculate the statistics over new loaded data
            query_set = CSVData.objects.raw(
                f"""
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
                    WHERE "statistics_csvdata"."uuid" in ({", ".join(loaded_objects_ids)})
                    GROUP BY
                        GROUPING SETS ("statistics_csvdata"."aircraft", "statistics_csvdata"."type", "statistics_csvdata"."status")
                """
            )

            # get all Statistics model fields to facilitate the values extraction from the query_set
            csv_data_fields = [
                f.name
                for f in Statistics._meta.fields
                if str(f.name)
                not in [
                    "uuid",
                    "is_active",
                    "updated",
                    "created",
                ]
            ]
            
            # dictionary where the key is query_set obj' aircraft attribute
            # and the value is all query_set obj' columns, it facilitates the exraction process
            # of the columns' values from the newly generate query_set, and works as map structure
            # so we can easilly update the existing aircafts rows
            query_set_aircrafts = {}

            for obj in query_set:
                query_set_aircrafts[obj.aircraft] = {}
                for field in csv_data_fields:
                    query_set_aircrafts[obj.aircraft][field] = getattr(obj, field)

            # if it was the first time to upload a file to the database that it will
            # create directely a new Statistics objects
            if Statistics.objects.exists():
                new_stats_objs = []
                aircrafts = {aircraft_value[0] for aircraft_value in Statistics.objects.values_list("aircraft")}

                for key in query_set_aircrafts:
                    if key in aircrafts:
                        Statistics.objects.filter(aircraft=key).update(
                            info_count=F("info_count") + query_set_aircrafts[key]["info_count"],
                            errors_count=F("errors_count") + query_set_aircrafts[key]["errors_count"],
                            pre_legend=F("pre_legend") + query_set_aircrafts[key]["pre_legend"],
                            warning=F("warning") + query_set_aircrafts[key]["warning"],
                            paired_b=F("paired_b") + query_set_aircrafts[key]["paired_b"],
                            legend=F("legend") + query_set_aircrafts[key]["legend"],
                            lower_b=F("lower_b") + query_set_aircrafts[key]["lower_b"],
                            repeat_legend=F("repeat_legend") + query_set_aircrafts[key]["repeat_legend"],
                            upper_a=F("upper_a") + query_set_aircrafts[key]["upper_a"],
                            lower_a=F("lower_a") + query_set_aircrafts[key]["lower_a"],
                            paired_a=F("paired_a") + query_set_aircrafts[key]["paired_a"],
                        )
                    else:
                        new_stats_objs.append(Statistics(**query_set_aircrafts[key]))

                Statistics.objects.bulk_create(new_stats_objs)
            else:
                Statistics.objects.bulk_create(
                    [Statistics(**query_set_aircrafts[key]) for key in query_set_aircrafts.keys()]
                )
