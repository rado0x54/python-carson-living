"""Eagle Eye API Entities"""
import shutil

from requests import Request

from carson_living.entities import _AbstractAPIEntity

from carson_living.const import (EEN_API_URI,
                                 EEN_DEVICE_ENDPOINT,
                                 EEN_GET_IMAGE_ENDPOINT,
                                 EEN_GET_VIDEO_ENDPOINT,
                                 EEN_ASSET_CLS_PRE,
                                 EEN_ASSET_REF_PREV,
                                 EEN_VIDEO_FORMAT_FLV)

from carson_living.error import CarsonAPIError

from carson_living.util import (current_milli_time,
                                timedelta_to_milli_time)


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
        url = EEN_API_URI + EEN_DEVICE_ENDPOINT
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

    @staticmethod
    def utc_to_een_timestamp(utc_dt):
        """Convert utc_dt to EEN string

        Note, no timezone conversion is performed, please make sure the
        Datetime object is in UTC.

        Args:
            utc_dt: Datetime object in UTC

        Returns: EEN timestamp format

        """
        return utc_dt.strftime('%Y%m%d%H%M%S.%f')[:-3]

    @staticmethod
    def _get_video_timestamps(length, utc_dt, video_format):
        # default are download parameters
        time_millies = current_milli_time()
        length_millies = timedelta_to_milli_time(length)

        # Live case
        start_ts = 'stream_{}'.format(time_millies)
        end_ts = '+{}'.format(length_millies)

        if utc_dt is None:
            if video_format != EEN_VIDEO_FORMAT_FLV:
                raise CarsonAPIError(
                    'Live video streaming is only possible with .flv')
        else:
            # Not live
            start_ts = EagleEyeCamera.utc_to_een_timestamp(utc_dt)
            end_ts = EagleEyeCamera.utc_to_een_timestamp(utc_dt + length)

        return start_ts, end_ts

    def get_image(self, file,
                  utc_dt=None,
                  asset_ref=EEN_ASSET_REF_PREV,
                  asset_class=EEN_ASSET_CLS_PRE):
        """Get binary JPEG image from the camera

        Args:
            file:
                file handler that is written to.
            utc_dt:
                Datetime object in UTC
            asset_ref:
                prev: previous image to time stamp
                next: next image to timestamp (blocks)
                asset: image at timestamp
            asset_class:
                all, pre, thumb

        Returns:
            JPEG Image
        """
        def _response_file_handler(response):
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)

        timestamp = 'now'
        if utc_dt is not None:
            timestamp = self.utc_to_een_timestamp(utc_dt)

        url = EEN_API_URI + EEN_GET_IMAGE_ENDPOINT.format(
            asset_ref)
        return self._api.authenticated_query(
            url, params={'id': self.entity_id,
                         'timestamp': timestamp,
                         'asset_class': asset_class},
            stream=True,
            response_handler=_response_file_handler)

    # Not this is quite duplicate at the moment, but a major refactor
    # would be needed to return a prepared url via authenticated_query
    def get_image_url(self, utc_dt=None,
                      asset_ref=EEN_ASSET_REF_PREV,
                      asset_class=EEN_ASSET_CLS_PRE,
                      check_auth=True):
        """Get JPEG image URL from the camera

        Args:
            utc_dt:
                Datetime object in UTC
            asset_ref:
                prev: previous image to time stamp
                next: next image to timestamp (blocks)
                asset: image at timestamp
            asset_class:
                all, pre, thumb
            check_auth:
                Check auth token and refresh

        Returns:
            JPEG Image URL or None if not valid Auth exists
        """
        if check_auth and not self._api.check_auth():
            return None

        timestamp = 'now'
        if utc_dt is not None:
            timestamp = self.utc_to_een_timestamp(utc_dt)

        url = EEN_API_URI.format(
            self._api.session_brand_subdomain
        ) + EEN_GET_IMAGE_ENDPOINT.format(
            asset_ref
        )

        prepared = Request(url=url, params={
            'id': self.entity_id,
            'timestamp': timestamp,
            'asset_class': asset_class,
            'A': self._api.session_auth_key}).prepare()
        return prepared.url

    # stream Live video to file
    def get_video(self, file, length, utc_dt=None,
                  video_format=EEN_VIDEO_FORMAT_FLV):
        """Get a (live) video stream from the camera

        Args:
            file: file handler for the response
            length: of the stream in timedelta
            video_format: flv or mp4
            utc_dt: utc timestamp for video, live for None

        Returns:
            Video stream to file
        """
        def _response_file_handler(response):
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)

        start_ts, end_ts = self._get_video_timestamps(
            length, utc_dt, video_format)

        url = EEN_API_URI + EEN_GET_VIDEO_ENDPOINT.format(
            video_format)
        return self._api.authenticated_query(
            url, params={'id': self.entity_id,
                         'start_timestamp': start_ts,
                         'end_timestamp': end_ts},
            stream=True,
            response_handler=_response_file_handler)

    # Not this is quite duplicate at the moment, but a major refactor
    # would be needed to return a prepared url via authenticated_query
    def get_video_url(self, length, utc_dt=None,
                      video_format=EEN_VIDEO_FORMAT_FLV, check_auth=True):
        """Get a (live) video stream from the camera

        Args:
            file: file handler for the response
            length: of the stream in timedelta
            video_format: flv or mp4
            utc_dt: utc timestamp for video, live for None
            check_auth: Check auth token and refresh

        Returns:
            Video url or None if not valid Auth exists
        """
        if check_auth and not self._api.check_auth():
            return None

        start_ts, end_ts = self._get_video_timestamps(
            length, utc_dt, video_format)

        url = EEN_API_URI.format(
            self._api.session_brand_subdomain
        ) + EEN_GET_VIDEO_ENDPOINT.format(
            video_format
        )

        prepared = Request(url=url, params={
            'id': self.entity_id,
            'start_timestamp': start_ts,
            'end_timestamp': end_ts,
            'A': self._api.session_auth_key}).prepare()
        return prepared.url
