from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.utils.translation import gettext_lazy as _


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (InvalidToken, AuthenticationFailed)):
        if response is not None:
            response.data['detail'] = _("Your session has expired or the token is invalid. Please log in again.")

    if isinstance(exc, NotAuthenticated):
        if response is not None:
            response.data['detail'] = _("Authentication credentials were not provided. Please log in first.")

    return response