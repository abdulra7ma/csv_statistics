"""

"""

from apps.statistics.models import StatisticsCSVUploadedFile
from apps.statistics.api.utils import generate_file_hash
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import generate_statistics, load_csv, map_statistics_by_aircraft, update_statistics_objects


@receiver(post_save, sender=StatisticsCSVUploadedFile)
@transaction.atomic
def generate_and_save_statistics(sender, instance, created, **kwargs) -> None:
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
            loaded_objects_ids = load_csv(instance.file.path)
            quert_set = generate_statistics(loaded_objects_ids)
            mapped_queryset = map_statistics_by_aircraft(quert_set)
            update_statistics_objects(mapped_queryset)
