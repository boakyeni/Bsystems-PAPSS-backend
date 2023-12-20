from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status, serializers
from django.core.exceptions import ValidationError


def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc, serializers.ValidationError):
        error_string = ""
        for key, value in exc.detail.items():
            error_string = value[0][:-1] + ": " + key

        custom_response_data = {
            # customize your response format here
            "errors": exc.detail,
            "status": 400,
            "message": error_string,
        }
        return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, ValidationError):
        custom_response_data = {
            # customize your response format here
            "errors": exc.message,
            "status": 400,
            "message": "Validation Error",
        }
        return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)

    return response
