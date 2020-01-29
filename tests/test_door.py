# -*- coding: utf-8 -*-
"""Carson API Module for Carson Living tests."""

import requests_mock

from carson_living.const import C_API_VERSION

from tests.test_base import CarsonUnitTestBase
from tests.helpers import load_fixture


class TestDoor(CarsonUnitTestBase):
    """Carson Living door entity test class."""

    def test_api_initialization(self):
        """Test correct API initialization"""
        # Test
        self.assertIsNotNone(self.carson)

    def test_api_door_initialization(self):
        """Test correct doors after initialization"""
        doors = self.first_building.doors
        self.assertEqual(3, len(doors))

        i = 0
        for door in doors:
            mock_door_payload = self.c_mock_first_property['doors'][i]
            self.assertEqual(
                'carson_door_' + str(mock_door_payload['id']),
                door.unique_entity_id
            )
            self.assertEqual(
                mock_door_payload['name'],
                door.name
            )
            self.assertEqual(
                mock_door_payload['provider'],
                door.provider
            )
            self.assertEqual(
                mock_door_payload['isActive'],
                door.is_active
            )
            self.assertEqual(
                mock_door_payload['disabled'],
                door.disabled
            )
            self.assertEqual(
                mock_door_payload['isUnitDoor'],
                door.is_unit_door
            )
            self.assertEqual(
                mock_door_payload['staffOnly'],
                door.staff_only
            )
            self.assertEqual(
                mock_door_payload['defaultInBuilding'],
                door.default_in_building
            )
            self.assertEqual(
                mock_door_payload['externalId'],
                door.external_id
            )
            self.assertEqual(
                mock_door_payload['available'],
                door.available
            )
            self.assertEqual(
                mock_door_payload['order'],
                door.order
            )

            i += 1

    def test_api_door_open(self):
        """Test correct door open"""
        doors = self.first_building.doors

        i = 0
        for door in doors:
            with requests_mock.Mocker() as mock:
                mock_door_payload = self.c_mock_first_property['doors'][i]
                mock.post(
                    'https://api.carson.live/api/{}/doors/{}/open/'
                    .format(C_API_VERSION, mock_door_payload['id']),
                    text=load_fixture('carson.live', 'carson_door_open.json')
                )

                # execute
                door.open()

                self.assertEqual(1, mock.call_count)
                i += 1
