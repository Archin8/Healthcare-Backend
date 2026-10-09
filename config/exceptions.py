import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = drf_handler(exc, context)

    if response is not None:
        return response            # DRF handled it (400/401/403/404/405...)

    if isinstance(exc, IntegrityError):
        logger.warning('Integrity error: %s', exc)
        return Response(
            {'detail': 'This operation conflicts with existing data.'},
            status=status.HTTP_409_CONFLICT,
        )

    # Unknown error: log the details, never leak them to the client.
    logger.exception('Unhandled exception', exc_info=exc)
    return Response(
        {'detail': 'Something went wrong on our side.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
