# -*- coding: utf-8 -*-
"""Collection of util functions"""

import time

from carson_living.error import (CarsonAPIError,
                                 CarsonCommunicationError)
from carson_living.const import CARSON_RESPONSE


def default_carson_response_handler(response):
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


def update_dictionary(current_dict, update_dict, constructor):
    """Update current_dict to update_dict without reconstructing existing

    update_dictionary updates the dict current_dict to resemble update_dict
    by
        1. removing values from current_dict that are missing in update_dict.
           (via del current_dict('missing'))
        2. adding values to current_dict that are only found in update_dict.
           (via constructor(update_dict['new'])
        3. update values (via current_dict[i].update(update_dict['changed']))

    Args:
        current_dict: The dict to update with entities
        update_dict: The latest dict with update payloads
        constructor: Constructor funtion to generate entity with payload

    """

    existing_keys = set(current_dict.keys())
    update_keys = set(update_dict.keys())

    # Update
    for i in existing_keys.intersection(update_keys):
        current_dict[i].update(update_dict[i])

    # Add
    for i in update_keys.difference(existing_keys):
        current_dict[i] = constructor(update_dict[i])

    # Remove
    for i in existing_keys.difference(update_keys):
        del current_dict[i]


def current_milli_time():
    """Return the current time in milliseconds"""
    return int(time.time() * 1000)


def timedelta_to_milli_time(timedelta):
    """Return the current time in milliseconds"""
    return int(timedelta.total_seconds() * 1000)
