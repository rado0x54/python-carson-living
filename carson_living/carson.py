# -*- coding: utf-8 -*-
"""Carson Living API Module."""
import logging

from carson_living.auth import CarsonAuth

from carson_living.carson_entities import (CarsonUser,
                                           CarsonBuilding)
from carson_living.const import (C_API_URI,
                                 C_ME_ENDPOINT)
from carson_living.util import update_dictionary


_LOGGER = logging.getLogger(__name__)


# pylint: disable=useless-object-inheritance
class Carson(CarsonAuth):
    """A Python Abstraction object to the Carson Living API.

        Attributes:
            _user: The authenticated user to Carson
            _buildings:
                The building properties that are associated with
                the current user
    """
    def __init__(self, username, password,
                 initial_token=None, token_update_cb=None):
        super(Carson, self).__init__(username, password,
                                     initial_token, token_update_cb)

        self._user = None
        self._buildings = {}

        self.update()

    @property
    def buildings(self):
        """Building properties that belong to the user"""
        return self._buildings.values()

    @property
    def first_building(self):
        """Convenience Function to return first building in account"""
        return next(iter(self.buildings))

    @property
    def user(self):
        """The current authenticated user"""
        return self._user

    def update(self):
        """Update entity list and individual entity parameters associated with the API

        """
        _LOGGER.debug('Updating Carson Living API and associated entities')
        url = C_API_URI + C_ME_ENDPOINT
        me_payload = self.authenticated_query(url)

        self._update_user(me_payload)
        self._update_buildings(me_payload)

    def _update_user(self, payload):
        if self._user is None:
            self._user = CarsonUser(entity_payload=payload)
        else:
            self._user.update(payload)

    def _update_buildings(self, payload):
        # Not 100% if propertyLevel condition is playing it overly safe.
        update_buildings = {p['id']: p
                            for p in payload.get('properties')
                            if p['propertyLevel'] == 'building'}

        update_dictionary(
            self._buildings,
            update_buildings,
            lambda p: CarsonBuilding(
                self,
                p))
