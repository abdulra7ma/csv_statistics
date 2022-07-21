import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.statistics.statistics import FLightStatistics
from apps.statistics.models import StatisticsCSVUploadedFile

from apps.statistics.utils.file_hash import generate_file_hash


@receiver(post_save, sender=StatisticsCSVUploadedFile)
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
            statistics_model = FLightStatistics(file_path=csv_file_path)
            statistics_model.run()
