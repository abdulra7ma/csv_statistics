from apps.statistics.models import Statistics, StatisticsCSVUploadedFile
from apps.statistics.api.utils import generate_file_hash
from rest_framework import serializers, status


class StatisticsCSVUploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsCSVUploadedFile
        fields = ["file", "file_hash"]
        extra_kwargs = {
            "file": {"write_only": True},
            "file_hash": {"read_only": True},
        }

    def validate_file(self, file):
        ALLOWED_FILE_FORMATS = ["csv"]

        if file.name.split(".")[-1].lower() not in ALLOWED_FILE_FORMATS:
            raise serializers.ValidationError(
                detail="file format not supported please submit a valid file format.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return file

    def validate(self, attrs):
        if "file" not in attrs:
            raise serializers.ValidationError(
                detail="file not found",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return super().validate(attrs)

    def create(self, validated_data):
        instance = super().create(validated_data)

        # create hash for the file after object creation
        instance.file_hash = generate_file_hash(instance.file.path)
        instance.save()

        return instance


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = [
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
        ]
