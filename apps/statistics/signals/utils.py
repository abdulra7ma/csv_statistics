import csv
from typing import List

from apps.statistics.models import CSVData, Statistics
from django.db.models import F
from django.db.models.query import QuerySet


def get_query(ids):
    """
    Prepare the raw query for statistics
    """
    return f"""
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
            WHERE "statistics_csvdata"."uuid" in ({", ".join(ids)})
            GROUP BY
                GROUPING SETS (
                    ("statistics_csvdata"."aircraft"),
                    ("statistics_csvdata"."type"), 
                    ("statistics_csvdata"."status"),
                    ()
                );
        """


def generate_statistics(ids: List[str]) -> QuerySet:
    """
    Generates statistical data over the given CSVData objects

    Params:
        ids (list) -> list of all CSVData objects  ids for statistics query

    Returns:
        QuerySet of the query objects
    """

    return CSVData.objects.raw(get_query(ids))


def map_statistics_by_aircraft(query_set: QuerySet) -> dict:
    """
    Returns dictionary where the keys are query_set objects' aircraft valuess
    and the values are all other columns of query_set objects .

    **NOTE** This function facilitates the extraction process of the columns' values from the newly generate query_set,
             and works as map structure so we can easilly update the existing aircafts rows
    """
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

    mapped_queryset = {}

    for obj in query_set:
        mapped_queryset[obj.aircraft] = {}
        for field in csv_data_fields:
            mapped_queryset[obj.aircraft][field] = getattr(obj, field)
    return mapped_queryset


def update_statistics_objects(mapped_queryset: dict) -> None:
    """
    Generates Statistics objects if it was the first time to upload a file to the database,
    else updates the existing Statistics objects counters

    Params:
        mapped_queryset (dict) -> dict of all new generate statistics objects where the mapping is the aircraft

    Returns:
        None
    """

    if Statistics.objects.exists():
        new_stats_objs = []
        aircrafts = {aircraft_value[0] for aircraft_value in Statistics.objects.values_list("aircraft")}

        for key in mapped_queryset:
            if key in aircrafts:
                Statistics.objects.filter(aircraft=key).update(
                    info_count=F("info_count") + mapped_queryset[key]["info_count"],
                    errors_count=F("errors_count") + mapped_queryset[key]["errors_count"],
                    pre_legend=F("pre_legend") + mapped_queryset[key]["pre_legend"],
                    warning=F("warning") + mapped_queryset[key]["warning"],
                    paired_b=F("paired_b") + mapped_queryset[key]["paired_b"],
                    legend=F("legend") + mapped_queryset[key]["legend"],
                    lower_b=F("lower_b") + mapped_queryset[key]["lower_b"],
                    repeat_legend=F("repeat_legend") + mapped_queryset[key]["repeat_legend"],
                    upper_a=F("upper_a") + mapped_queryset[key]["upper_a"],
                    lower_a=F("lower_a") + mapped_queryset[key]["lower_a"],
                    paired_a=F("paired_a") + mapped_queryset[key]["paired_a"],
                )
            else:
                new_stats_objs.append(Statistics(**mapped_queryset[key]))

        Statistics.objects.bulk_create(new_stats_objs)
    else:
        Statistics.objects.bulk_create([Statistics(**mapped_queryset[key]) for key in mapped_queryset.keys()])


def load_csv(file_path) -> None:
    with open(file_path, "r") as csv_file:
        data = csv.reader(csv_file, delimiter=",")
        next(data)

        loaded_objects = []

        for row in data:
            loaded_objects.append(
                CSVData(
                    priority=row[0],
                    type=row[1],
                    aircraft=row[2],
                    status=row[3],
                    _errors_count=row[4],
                    _info_count=row[5],
                )
            )

    return [f"'{str(obj.uuid)}'" for obj in CSVData.objects.bulk_create(loaded_objects)]
