"""Eagle Eye API Entities"""

from carson_living.entities import _AbstractAPIEntity

from carson_living.const import (EAGLE_EYE_API_URI,
                                 EAGLE_EYE_DEVICE_ENDPOINT)


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
