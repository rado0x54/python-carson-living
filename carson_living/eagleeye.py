"""Basic Eagle Eye API Module"""
import logging

import requests
from requests import HTTPError

from carson_living.error import (CarsonError,
                                 CarsonAPIError)
from carson_living.eagleeye_entities import EagleEyeCamera

from carson_living.util import update_dictionary
from carson_living.const import (BASE_HEADERS,
                                 EEN_API_URI,
                                 EEN_DEVICE_LIST_ENDPOINT,
                                 EEN_IS_AUTH_ENDPOINT)

_LOGGER = logging.getLogger(__name__)


# pylint: disable=useless-object-inheritance
class EagleEye(object):
    """Eagle Eye API class for interfacing with the endpoints

    This class should probably be moved in a dedicated Eagle Eye project,
    but initially it can live within Carson Living. Note, the eagle eye
    API does not update it's state during initialization, but is updated
    externally. Carson Living update automatically triggers an update call
    to Eagle Eye.
    """

    def __init__(self, session_callback):
        self._session_callback = session_callback
        self._session_auth_key = None
        self._session_brand_subdomain = None
        self._cameras = {}

    @property
    def session_auth_key(self):
        """Current Auth Key"""
        return self._session_auth_key

    @property
    def session_brand_subdomain(self):
        """Current Brand Subdomain"""
        return self._session_brand_subdomain

    @property
    def cameras(self):
        """Get all cameras returned directly by the API"""
        return self._cameras.values()

    def get_camera(self, ee_id):
        """

        Args:
            ee_id: Eagle Eye camera id

        Returns:
            The EagleEye Camera with id or None, if not found.

        """
        return self._cameras.get(ee_id)

    def update_session_auth_key(self):
        """Updates the internal session state via session_callback

        Raises:
            CarsonError: If callback returns empty value.

        """
        _LOGGER.debug(
            'Trying to update the session auth key for the Eagle Eye API.')
        auth_key, brand_subdomain = self._session_callback()

        if not auth_key or not brand_subdomain:
            raise CarsonError(
                'Eagle Eye authentication callback returned empty values.')

        self._session_auth_key = auth_key
        self._session_brand_subdomain = brand_subdomain

    def check_auth(self, refresh=True):
        """Check if the current auth_key is still valid

        Args:
            refresh:
                automatically update auth_key if not valid

        Returns: True if a valid auth_key exists.

        """
        if not refresh and not self._session_auth_key:
            return False

        retry_auth = 1 if refresh else 0

        try:
            self.authenticated_query(
                EEN_API_URI + EEN_IS_AUTH_ENDPOINT,
                retry_auth=retry_auth
            )
        except CarsonAPIError:
            return False

        return True

    def authenticated_query(self, url, method='get', params=None,
                            json=None, retry_auth=1, stream=None,
                            response_handler=lambda r: r.json()):
        """Perform an authenticated Query against Eagle Eye

        Args:
            url:
                the url to query, can contain a branded subdomain
                to substitute
            method: the http method to use
            params: the http params to use
            json: the json payload to submit
            retry_auth: number of query and reauthentication retries
            stream: Stream the content
            response_handler: optional file handler to stream the raw content

        Returns:
            The json response object, or the file handler that was passed
            to receive the raw response.

        Raises:
            CarsonAPIError: Response indicated an client or
            server-side API error.
        """
        if not self._session_auth_key \
                or not self._session_brand_subdomain:
            self.update_session_auth_key()

        headers = {'Cookie': 'auth_key={}'.format(self._session_auth_key)}
        headers.update(BASE_HEADERS)

        response = requests.request(method,
                                    url.format(self._session_brand_subdomain),
                                    headers=headers,
                                    params=params,
                                    json=json,
                                    stream=stream)

        # special case, clear token and retry. (Recursion)
        if response.status_code == 401 and retry_auth > 0:
            _LOGGER.info(
                'Eagle Eye request %s returned 401, retrying ... (%d left)',
                url, retry_auth)
            self._session_auth_key = None
            return self.authenticated_query(
                url, method, params, json, retry_auth - 1,
                stream, response_handler)

        try:
            response.raise_for_status()
            return response_handler(response)

        except HTTPError as error:
            raise CarsonAPIError(error)

    def update(self):
        """Update internal state

        Update entity list and individual entity parameters associated with the
        Eagle Eye API

        """
        _LOGGER.debug('Updating Eagle Eye API and associated entities')
        self._update_cameras()

    def _update_cameras(self):
        # Query List
        device_list = self.authenticated_query(
            EEN_API_URI + EEN_DEVICE_LIST_ENDPOINT
        )

        update_cameras = {
            c[1]: EagleEyeCamera.map_list_to_entity_payload(c)
            for c in device_list if c[3] == 'camera'
        }

        update_dictionary(
            self._cameras,
            update_cameras,
            lambda c: EagleEyeCamera(self, c))
