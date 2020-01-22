# -*- coding: utf-8 -*-
"""Carson API Module for Carson Living tests."""

from tests.test_base import CarsonUnitTestBase


class TestCamera(CarsonUnitTestBase):
    """Carson Living camera entity test class."""

    def test_api_camera_initialization(self):
        """Test correct cameras after initialization"""
        cameras = self.first_building.cameras
        self.assertEqual(2, len(cameras))

        first_camera = next(iter(cameras))

        # ID is initalized from Carson Object
        mock_camera_id = self.c_mock_first_camera['externalId']

        self.assertEqual(
            mock_camera_id,
            first_camera.entity_id
        )
        self.assertEqual(
            'eagleeye_camera_' + mock_camera_id,
            first_camera.unique_entity_id
        )

        # Other properties
        self.assertEqual(
            self.e_mock_camera['name'],
            first_camera.name
        )
        self.assertEqual(
            self.e_mock_camera['settings'],
            first_camera.settings
        )
        self.assertEqual(
            self.e_mock_camera['utcOffset'],
            first_camera.utc_offset
        )
        self.assertEqual(
            self.e_mock_camera['timezone'],
            first_camera.timezone
        )
        self.assertEqual(
            self.e_mock_camera['guid'],
            first_camera.guid
        )
        self.assertEqual(
            self.e_mock_camera['permissions'],
            first_camera.permissions
        )
        self.assertEqual(
            self.e_mock_camera['tags'],
            first_camera.tags
        )
        self.assertEqual(
            self.e_mock_camera['bridges'],
            first_camera.bridges
        )
        self.assertEqual(
            self.e_mock_camera['camera_parameters_status_code'],
            first_camera.camera_parameters_status_code
        )
        self.assertEqual(
            self.e_mock_camera['camera_parameters'],
            first_camera.camera_parameters
        )
        self.assertEqual(
            self.e_mock_camera['camera_info_status_code'],
            first_camera.camera_info_status_code
        )
        self.assertEqual(
            self.e_mock_camera['camera_info'],
            first_camera.camera_info
        )
