# -*- coding: utf-8 -*-
"""Carson API Module for Carson Living tests."""

import requests_mock

from carson_living.const import API_VERSION

from tests.test_base import CarsonUnitTestBase
from tests.helpers import load_fixture


class TestCarson(CarsonUnitTestBase):
    """Carson Living API test class."""

    def test_api_initialization(self):
        """Test correct API initialization"""
        # Test
        self.assertTrue(self.init_me_mock.called)
        self.assertIsNotNone(self.carson)

    def test_api_user_initialization(self):
        """Test correct user entity after initialization"""
        user = self.carson.user
        self.assertIsNotNone(user)
        self.assertEqual(
            self.mock_carson_me.get('id'),
            user.entity_id)
        self.assertEqual(
            'carson_user_' + str(self.mock_carson_me.get('id')),
            user.unique_entity_id)
        self.assertEqual(
            self.mock_carson_me.get('firstName'),
            user.first_name)
        self.assertEqual(
            self.mock_carson_me.get('lastName'),
            user.last_name)

        self.assertEqual(2, len(user.contact_info))
        for i in range(len(user.contact_info)):
            self.assertEqual(
                self.mock_carson_me['contactInfo'][i]['contactInfo'],
                user.contact_info[i]['contact_info']
            )
            self.assertEqual(
                self.mock_carson_me['contactInfo'][i]['type'],
                user.contact_info[i]['type']
            )
            self.assertEqual(
                self.mock_carson_me['contactInfo'][i]['primary'],
                user.contact_info[i]['primary']
            )
            self.assertEqual(
                self.mock_carson_me['contactInfo'][i]['verified'],
                user.contact_info[i]['verified']
            )

        self.assertEqual(
            self.mock_carson_me['photo']['url'],
            user.photo.get('url'))
        self.assertEqual(
            self.mock_carson_me['photo']['thumbnailUrl'],
            user.photo.get('thumbnail_url'))

        self.assertEqual(
            self.mock_carson_me['verified'],
            user.verified)
        self.assertEqual(
            self.mock_carson_me['isAdmin'],
            user.is_admin)
        self.assertEqual(
            self.mock_carson_me['isService'],
            user.is_service)

    def test_api_buildings_initialization(self):
        """Test correct buildings entities after initialization"""
        buildings = self.carson.buildings
        self.assertEqual(1, len(buildings))

        mock_building_payload = self.mock_carson_me['properties'][0]
        main_building = next(iter(self.carson.buildings))

        self.assertEqual(
            'carson_building_' + str(mock_building_payload.get('id')),
            main_building.unique_entity_id
        )

        # Check mapping
        self.assertEqual(
            mock_building_payload['name'],
            main_building.name
        )
        self.assertEqual(
            mock_building_payload['type'],
            main_building.type
        )
        self.assertEqual(
            mock_building_payload['paymentsEnabled'],
            main_building.payments_enabled
        )
        self.assertEqual(
            mock_building_payload['area'],
            main_building.area
        )
        self.assertEqual(
            mock_building_payload['visitorInviteEnabled'],
            main_building.visitor_invite_enabled
        )
        self.assertEqual(
            mock_building_payload['doorsAvailable'],
            main_building.doors_available
        )
        self.assertEqual(
            mock_building_payload['pmcName'],
            main_building.pmc_name
        )
        self.assertEqual(
            mock_building_payload['serviceRequestsEnabled'],
            main_building.service_requests_enabled
        )
        self.assertEqual(
            mock_building_payload['country'],
            main_building.country
        )
        self.assertEqual(
            mock_building_payload['state'],
            main_building.state
        )
        self.assertEqual(
            mock_building_payload['timezone'],
            main_building.timezone
        )

        self.assertEqual(1, len(main_building.units))
        for i in range(len(main_building.units)):
            self.assertEqual(
                mock_building_payload['units'][i]['name'],
                main_building.units[i]['name']
            )
            self.assertEqual(
                mock_building_payload['units'][i]['paymentsEnabled'],
                main_building.units[i]['payments_enabled']
            )

    def test_api_camera_initialization(self):
        """Test correct cameras after initialization"""
        main_building = next(iter(self.carson.buildings))
        cameras = main_building.cameras
        self.assertEqual(2, len(cameras))

    def test_api_door_initialization(self):
        """Test correct doors after initialization"""
        main_building = next(iter(self.carson.buildings))
        mock_building_payload = self.mock_carson_me['properties'][0]

        doors = main_building.doors
        self.assertEqual(3, len(doors))

        i = 0
        for door in doors:
            mock_door_payload = mock_building_payload['doors'][i]
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

        main_building = next(iter(self.carson.buildings))
        mock_building_payload = self.mock_carson_me['properties'][0]

        doors = main_building.doors

        i = 0
        for door in doors:
            with requests_mock.mock() as mock:
                mock_door_payload = mock_building_payload['doors'][i]
                mock.post(
                    'https://api.carson.live/api/{}/doors/{}/open/'
                    .format(API_VERSION, mock_door_payload['id']),
                    text=load_fixture('carson.live', 'carson_door_open.json')
                )

                # execute
                door.open()

                self.assertTrue(mock.called)
                self.assertEqual(1, mock.call_count)
                i += 1
