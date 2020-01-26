# -*- coding: utf-8 -*-
"""Carson API Module for Carson Living tests."""

import requests_mock

from tests.test_base import CarsonUnitTestBase


class TestCarson(CarsonUnitTestBase):
    """Carson Living API test class."""

    def test_api_initialization(self):
        """Test correct API initialization"""
        # Test
        self.assertIsNotNone(self.carson)

    def test_api_user_initialization(self):
        """Test correct user entity after initialization"""
        user = self.carson.user
        self.assertIsNotNone(user)
        self.assertEqual(
            self.c_mock_me.get('id'),
            user.entity_id)
        self.assertEqual(
            'carson_user_' + str(self.c_mock_me.get('id')),
            user.unique_entity_id)
        self.assertEqual(
            self.c_mock_me.get('firstName'),
            user.first_name)
        self.assertEqual(
            self.c_mock_me.get('lastName'),
            user.last_name)

        self.assertEqual(2, len(user.contact_info))
        for i in range(len(user.contact_info)):
            self.assertEqual(
                self.c_mock_me['contactInfo'][i]['contactInfo'],
                user.contact_info[i]['contact_info']
            )
            self.assertEqual(
                self.c_mock_me['contactInfo'][i]['type'],
                user.contact_info[i]['type']
            )
            self.assertEqual(
                self.c_mock_me['contactInfo'][i]['primary'],
                user.contact_info[i]['primary']
            )
            self.assertEqual(
                self.c_mock_me['contactInfo'][i]['verified'],
                user.contact_info[i]['verified']
            )

        self.assertEqual(
            self.c_mock_me['photo']['url'],
            user.photo.get('url'))
        self.assertEqual(
            self.c_mock_me['photo']['thumbnailUrl'],
            user.photo.get('thumbnail_url'))

        self.assertEqual(
            self.c_mock_me['verified'],
            user.verified)
        self.assertEqual(
            self.c_mock_me['isAdmin'],
            user.is_admin)
        self.assertEqual(
            self.c_mock_me['isService'],
            user.is_service)

        self.assertIn(str(user.entity_id), str(user))
        self.assertIn(user.first_name, str(user))
        self.assertIn(user.last_name, str(user))

        self.assertIn(user.unique_entity_id, repr(user))
        self.assertIn("CarsonUser", repr(user))

    def test_api_buildings_initialization(self):
        """Test correct buildings entities after initialization"""
        buildings = self.carson.buildings
        self.assertEqual(1, len(buildings))

        self.assertEqual(
            'carson_building_' + str(self.c_mock_first_property.get('id')),
            self.first_building.unique_entity_id
        )

        # Check mapping
        self.assertEqual(
            self.c_mock_first_property['name'],
            self.first_building.name
        )
        self.assertEqual(
            self.c_mock_first_property['type'],
            self.first_building.type
        )
        self.assertEqual(
            self.c_mock_first_property['paymentsEnabled'],
            self.first_building.payments_enabled
        )
        self.assertEqual(
            self.c_mock_first_property['area'],
            self.first_building.area
        )
        self.assertEqual(
            self.c_mock_first_property['visitorInviteEnabled'],
            self.first_building.visitor_invite_enabled
        )
        self.assertEqual(
            self.c_mock_first_property['doorsAvailable'],
            self.first_building.doors_available
        )
        self.assertEqual(
            self.c_mock_first_property['pmcName'],
            self.first_building.pmc_name
        )
        self.assertEqual(
            self.c_mock_first_property['serviceRequestsEnabled'],
            self.first_building.service_requests_enabled
        )
        self.assertEqual(
            self.c_mock_first_property['country'],
            self.first_building.country
        )
        self.assertEqual(
            self.c_mock_first_property['state'],
            self.first_building.state
        )
        self.assertEqual(
            self.c_mock_first_property['timezone'],
            self.first_building.timezone
        )

        self.assertEqual(1, len(self.first_building.units))
        for i in range(len(self.first_building.units)):
            self.assertEqual(
                self.c_mock_first_property['units'][i]['name'],
                self.first_building.units[i]['name']
            )
            self.assertEqual(
                self.c_mock_first_property['units'][i]['paymentsEnabled'],
                self.first_building.units[i]['payments_enabled']
            )

        self.assertEqual(3, len(self.first_building.doors))

        # Carson Building returns 2 cameras
        self.assertEqual(2, len(self.first_building.cameras))

        # Eagle Eye API returns 8 cameras
        self.assertIsNotNone(self.first_building.eagleeye_api)
        self.assertEqual(8, len(self.first_building.eagleeye_api.cameras))

        self.assertIn(str(self.first_building.entity_id),
                      str(self.first_building))
        self.assertIn(self.first_building.name,
                      str(self.first_building))
        self.assertIn(self.first_building.pmc_name,
                      str(self.first_building))

        self.assertIn(self.first_building.unique_entity_id,
                      repr(self.first_building))
        self.assertIn("CarsonBuilding",
                      repr(self.first_building))

    @requests_mock.Mocker()
    def test_later_carson_update_changes_entities(self, mock):
        """Later calling update changes the entities"""
        self._init_default_mocks(mock, 'carson_me_update.json')

        self.carson.update()

        self.assertTrue(mock.called)

        # User updated successfully
        self.assertEqual(
            self.c_mock_me.get('firstName'),
            self.carson.user.first_name
        )

        self.assertEqual(2, len(self.carson.buildings))
        i = 0
        for building in self.carson.buildings:
            # Building updated successfully
            self.assertEqual(
                self.c_mock_me['properties'][i]['name'],
                building.name
            )
            i += 1

        # Camera deleted, changed, added
        self.assertEqual(3, len(self.first_building.cameras))

        # Door deleted, changed, added
        self.assertEqual(4, len(self.first_building.doors))
