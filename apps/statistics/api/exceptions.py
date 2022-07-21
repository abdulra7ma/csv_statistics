# external imports
from rest_framework.exceptions import APIException


class NotCorrectParameters(APIException):
    """Raise a HTTP 400 error, if query params not Correct or not provided"""

    status_code = 400
    default_detail = "Not correct query parameters"
    default_code = "not_correct_query_params"
