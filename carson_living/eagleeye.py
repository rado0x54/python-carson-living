"""Basic Eagle Eye API Module"""
import requests

from requests import HTTPError

from carson_living import CarsonError, CarsonAPIError
from carson_living.const import BASE_HEADERS


class EagleEye(object):
    """Eagle Eye API class for interfacing with the endpoints

    This class should probably be moved in a dedicated Eagle Eye project,
    but initially it can live within Carson Living
    """

    def __init__(self, auth_callback):
        self._auth_callback = auth_callback
        self._active_auth_key = None
        self._active_brand_subdomain = None

    def update_auth(self):
        new_auth_key, new_brand_subdomain = self._auth_callback()

        if not new_auth_key or not new_brand_subdomain:
            raise CarsonError('Eagle Eye authentication callback returned empty values.')

        self._active_auth_key = new_auth_key
        self._active_brand_subdomain = new_brand_subdomain

    def authenticated_query(self,
                            url,
                            method='get',
                            params=None,
                            json=None,
                            retry_auth=1):
        """Perform an authenticated Query against Eagle Eye

        Args:
            url: the url to query, can contain a branded subdomain to substitute
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

        if not self._active_auth_key or not self._active_brand_subdomain:
            self.update_auth()

        headers = {'Authentication': self._active_auth_key}
        headers.update(BASE_HEADERS)

        response = requests.request(method, url.format(self._active_brand_subdomain),
                                    headers=headers,
                                    params=params,
                                    json=json)

        # special case, clear token and retry. (Recursion)
        if response.status_code == 401 and retry_auth > 0:
            self._active_auth_key = None
            return self.authenticated_query(url,
                                            method,
                                            params,
                                            json,
                                            retry_auth - 1)

        try:
            response.raise_for_status()
            return response.json()

        except (ValueError, HTTPError) as error:
            raise CarsonAPIError(error)
