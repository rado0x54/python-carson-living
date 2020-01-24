"""Eagle Eye API Entities"""

from carson_living.entities import _AbstractAPIEntity

from carson_living.const import (EAGLE_EYE_API_URI,
                                 EAGLE_EYE_DEVICE_ENDPOINT)


class EagleEyeCamera(_AbstractAPIEntity):
    """Eagle Eye Camera Entity

    The eagle eye camera is initialized with the device/list payload to
    allow for fast initialization

    """
    def __init__(self, api, entity_payload):
        super(EagleEyeCamera, self).__init__(
            api,
            update_callback=self._get_payload_internal,
            entity_payload=entity_payload
        )

    @classmethod
    def from_api(cls, api, camera_id):
        """Init Camera from API call

        Args:
            api: Eagle Eye API
            camera_id: Eagle Eye Camera ID

        Returns:
            Initialized EagleEyeCamera

        """
        entity_payload = cls.get_payload(api, camera_id)
        return cls(api, entity_payload)

    @classmethod
    def from_list_payload(cls, api, list_entity_payload):
        """Init Camera from List Payload

        Args:
            api: Eagle Eye API
            list_entity_payload:
                Eagle Eye JSON from /list call

        Returns:
            Initialized EagleEyeCamera

        """
        entity_payload = cls.map_list_to_entity_payload(list_entity_payload)
        return cls(api, entity_payload)

    @staticmethod
    def map_list_to_entity_payload(list_entity_payload):
        """Map from list to entity payload

        Args:
            list_entity_payload:
                Eagle eye list payload

        Returns:
            Eagle eye entity payload

        """
        return {
            "bridges": {
                b[0]: b[1] for b in list_entity_payload[4]
            },
            "name": list_entity_payload[2],
            "tags": list_entity_payload[7],
            "utcOffset": list_entity_payload[12],
            "timezone": list_entity_payload[11],
            "permissions": list_entity_payload[6],
            "guid": list_entity_payload[8],
            "id": list_entity_payload[1],
            "account_id": list_entity_payload[0]
        }

    def _get_payload_internal(self):
        return self.get_payload(self._api, self.entity_id)

    @staticmethod
    def get_payload(api, camera_id):
        """Get entity payload from API

        Args:
            api: Eagle Eye API
            camera_id: Eagle Eye Camera ID

        Returns:
            Eagle eye entity payload

        """
        url = EAGLE_EYE_API_URI + EAGLE_EYE_DEVICE_ENDPOINT
        return api.authenticated_query(
            url, params={'id': camera_id})

    @property
    def unique_entity_id(self):
        return 'eagleeye_camera_{}'.format(self.entity_id)

    def _internal_update(self):
        pass

    @property
    def entity_id(self):
        return self._entity_payload.get('id')

    def __str__(self):
        pattern = """\
id: {entity_id}
name: {name}
account id: {account_id}
guid: {guid}
tags: {tags}"""
        return pattern.format(
            entity_id=self.entity_id,
            name=self.name,
            account_id=self.account_id,
            guid=self.guid,
            tags=', '.join(self.tags)
        )

    @property
    def account_id(self):
        """Account id

        Returns: Eagle Eye Account Id for that camera

        """
        return self._entity_payload.get('account_id')

    @property
    def name(self):
        """Name

        Returns: Device name

        """
        return self._entity_payload.get('name')

    @property
    def utc_offset(self):
        """UTC offset

        Returns: Signed UTC offset in seconds of the set 'timezone'

        """
        return self._entity_payload.get('utcOffset')

    @property
    def timezone(self):
        """Timezone

        Returns: tz database string of the camera

        """
        return self._entity_payload.get('timezone')

    @property
    def guid(self):
        """GUID

        Returns:
            The GUID (Globally Unique Identifier) is an immutable device
            identifier

        """
        return self._entity_payload.get('guid')

    @property
    def permissions(self):
        """Permissions

        Returns:
            String of characters each defining a permission level of
            the current user

        """
        return self._entity_payload.get('permissions')

    @property
    def tags(self):
        """Tags

        Returns:
            Array of strings each representing a tag name

        """
        return self._entity_payload.get('tags')

    @property
    def bridges(self):
        """Bridges

        Returns:
            Json object of bridges (ESNs) this device is seen by and the
            camera attach status:

        """
        return self._entity_payload.get('bridges')
