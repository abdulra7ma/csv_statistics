import pytest

from django.conf import settings


@pytest.fixture()
def django_settings():
    return settings
