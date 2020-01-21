"""Module containing all devices that are exposed via Carson Living"""

import logging
from abc import ABCMeta, abstractmethod

from carson_living.error import CarsonError
from carson_living.eagleeye import EagleEye
from carson_living.const import (API_URI,
                                 EAGLEEYE_SESSION_ENDPOINT)
from carson_living.util import update_dictionary

_LOGGER = logging.getLogger(__name__)


class _AbstractEntity(object):
    # pylint: disable=useless-object-inheritance
    """Updateable Base Entity

    Attributes:
        _update_callback:
            The callback that can be used to update the
            entity_payload:
        _entity_payload:
            The payload the the entity draws its internal
            state from.

    """
    __metaclass__ = ABCMeta

    def __init__(self, update_callback=None, entity_payload=None):
        self._update_callback = update_callback
        self._entity_payload = entity_payload

        # update internal representation
        self.update(entity_payload)

    @property
    @abstractmethod
    def entity_id(self):
        """Entity ID

        Returns:
            Domain-specific entity id.

        """
        raise NotImplementedError(
            'Derived Entity does not implement entity_id!')

    @property
    @abstractmethod
    def unique_entity_id(self):
        """Unqiue Entity ID

        Returns:
            Unique entity id across entire library.
        """
        raise NotImplementedError(
            'Derived Entity does not implement unique_entity_id!')

    @abstractmethod
    def _internal_update(self):
        """Update internal state

        Allows the entity to update internal state
        after _entity_payload changes
        """
        raise NotImplementedError(
            'Derived Entity does not implement _internal_update!')

    @property
    def entity_payload(self):
        """Entity Payload

        Returns: the raw entity_payload

        """
        return self._entity_payload

    def update(self, entity_payload=None):
        """Update the entity

        Updates the entity with a given entity_payload. This payload
        can be passed directly the update function OR if left empty,
        the entity updates via tha given update_callback

        Args:
            entity_payload: optional payload to setup the entity

        Raises:
            CarsonError:
                If neither a entity_payload or a update_callback
                was passes during initialization.

        """
        if self._update_callback is None and self._entity_payload is None:
            raise CarsonError(
                'Trying to update entity {} without external payload '
                'or a callback function'
                .format(self.unique_entity_id))

        if entity_payload is not None:
            self._entity_payload = entity_payload
            _LOGGER.info(
                'Successfully updated entity %s from external payload',
                self.unique_entity_id)
        else:
            self._entity_payload = self._update_callback()
            _LOGGER.info(
                'Successfully updated entity %s from update callback',
                self.unique_entity_id)

        # Allow child class to perform internal updates
        self._internal_update()


class _AbstractAPIEntity(_AbstractEntity):
    # pylint: disable=abstract-method
    __metaclass__ = ABCMeta

    def __init__(self, api, update_callback=None, entity_payload=None):
        self._api = api
        super(_AbstractAPIEntity, self).__init__(
            update_callback=update_callback,
            entity_payload=entity_payload)


class CarsonBuilding(_AbstractAPIEntity):
    """Carson Living Building Entity

    Attributes:
        _cameras:
            dict id->entity mapping of all camera entities
            associated with the given building.
        _doors:
            dict id->entity mapping of all door entities
            associated with the given building.
        _eagleeye:
            Eagle Eye API object that carries a building-specific
            authorization callback.


    """

    def __init__(self, api, update_callback=None, entity_payload=None):
        self._cameras = {}
        self._doors = {}
        self._eagleeye = EagleEye(self._get_eagleeye_session)

        super(CarsonBuilding, self).__init__(api,
                                             update_callback=update_callback,
                                             entity_payload=entity_payload)

    def _get_eagleeye_session(self):
        """Retrieve a new eagle eye auth key and subdomain information

        Args:
            building_id: The building id of the Carson property

        Returns:
            (tuple): tuple containing:

                sessionid(str): Eagle Eye authentication token for account
                subdomain(str): Eagle Eye subdomain to use with account

        """
        url = API_URI + EAGLEEYE_SESSION_ENDPOINT.format(self.entity_id)
        return self._api.authenticated_query(url)

    @property
    def entity_id(self):
        return self.entity_payload.get('id')

    @property
    def unique_entity_id(self):
        return 'carson_building_{}'.format(self.entity_id)

    def _internal_update(self):
        # Update Cameras from _entity_payload
        self._update_cameras()

        # Update Doors from _entity_payload
        self._update_doors()

    def _update_cameras(self):
        # Only Support Eagle_Eye right now
        update_cameras = {c['id']: c
                          for c in self.entity_payload.get('cameras')
                          if c['provider'] == 'eagle_eye'}

        update_dictionary(
            self._cameras,
            update_cameras,
            lambda p: EagleEyeCamera(
                self._eagleeye,
                entity_payload=p))

    def _update_doors(self):
        update_doors = {d['id']: d for d in self.entity_payload.get('doors')}

        update_dictionary(
            self._doors,
            update_doors,
            lambda p: CarsonDoor(
                self._api,
                entity_payload=p))

    @property
    def name(self):
        """Name

        Returns: The name of the building

        """
        return self.entity_payload.get('name')

    @property
    def type(self):
        """Type

        Returns: The type of building

        """
        return self.entity_payload.get('type')

    @property
    def cameras(self):
        """Cameras

        Returns: All camera entities associated with the building

        """
        return self._cameras.values()

    @property
    def doors(self):
        """Doors

        Returns: All door entities associated with the building

        """
        return self._doors.values()


class CarsonUser(_AbstractEntity):
    """Carson Living User Entity

    """

    @property
    def unique_entity_id(self):
        return 'carson_user_{}'.format(self.entity_id)

    def _internal_update(self):
        pass

    @property
    def entity_id(self):
        return self.entity_payload.get('id')

    @property
    def first_name(self):
        """First Name

        Returns: First Name of the current User

        """
        return self.entity_payload.get('firstName')

    @property
    def last_name(self):
        """Last Name

        Returns: Last Name of the current User

        """
        return self.entity_payload.get('lastName')


class CarsonDoor(_AbstractAPIEntity):
    """Carson Living Door Entity

    """

    @property
    def unique_entity_id(self):
        return 'carson_door_{}'.format(self.entity_id)

    def _internal_update(self):
        pass

    @property
    def entity_id(self):
        return self.entity_payload.get('id')


class EagleEyeCamera(_AbstractAPIEntity):
    """Eagle Eye Camera Entity

    """

    @property
    def unique_entity_id(self):
        return 'eagleeye_camera_{}'.format(self.entity_id)

    def _internal_update(self):
        pass

    @property
    def entity_id(self):
        return self.entity_payload.get('id')
