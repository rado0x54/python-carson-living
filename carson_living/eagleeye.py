"""Basic Eagle Eye API Module"""
import requests

from requests import HTTPError

from carson_living.error import CarsonError, CarsonAPIError
from carson_living.const import BASE_HEADERS


# pylint: disable=useless-object-inheritance
class EagleEye(object):
    """Eagle Eye API class for interfacing with the endpoints

    This class should probably be moved in a dedicated Eagle Eye project,
    but initially it can live within Carson Living
    """

    def __init__(self, session_callback):
        self._session_callback = session_callback
        self._session_auth_key = None
        self._session_brand_subdomain = None
        self._cameras = []

    @property
    def cameras(self):
        """Get all cameras returned directly by the API"""
        return self._cameras

    def _update_session_auth_key(self):
        """Updates the internal session state via session_callback

        Raises:
            CarsonError: If callback returns empty value.

        """
        auth_key, brand_subdomain = self._session_callback()

        if not auth_key or not brand_subdomain:
            raise CarsonError(
                'Eagle Eye authentication callback returned empty values.')

        self._session_auth_key = auth_key
        self._session_brand_subdomain = brand_subdomain

    def authenticated_query(self, url, method='get', params=None,
                            json=None, retry_auth=1):
        """Perform an authenticated Query against Eagle Eye

        Args:
            url:
                the url to query, can contain a branded subdomain
                to substitute
            method: the http method to use
            params: the http params to use
            json: the json payload to submit
            retry_auth: number of query and reauthentication retries

        Returns:
            The json response object

        Raises:
            CarsonAPIError: Response indicated an client or
            server-side API error.
        """

        if not self._session_auth_key \
                or not self._session_brand_subdomain:
            self._update_session_auth_key()

        headers = {'Cookie': 'auth_key={}'.format(self._session_auth_key)}
        headers.update(BASE_HEADERS)

        response = requests.request(method,
                                    url.format(self._session_brand_subdomain),
                                    headers=headers,
                                    params=params,
                                    json=json)

        # special case, clear token and retry. (Recursion)
        if response.status_code == 401 and retry_auth > 0:
            self._session_auth_key = None
            return self.authenticated_query(
                url, method, params, json, retry_auth - 1)

        try:
            response.raise_for_status()
            return response.json()

        except (ValueError, HTTPError) as error:
            raise CarsonAPIError(error)

    def update(self):
        """Update internal state

        Update entity list and individual entity parameters associated with the
        Eagle Eye API

        """

    def _update_cameras(self):
        pass
