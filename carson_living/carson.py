# -*- coding: utf-8 -*-
"""Carson Living API Module."""

import logging

from carson_living.const import (API_URI,
                                 EAGLEEYE_SESSION_ENDPOINT)

_LOGGER = logging.getLogger(__name__)


# pylint: disable=useless-object-inheritance
class Carson(object):
    """A Python Abstraction object to the Carson Living API.

        Attributes:
            carson_auth: The Carson Authentication class to use
    """

    def __init__(self, carson_auth):
        self.carson_auth = carson_auth

    def get_eagleeye_session(self, building_id):
        """Retrieve a new eagle eye auth key and subdomain information

        Args:
            building_id: The building id of the Carson property

        Returns:
            (tuple): tuple containing:

                sessionid(str): Eagle Eye authentication token for account
                subdomain(str): Eagle Eye subdomain to use with account

        """
        url = API_URI + EAGLEEYE_SESSION_ENDPOINT.format(building_id)
        return self.carson_auth.authenticated_query(url)

    def get_doors(self):
        """Return door objects"""

    def get_cameras(self):
        """Return camera objects"""
