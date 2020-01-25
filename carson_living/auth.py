# coding: utf-8
"""Carson Living Authentication Module"""

import logging
import time
import requests
import jwt
from jwt import InvalidTokenError


from carson_living.const import (BASE_HEADERS,
                                 API_URI,
                                 AUTH_ENDPOINT)
from carson_living.util import default_carson_response_handler
from carson_living.error import (CarsonAPIError,
                                 CarsonAuthenticationError,
                                 CarsonTokenError)

_LOGGER = logging.getLogger(__name__)


# pylint: disable=useless-object-inheritance
class CarsonAuth(object):
    """A generalized Authentication Class for Carson Living.

    Responsible for managing (retrieving and updating) the
    JWT Authentication token for the Carson API.

    Attributes:
        _username: Carson Living username
        _password: Carson Living password
        _token: current JWT token
        _token_payload: current JWT token payload
        _token_expiration_time: current JWT token expiration time
    """

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
        """
        Returns:
            current JWT token or None if currently authenticated.
        """
        return self._token

    @property
    def token_payload(self):
        """
        Returns:
            current JWT token payload or None if currently authenticated.
        """
        return self._token_payload

    @property
    def token_expiration_date(self):
        """
        Returns:
            current JWT token expiration time (seconds from epoch)
            or None if currently authenticated.
        """
        return self._token_expiration_time

    @token.setter
    def token(self, token):
        """Set or clear a new JWT Token.
        Args:
            token: Valid JWT token or None to clear current token.

        Raises:
            CarsonTokenError: JWT token format is invalid.
        """
        if token is None:
            self._token = None
            self._token_payload = None
            self._token_expiration_time = None
            return
        try:
            self._token_payload = jwt.decode(token, verify=False)
            self._token_expiration_time = self._token_payload.get('exp')

            self._token = token
            _LOGGER.info('Set access Token for %s',
                         self._token_payload.get('email', '<no e-mail found>'))
        except InvalidTokenError:
            raise CarsonTokenError('Cannot decode invalid token {}'
                                   .format(token))

    def update_token(self):
        """Authenticate user against Carson Living API.

        Raises:
            CarsonAuthenticationError: On authentication error.

        """
        _LOGGER.info('Getting new access Token for %s', self._username)

        response = requests.post(
            (API_URI + AUTH_ENDPOINT),
            json={
                'username': self._username,
                'password': self._password,
            },
            headers=BASE_HEADERS
        )
        try:
            data = default_carson_response_handler(response)
            self.token = data.get('token')
        except CarsonAPIError as error:
            raise CarsonAuthenticationError(error)

    def valid_token(self):
        """Checks that Carson Authentication has a valid token.

        Returns:
            True if a token is set and not expired, otherwise False
        """
        if self.token is None or self._token_expiration_time is None:
            return False

        return self._token_expiration_time > int(time.time())

    def authenticated_query(self, url, method='get', params=None,
                            json=None, retry_auth=1,
                            response_handler=default_carson_response_handler):
        """Perform an authenticated Query against Carson Living

        Args:
            url: the url to query
            method: the http method to use
            params: the http params to use
            json: the json payload to submit
            retry_auth: number of query and reauthentication retries
            response_handler: dynamic response handler for api

        Returns:
            The unwrapped data dict of the Carson Living response.

        Raises:
            CarsonCommunicationError: Response was not received or
                not in the expected format.
            CarsonAPIError: Response indicated an client-side API
                error.
        """

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
            return self.authenticated_query(
                url, method, params, json, retry_auth - 1,
                response_handler)

        return response_handler(response)
