# -*- coding: utf-8 -*-
"""Carson API Module for Carson Living tests."""
import io
from datetime import datetime
from datetime import timedelta

import requests_mock

from carson_living import (EagleEyeCamera,
                           CarsonAPIError,
                           EEN_VIDEO_FORMAT_MP4)

from tests.test_base import CarsonUnitTestBase
from tests.helpers import (setup_ee_camera_mock,
                           setup_ee_image_mock,
                           setup_ee_video_mock)

# 2.7 support fallback
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class TestCamera(CarsonUnitTestBase):
    """Carson Living camera entity test class."""

    def test_api_camera_initialization(self):
        """Test correct cameras after initialization"""
        cameras = self.first_building.cameras
        self.assertEqual(2, len(cameras))

        mock_camera_dict = {d[1]: d
                            for d in self.e_mock_device_list}

        for camera in cameras:
            mock_camera = mock_camera_dict[camera.entity_id]
            self.assertEqual(mock_camera[0], camera.account_id)
            self.assertEqual(mock_camera[1], camera.entity_id)
            self.assertEqual(
                'eagleeye_camera_' + mock_camera[1],
                camera.unique_entity_id
            )
            self.assertEqual(mock_camera[2], camera.name)
            self.assertEqual(mock_camera[12], camera.utc_offset)
            self.assertEqual(mock_camera[11], camera.timezone)
            self.assertEqual(mock_camera[6], camera.permissions)
            self.assertEqual(mock_camera[8], camera.guid)
            self.assertEqual(mock_camera[7], camera.tags)
            self.assertEqual(
                {d[0]: d[1] for d in mock_camera[4]},
                camera.bridges
            )

            self.assertIn(str(camera.entity_id), str(camera))
            self.assertIn(camera.name, str(camera))
            self.assertIn(camera.account_id, str(camera))
            self.assertIn(camera.guid, str(camera))

            self.assertIn(camera.unique_entity_id, repr(camera))
            self.assertIn("EagleEyeCamera", repr(camera))

    @requests_mock.Mocker()
    def test_api_call_back_update(self, mock):
        """Test Camera update via api"""
        # Camera ID Mocks
        subdomain = self.c_mock_esession['activeBrandSubdomain']
        e_mock_camera = setup_ee_camera_mock(
            mock, subdomain, 'device_camera_update.json')

        first_camera = next(iter(self.first_building.cameras))
        first_camera.update()

        self.assertEqual(1, mock.call_count)

        self.assertEqual(e_mock_camera['name'], first_camera.name)

    @requests_mock.Mocker()
    def test_payload_and_api_init_are_equal(self, mock):
        """Test equal initialization class methods"""
        # Camera ID Mocks
        subdomain = self.c_mock_esession['activeBrandSubdomain']
        setup_ee_camera_mock(
            mock, subdomain, 'device_camera.json')

        ee_api = self.first_building.eagleeye_api
        camera_id = "random_id"

        c_api = EagleEyeCamera.from_api(ee_api, camera_id)
        c_payload = EagleEyeCamera.from_list_payload(
            ee_api, self.e_mock_device_list[0])

        self.assertEqual(c_api.account_id, c_payload.account_id)
        self.assertEqual(c_api.entity_id, c_payload.entity_id)
        self.assertEqual(c_api.unique_entity_id, c_payload.unique_entity_id)
        self.assertEqual(c_api.name, c_payload.name)
        self.assertEqual(c_api.utc_offset, c_payload.utc_offset)
        self.assertEqual(c_api.timezone, c_payload.timezone)
        self.assertEqual(c_api.permissions, c_payload.permissions)
        self.assertEqual(c_api.guid, c_payload.guid)
        self.assertEqual(c_api.tags, c_payload.tags)
        self.assertEqual(c_api.bridges, c_payload.bridges)

    def test_een_timestamp_conversion(self):
        """Test correct EEN conversion"""
        sample_dt = datetime(2020, 1, 31, 23, 1, 3, 123456)
        sample_dt_str = EagleEyeCamera.utc_to_een_timestamp(sample_dt)
        self.assertEqual("20200131230103.123", sample_dt_str)

    @requests_mock.Mocker()
    def test_camera_get_image(self, mock):
        """Test get image function"""
        subdomain = self.c_mock_esession['activeBrandSubdomain']
        mock_image = setup_ee_image_mock(mock, subdomain)

        first_camera = next(iter(self.first_building.cameras))
        sample_dt = datetime(2020, 1, 31, 23, 1, 3, 123456)

        buffer = io.BytesIO()
        first_camera.get_image(buffer, sample_dt)

        self.assertEqual(mock_image, buffer.getvalue())
        self.assertEqual(1, mock.call_count)
        self.assertNotIn('A=', mock.last_request.url)

    def test_camera_get_image_url(self):
        """Test get image url function"""
        first_camera = next(iter(self.first_building.cameras))
        sample_dt = datetime(2020, 1, 31, 23, 1, 3, 123456)

        url = first_camera.get_image_url(sample_dt, check_auth=False)

        self.assertIn('id=', url)
        self.assertIn('timestamp=20200131230103.123', url)
        self.assertIn('asset_class=', url)
        self.assertIn('A=', url)

    @requests_mock.Mocker()
    def test_camera_get_live_video(self, mock):
        """Test get live video function"""
        subdomain = self.c_mock_esession['activeBrandSubdomain']
        mock_video = setup_ee_video_mock(mock, subdomain)

        first_camera = next(iter(self.first_building.cameras))

        buffer = io.BytesIO()
        first_camera.get_video(buffer, timedelta(seconds=2))

        self.assertEqual(mock_video, buffer.getvalue())
        self.assertEqual(1, mock.call_count)
        self.assertIn('stream_', mock.last_request.url)
        self.assertNotIn('A=', mock.last_request.url)

    @requests_mock.Mocker()
    def test_camera_get_video(self, mock):
        """Test get video stream"""
        sample_dt = datetime(2020, 1, 24, 15, 1, 3, 123456)
        subdomain = self.c_mock_esession['activeBrandSubdomain']
        mock_video = setup_ee_video_mock(mock, subdomain, EEN_VIDEO_FORMAT_MP4)

        first_camera = next(iter(self.first_building.cameras))

        buffer = io.BytesIO()
        first_camera.get_video(buffer, timedelta(seconds=30),
                               sample_dt, EEN_VIDEO_FORMAT_MP4)

        self.assertEqual(mock_video, buffer.getvalue())
        self.assertEqual(1, mock.call_count)
        self.assertIn('video.mp4', mock.last_request.url)
        self.assertIn('=20200124150103.123', mock.last_request.url)
        self.assertNotIn('stream_', mock.last_request.url)
        self.assertNotIn('A=', mock.last_request.url)

    def test_camera_get_live_video_url(self):
        """Test live video URL"""
        first_camera = next(iter(self.first_building.cameras))

        url_live = first_camera.get_video_url(
            timedelta(seconds=30), check_auth=False)

        self.assertIn('video.flv', url_live)
        self.assertIn('id=', url_live)
        self.assertIn('start_timestamp=stream_', url_live)
        self.assertIn('end_timestamp=%2B', url_live)
        self.assertIn('A=', url_live)

    def test_camera_get_video_url(self):
        """Test video URL"""
        first_camera = next(iter(self.first_building.cameras))

        sample_dt = datetime(2020, 1, 24, 15, 1, 3, 123456)
        url = first_camera.get_video_url(
            timedelta(seconds=30), sample_dt,
            EEN_VIDEO_FORMAT_MP4, check_auth=False)

        self.assertIn('video.mp4', url)
        self.assertIn('id=', url)
        self.assertIn('start_timestamp=', url)
        self.assertIn('end_timestamp=', url)
        self.assertNotIn('start_timestamp=stream_', url)
        self.assertNotIn('end_timestamp=%2B', url)
        self.assertIn('A=', url)

    def test_camera_get_live_video_url_throws_mp4(self):
        """Live video cannot be video_format mp4"""
        first_camera = next(iter(self.first_building.cameras))

        with self.assertRaises(CarsonAPIError):
            first_camera.get_video_url(
                timedelta(seconds=30), video_format=EEN_VIDEO_FORMAT_MP4,
                check_auth=False)

    def test_camera_get_live_video_throws_mp4(self):
        """Live video cannot be video_format mp4"""
        first_camera = next(iter(self.first_building.cameras))
        buffer = io.BytesIO()

        with self.assertRaises(CarsonAPIError):
            first_camera.get_video(buffer, timedelta(seconds=2))

    def test_camera_get_image_url_check_auth(self):
        """Test get image url function"""
        self.first_building.eagleeye_api.check_auth = Mock(return_value=True)
        first_camera = next(iter(self.first_building.cameras))

        url = first_camera.get_image_url()

        self.assertIn('id=', url)
        self.assertIn('timestamp=', url)
        self.assertIn('asset_class=', url)
        self.assertIn('A=', url)

        self.first_building.eagleeye_api.check_auth.assert_called_with()

    def test_camera_get_live_video_url_check_auth(self):
        """Test live video URL"""
        self.first_building.eagleeye_api.check_auth = Mock(return_value=True)
        first_camera = next(iter(self.first_building.cameras))

        url_live = first_camera.get_video_url(timedelta(seconds=30))

        self.assertIn('video.flv', url_live)
        self.assertIn('id=', url_live)
        self.assertIn('start_timestamp=stream_', url_live)
        self.assertIn('end_timestamp=%2B', url_live)
        self.assertIn('A=', url_live)

        self.first_building.eagleeye_api.check_auth.assert_called_with()

    def test_camera_get_image_url_check_auth_fails(self):
        """Test get image url function"""

        self.first_building.eagleeye_api.check_auth = Mock(return_value=False)
        first_camera = next(iter(self.first_building.cameras))

        url = first_camera.get_image_url()

        self.assertIsNone(url)
        self.first_building.eagleeye_api.check_auth.assert_called_with()

    def test_camera_get_live_video_url_check_auth_fails(self):
        """Test live video URL"""
        self.first_building.eagleeye_api.check_auth = Mock(return_value=False)
        first_camera = next(iter(self.first_building.cameras))

        url_live = first_camera.get_video_url(timedelta(seconds=30))

        self.assertIsNone(url_live)
        self.first_building.eagleeye_api.check_auth.assert_called_with()
