# external imports
import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def rest_client():
    """
    A better Alternative for the native Django fixture client
    """
    return APIClient()
