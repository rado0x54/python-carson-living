"""Carson Living Entities"""

from carson_living.entities import (_AbstractEntity,
                                    _AbstractAPIEntity)

from carson_living.eagleeye import EagleEye

from carson_living.const import (C_API_URI,
                                 C_EEN_SESSION_ENDPOINT,
                                 C_DOOR_OPEN_ENDPOINT)

from carson_living.util import update_dictionary


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

    def __init__(self, api, entity_payload):
        self._cameras = {}
        self._doors = {}
        # Beware, entity building id must be injected early, since it is
        # required during object __init__
        self._eagleeye = EagleEye(
            lambda: self._get_eagleeye_session(api, entity_payload.get('id'))
        )

        super(CarsonBuilding, self).__init__(api,
                                             entity_payload=entity_payload)

    def __str__(self):
        pattern = """\
id: {entity_id}
name: {name}
number of cameras: {nr_cams}
number of door: {nr_doors}
number of units: {nr_units}
pmc: {pmc_name}"""
        return pattern.format(
            entity_id=self.entity_id,
            name=self.name,
            nr_cams=len(self.cameras),
            nr_doors=len(self.doors),
            nr_units=len(self.units),
            pmc_name=self.pmc_name
        )

    @staticmethod
    def _get_eagleeye_session(carson_api, building_id):
        """Retrieve a new eagle eye auth key and subdomain information

        Args:
            carson_api: The carson living api object
            building_id: The building id of the Carson property

        Returns:
            (tuple): tuple containing:

                sessionid(str): Eagle Eye authentication token for account
                subdomain(str): Eagle Eye subdomain to use with account

        """
        url = C_API_URI + C_EEN_SESSION_ENDPOINT.format(building_id)
        session = carson_api.authenticated_query(url)
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
        # Update existing via Eagle Eye.
        self._eagleeye.update()

        # Cameras are managed by Eagle Eye API and
        # Carson Living only contains filter view of
        # Eagle Eye API
        self._cameras = {
            c['liveViewId']: self._eagleeye.get_camera(c['liveViewId'])
            for c in self.entity_payload.get('cameras')
            if c['provider'] == 'eagle_eye'
        }

    def _update_doors(self):
        update_doors = {d['id']: d for d in self.entity_payload.get('doors')}

        update_dictionary(
            self._doors,
            update_doors,
            lambda p: CarsonDoor(
                self._api,
                entity_payload=p))

    @property
    def eagleeye_api(self):
        """Eagle Eye API

        Returns: Eagle Eye API associated with that building.

        """
        return self._eagleeye

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

    def __str__(self):
        pattern = """\
id: {entity_id}
first name: {first_name}
last name: {last_name}
contact info: {contact_info}
verified: {verfied}
is_admin: {is_admin}"""
        return pattern.format(
            entity_id=self.entity_id,
            first_name=self.first_name,
            last_name=self.last_name,
            contact_info=', '.join(
                ['{}: {}'.format(c['type'], c['contact_info'])
                 for c in self.contact_info]),
            verfied=self.verified,
            is_admin=self.is_admin
        )

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

    def __str__(self):
        pattern = """\
id: {entity_id}
name: {name}
provider: {provider}
is_active: {is_active}
is_unit_door: {is_unit_door}
default_in_building: {default_in_building}"""
        return pattern.format(
            entity_id=self.entity_id,
            name=self.name,
            provider=self.provider,
            is_active=self.is_active,
            is_unit_door=self.is_unit_door,
            default_in_building=self.default_in_building
        )

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
        url = C_API_URI + C_DOOR_OPEN_ENDPOINT.format(self.entity_id)
        self._api.authenticated_query(url, method='post')
