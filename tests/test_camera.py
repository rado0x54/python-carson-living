# -*- coding: utf-8 -*-
"""Carson API Module for Carson Living tests."""

import requests_mock

from carson_living import EagleEyeCamera

from tests.test_base import CarsonUnitTestBase
from tests.helpers import setup_ee_camera_mock


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