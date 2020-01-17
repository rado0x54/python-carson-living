# -*- coding: utf-8 -*-
"""Collection of util functions"""

from carson_living.error import CarsonAPIError, CarsonCommunicationError
from carson_living.const import CARSON_RESPONSE


def handle_response_return_data(r):
    try:
        r_json = r.json()
        if not all(k in r_json for k in CARSON_RESPONSE.values()):
            raise CarsonCommunicationError('Carson API response does not contain all expected keys')

        if r_json.get(CARSON_RESPONSE['CODE']) != 0:
            raise CarsonAPIError('Carson API error returned unsuccessful state. Status: %s, Message: %s',
                                 r_json.get(CARSON_RESPONSE['STATUS']),
                                 r_json.get(CARSON_RESPONSE['MSG']))
    except ValueError as e:
        raise CarsonCommunicationError('Response error for %s to %s', r.request.method, r.url)

    return r_json.get(CARSON_RESPONSE['DATA'])
