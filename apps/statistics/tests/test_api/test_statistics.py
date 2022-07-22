import pytest
from django.urls import reverse
from django.utils.translation import gettext
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

STATISTICS_SERIALIZER_PATH = "apps.statistics.api.serializers.StatisticsSerializer"


@pytest.mark.django_db
def test_login_api_success(user_account, unauthorized_api_client, mocker):
    user = user_account()
    mocked_validate = mocker.patch(f"{STATISTICS_SERIALIZER_PATH}.validate", return_value={"user": user})
    mocked_response = Response(status=status.HTTP_204_NO_CONTENT)
    mocked_login = mocker.patch(
        "quran_kg.apps.accounts.services.login.LoginService.login", return_value=mocked_response
    )

    data = {"email": "jane@example.com", "password": "super-secret-password"}  # nosec
    response = unauthorized_api_client.post(reverse("api-v1-accounts:login"), data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    mocked_validate.assert_called_once_with(data)
    mocked_login.assert_called_once_with(mocker.ANY, user)
