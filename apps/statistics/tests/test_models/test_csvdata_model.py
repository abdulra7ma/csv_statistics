import pytest
from apps.statistics.models import CSVData


@pytest.mark.django_db
def test_csvdata_object_creation():
    assert CSVData.objects.count() == 0

    data = {
        "priority": "Top",
        "type": "test_type",
        "aircraft": "AN564",
        "status": "active",
        "_errors_count": 5,
        "_info_count": 4,
    }

    csv_data = CSVData.objects.create(**data)

    assert CSVData.objects.count() == 1
    assert csv_data.priority == data["priority"]
    assert csv_data.type == data["type"]
    assert csv_data.aircraft == data["aircraft"]
    assert csv_data.status == data["status"]
    assert csv_data._errors_count == data["_errors_count"]
    assert csv_data._info_count == data["_info_count"]


@pytest.mark.django_db
def test_csvdata_obj_default_values_after_creation():
    assert CSVData.objects.count() == 0

    data = {
        "priority": "Top",
        "type": "test_type",
        "aircraft": "AN564",
        "status": "active",
    }

    csv_data = CSVData.objects.create(**data)
    assert CSVData.objects.count() == 1
    assert csv_data._errors_count == 0
    assert csv_data._info_count == 0


@pytest.mark.django_db
def test_core_queryset_activate():
    assert CSVData.objects.count() == 0

    csv_data = CSVData.objects.create(is_active=False)

    assert CSVData.objects.count() == 1
    assert CSVData.objects.active().count() == 0
    assert CSVData.objects.inactive().count() == 1
    assert CSVData.objects.inactive().first() == csv_data

    csv_data.activate()

    assert CSVData.objects.count() == 1
    assert CSVData.objects.active().count() == 1
    assert CSVData.objects.inactive().count() == 0
    assert CSVData.objects.active().first() == csv_data


@pytest.mark.django_db
def test_core_queryset_deactivate():
    assert CSVData.objects.count() == 0

    csv_data = CSVData.objects.create(is_active=True)

    assert CSVData.objects.count() == 1
    assert CSVData.objects.active().count() == 1
    assert CSVData.objects.inactive().count() == 0
    assert CSVData.objects.active().first() == csv_data

    csv_data.deactivate()

    assert CSVData.objects.count() == 1
    assert CSVData.objects.active().count() == 0
    assert CSVData.objects.inactive().count() == 1
    assert CSVData.objects.inactive().first() == csv_data
