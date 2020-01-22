"""Module containing all devices that are exposed via Carson Living"""

import logging
from abc import ABCMeta, abstractmethod

from carson_living.error import CarsonError
from carson_living.eagleeye import EagleEye
from carson_living.const import (API_URI,
                                 EAGLEEYE_SESSION_ENDPOINT,
                                 DOOR_OPEN_ENDPOINT,
                                 EAGLE_EYE_API_URI,
                                 EAGLE_EYE_DEVICE_ENDPOINT)
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

    def __repr__(self):
        return '<Object {} with unique_entity_id {}>'.format(
            self.__class__.__name__, self.unique_entity_id)

    def __str__(self):
        return '{} with unique id {}'.format(
            self.__class__.__name__, self.unique_entity_id)

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
        if not self._update_callback and not entity_payload:
            raise CarsonError(
                'Trying to update entity {} without external payload '
                'or a callback function'
                .format(self.unique_entity_id))

        # If there is a callback execute it (Priority over pass entity_payload)
        if self._update_callback:
            _LOGGER.info(
                'Trying to updated entity %s from update callback',
                self.unique_entity_id)
            entity_payload = self._update_callback()

        # There should be a entity_payload now, otherwise fail
        if not entity_payload:
            raise CarsonError(
                'Trying to update {}, but no payload found set or returned'
                .format(self.unique_entity_id))

        self._entity_payload = entity_payload

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
        session = self._api.authenticated_query(url)
        return session.get('sessionId'), session.get('activeBrandSubdomain')

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
                self._eagleeye, p['externalId']))

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

    @property
    def payments_enabled(self):
        """Payments enabled

        Returns: True if that building has payments enabled

        """
        return self.entity_payload.get('paymentsEnabled')

    @property
    def area(self):
        """Area

        Returns:
            A dict with lat, lon, radius representing the geo
            location of the building

        """
        return self.entity_payload.get('area')

    @property
    def visitor_invite_enabled(self):
        """Visitor invite enabled

        Returns:
            True if the user is allowed to invite visitors
            to Carson Living

        """
        return self.entity_payload.get('visitorInviteEnabled')

    @property
    def doors_available(self):
        """Doors available

        Returns:
            True if the building has doors

        """
        return self.entity_payload.get('doorsAvailable')

    @property
    def pmc_name(self):
        """PMC

        Returns:
            Name of the property management company

        """
        return self.entity_payload.get('pmcName')

    @property
    def service_requests_enabled(self):
        """Service requests enabled

        Returns:
            True if the building allows to receive service requests

        """
        return self.entity_payload.get('serviceRequestsEnabled')

    @property
    def visitor_invites_left(self):
        """Visitor invites left

        Returns:
            Number of visitor invites that are left for the building
            (in regard to the current user)

        """
        return self.entity_payload.get('visitorInvitesLeft')

    @property
    def country(self):
        """Country

        Returns:
            Name of the country the building is in

        """
        return self.entity_payload.get('country')

    @property
    def state(self):
        """State

        Returns:
            Name of the state the building is in

        """
        return self.entity_payload.get('state')

    @property
    def timezone(self):
        """Timezone

        Returns:
            The tz database string the building is in

        """
        return self.entity_payload.get('timezone')

    @property
    def units(self):
        """List of units

        Returns:
            A list of units with element dict keys:
                name: Name of the Unit
                payments_enabled: True/False
        """
        return [
            {
                'name': u.get('name'),
                'payments_enabled': u.get('paymentsEnabled'),
            }
            for u in self.entity_payload.get('units')]


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

    @property
    def contact_info(self):
        """List of contact information

        Returns:
            A list of contact information with element
            dict keys:
                contact_info: The contact info
                type: type of contact info
                primary: True/False
                verified: True/False
        """
        return [
            {
                'contact_info': c.get('contactInfo'),
                'type': c.get('type'),
                'primary': c.get('primary'),
                'verified': c.get('verified'),
            }
            for c in self.entity_payload.get('contactInfo')]

    @property
    def photo(self):
        """Photo

        Returns: Photo dict with keys:
            url: full-size photo
            thumbnail_url: thumbnail preview photo

        """
        photo = self.entity_payload.get('photo')
        return {
            'url': photo.get('url'),
            'thumbnail_url': photo.get('thumbnailUrl')
        }

    @property
    def verified(self):
        """Verified

        Returns: True if the user account is verified

        """
        return self.entity_payload.get('verified')

    @property
    def is_admin(self):
        """Verified

        Returns: True if the user account is an admin account

        """
        return self.entity_payload.get('isAdmin')

    @property
    def is_service(self):
        """Is Service

        Returns: True if the user account is a service account

        """
        return self.entity_payload.get('isService')


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

    @property
    def name(self):
        """Name

        Returns: The name of the door

        """
        return self.entity_payload.get('name')

    @property
    def provider(self):
        """Provider

        Returns: The provider service of the door

        """
        return self.entity_payload.get('provider')

    @property
    def is_active(self):
        """Is active

        Returns: True if door is currently active

        """
        return self.entity_payload.get('isActive')

    @property
    def disabled(self):
        """disabled

        Returns: True if door is currently disabled

        """
        return self.entity_payload.get('disabled')

    @property
    def is_unit_door(self):
        """Is unit door

        Returns: True if door belongs to a unit

        """
        return self.entity_payload.get('isUnitDoor')

    @property
    def staff_only(self):
        """Staff only

        Returns: True if door can be used by staff only

        """
        return self.entity_payload.get('staffOnly')

    @property
    def default_in_building(self):
        """Default in building

        Returns: True if door is a default entrance door

        """
        return self.entity_payload.get('defaultInBuilding')

    @property
    def external_id(self):
        """External id

        Returns: External reference id of the provider

        """
        return self.entity_payload.get('externalId')

    @property
    def available(self):
        """Available

        Returns: True if door is currently available

        """
        return self.entity_payload.get('available')

    @property
    def order(self):
        """Order

        Returns: Integer that represents a linear order within the building

        """
        return self.entity_payload.get('order')

    def open(self):
        """Unlock the door

        """
        url = API_URI + DOOR_OPEN_ENDPOINT.format(self.entity_id)
        self._api.authenticated_query(url, method='post')


class EagleEyeCamera(_AbstractAPIEntity):
    """Eagle Eye Camera Entity

    """
    def __init__(self, api, ee_id):
        self._ee_id = ee_id
        super(EagleEyeCamera, self).__init__(
            api,
            update_callback=self._get_payload
        )

    def _get_payload(self):
        url = EAGLE_EYE_API_URI + EAGLE_EYE_DEVICE_ENDPOINT
        return self._api.authenticated_query(url,
                                             params={'id': self.entity_id})

    @property
    def unique_entity_id(self):
        return 'eagleeye_camera_{}'.format(self.entity_id)

    def _internal_update(self):
        pass

    @property
    def entity_id(self):
        return self._ee_id

    @property
    def name(self):
        """Name

        Returns: Device name

        """
        return self.entity_payload.get('name')

    @property
    def settings(self):
        """Settings

        Returns: Json object of basic settings (location, motion regions, etc.)

        """
        return self.entity_payload.get('settings')

    @property
    def utc_offset(self):
        """UTC offset

        Returns: Signed UTC offset in seconds of the set 'timezone'

        """
        return self.entity_payload.get('utcOffset')

    @property
    def timezone(self):
        """Timezone

        Returns: tz database string of the camera

        """
        return self.entity_payload.get('timezone')

    @property
    def guid(self):
        """GUID

        Returns:
            The GUID (Globally Unique Identifier) is an immutable device
            identifier

        """
        return self.entity_payload.get('guid')

    @property
    def permissions(self):
        """Permissions

        Returns:
            String of characters each defining a permission level of
            the current user

        """
        return self.entity_payload.get('permissions')

    @property
    def tags(self):
        """Tags

        Returns:
            Array of strings each representing a tag name

        """
        return self.entity_payload.get('tags')

    @property
    def bridges(self):
        """Bridges

        Returns:
            Json object of bridges (ESNs) this device is seen by and the
            camera attach status:

        """
        return self.entity_payload.get('bridges')

    @property
    def camera_parameters_status_code(self):
        """Camera parameters status code

        Returns:
            Indicates whether it was possible to retrieve the device parameters
            (200) or not (404)

        """
        return self.entity_payload.get('camera_parameters_status_code')

    @property
    def camera_parameters(self):
        """Camera Parameters

        Returns:
            Json object of camera parameters.

        """
        return self.entity_payload.get('camera_parameters')

    @property
    def camera_info_status_code(self):
        """Camera info status code

        Returns:
            Indicates whether it was possible to retrieve information about
            the device (200) or not (404)

        """
        return self.entity_payload.get('camera_info_status_code')

    @property
    def camera_info(self):
        """Name

        Returns: Json object of basic information related to a camera

        """
        return self.entity_payload.get('camera_info')
