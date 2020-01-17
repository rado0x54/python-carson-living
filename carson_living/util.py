# -*- coding: utf-8 -*-
"""Collection of util functions"""

from carson_living.error import (CarsonAPIError,
                                 CarsonCommunicationError)
from carson_living.const import CARSON_RESPONSE


def handle_response_return_data(response):
    """Safely handle Carson API responses

    Args:
        response: A Python Requests response object.

    Returns:
        The unwrapped data dict of the Carson Living response.

    Raises:
        CarsonCommunicationError: Response was not received or
            not in the expected format.
        CarsonAPIError: Response indicated an client-side API
            error.
    """
    try:
        r_json = response.json()
        if not all(k in r_json for k in CARSON_RESPONSE.values()):
            raise CarsonCommunicationError(
                'Carson API response does not contain all expected keys')

        if r_json.get(CARSON_RESPONSE['CODE']) != 0:
            raise CarsonAPIError(
                # pylint: disable=too-many-format-args
                'Carson API error returned unsuccessful state. '
                'Status: {}, Message: {}'.format(
                    r_json.get(CARSON_RESPONSE['STATUS'], '<no status>'),
                    r_json.get(CARSON_RESPONSE['MSG']), '<no msg>')
                )
    except ValueError:
        raise CarsonCommunicationError(
            'Unable to handle response payload for {} to {}'.format(
                response.request.method, response.url))

    return r_json.get(CARSON_RESPONSE['DATA'])
