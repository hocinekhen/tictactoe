from rest_framework.views import exception_handler
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

import json


def custom_exception_handler(exc, context):
    """
    override the default exception handler used by
    the Django Rest Framework to be similar to what specified
    in the response body description
    """
    # call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # change the error response body to be similar
    # to the one defined in the description
    if isinstance(exc, ValidationError):
        res = Response({"reason": str(exc)},
                       status=status.HTTP_400_BAD_REQUEST)
        return res
    if response is not None:
        errors = {**response.data}
        response.data = {}
        reason = json.dumps(errors)
        "delete special chars from stringified json"
        reason = reason.replace("\"", '').replace("\\", '')
        response.data['reason'] = reason
    else:
        raise Exception(response)

    return response
