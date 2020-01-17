# coding: utf-8
"""Python Carson Auth Class"""


import jwt
from jwt import InvalidTokenError

import logging
import requests
import time

from carson_living.const import (CACHE_FILE, CACHE_ATTRS, RETRY_TOKEN,
                                 BASE_HEADERS, API_URI, AUTH_ENDPOINT,
                                 MSG_GENERIC_FAIL)
from carson_living.util import handle_response_return_data
from carson_living.error import (CarsonAPIError, CarsonAuthenticationError, CarsonTokenError)

_LOGGER = logging.getLogger(__name__)


class CarsonAuth(object):
    """A generalized Authentication Class for Carson Living"""
    def __init__(self, username, password, token=None):
        self._username = username
        self._password = password
        self._token = None
        self._token_payload = None
        self._token_expiration_time = None

        # Set and init token values
        self.token = token

    @property
    def token(self):
        return self._token

    @property
    def token_payload(self):
        return self._token_payload

    @property
    def token_expiration_date(self):
        return self._token_expiration_time

    @token.setter
    def token(self, token):
        if token is None:
            self._token = None
            self._token_payload = None
            self._token_expiration_time
            return
        try:
            self._token_payload = jwt.decode(token, verify=False)
            self._token_expiration_time = self._token_payload.get('exp')

            self._token = token
            _LOGGER.info('Updated access Token for %s', self.get_email())
        except InvalidTokenError:
            raise CarsonTokenError('Cannot decode invalid token %s', token)

    def get_email(self):
        return self._token_payload.get('email', '<no mail found>')

    def update_token(self):
        """Authenticate user against Ring API."""
        _LOGGER.info('Getting access Token for %s', self._username)

        response = requests.post(
            (API_URI + AUTH_ENDPOINT),
            json={
                'username': self._username,
                'password': self._password,
            },
            headers=BASE_HEADERS
        )
        try:
            data = handle_response_return_data(response)
            self.token = data.get('token')
        except CarsonAPIError as e:
            raise CarsonAuthenticationError(e)

    def valid_token(self):
        """Return True if token is still valid"""
        if self.token is None or self._token_expiration_time is None:
            return False

        return self._token_expiration_time > int(time.time())

    def query(self,
              url,
              method='get',
              params=None,
              json=None,
              retry_auth=1):
        """Perform an authenticated query"""
        if not self.valid_token():
            self.update_token()

        headers = {'Authorization': 'JWT {}'.format(self.token)}
        headers.update(BASE_HEADERS)

        response = requests.request(method, url,
                                    headers=headers,
                                    params=params,
                                    json=json)

        # special case, clear token and retry. (Recursion)
        if response.status_code == 401 and retry_auth > 0:
            self.token = None
            return self.query(url,
                              method,
                              params,
                              json,
                              retry_auth - 1)

        return handle_response_return_data(response)
