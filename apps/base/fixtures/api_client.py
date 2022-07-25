import json

import pytest
from rest_framework.test import APIClient

__all__ = ["api_client"]


class _CustomAPIClient(APIClient):
    """
    Helper APIClient class

    As we use `rest_framework.parsers.JSONParser` only we need to make correct
    requests during test run:
        `content_type` should explicitly set to "application/json"
        `data should` properly encoded to JSON.
    """

    def post(self, path, data=None, format=None, content_type="application/json", follow=False, **extra):
        # if isinstance(data, (dict, list)):
        #     data = json.dumps(data)
        response = super().post(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    def put(self, path, data=None, format=None, content_type="application/json", follow=False, **extra):
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        response = super().put(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    def patch(self, path, data=None, format=None, content_type="application/json", follow=False, **extra):
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        response = super().patch(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    def delete(self, path, data=None, format=None, content_type="application/json", follow=False, **extra):
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        response = super().delete(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response


@pytest.fixture()
def api_client():
    return _CustomAPIClient()
