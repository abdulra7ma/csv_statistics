import pandas as pd
from django.db import transaction

from apps.statistics.models import Statistics


class FLightStatistics:
    def __init__(self, file_path) -> None:
        self.file = file_path

        self.read_file()

        print(self.file)

    def read_file(self):
        self.flight_data = pd.read_csv(self.file)

    def run(self):
        self.statistics_by_column("type")
        self.statistics_by_column("aircraft")
        self.statistics_by_column("aircraft")

    def statistics_by_column(self, column_name):
        columns_unique_values = self.flight_data[column_name].unique()

        with transaction.atomic():
            for cuv in columns_unique_values:
                data_by_type = self.flight_data.loc[self.flight_data[column_name] == cuv]

                cloumn_values = data_by_type["type"].value_counts()

                info_count = data_by_type["info_count"].count()
                errors_count = data_by_type["errors_count"].count()
                pre_legend = cloumn_values.get("PreLegend", default=0)
                warning = cloumn_values.get("Warning", default=0)
                paired_b = cloumn_values.get("Paired B", default=0)
                legend = cloumn_values.get("Legend", default=0)
                lower_b = cloumn_values.get("Lower B", default=0)
                repeat_legend = cloumn_values.get("Repeat Legend", default=0)
                upper_a = cloumn_values.get("Upper A", default=0)
                lower_a = cloumn_values.get("Lower A", default=0)
                paired_a = cloumn_values.get("Paired A", default=0)

                data = {
                    column_name: cuv,
                    "info_count": info_count,
                    "errors_count": errors_count,
                    "pre_legend": pre_legend,
                    "warning": warning,
                    "paired_b": paired_b,
                    "legend": legend,
                    "lower_b": lower_b,
                    "repeat_legend": repeat_legend,
                    "upper_a": upper_a,
                    "lower_a": lower_a,
                    "paired_a": paired_a,
                }

                Statistics.objects.create(**data)
