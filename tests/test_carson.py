# -*- coding: utf-8 -*-
"""Carson API Module for Carson Living tests."""


from tests.test_base import CarsonUnitTestBase


class TestCarson(CarsonUnitTestBase):
    """Carson Living API test class."""

    def test_api_initialization(self):
        """Test correct API initialization"""
        # Test
        self.assertTrue(self.init_me_mock.called)
        self.assertIsNotNone(self.carson)

    def test_api_user_initialization(self):
        """Test correct user entity after initialization"""
        self.assertIsNotNone(self.carson.user)
        self.assertEqual(
            self.mock_carson_me.get('id'),
            self.carson.user.entity_id)
        self.assertEqual(
            'carson_user_' + str(self.mock_carson_me.get('id')),
            self.carson.user.unique_entity_id)
        self.assertEqual(
            self.mock_carson_me.get('firstName'),
            self.carson.user.first_name)
        self.assertEqual(
            self.mock_carson_me.get('lastName'),
            self.carson.user.last_name)

    def test_api_buildings_initialization(self):
        """Test correct buildings entities after initialization"""
        buildings = self.carson.buildings
        self.assertEqual(1, len(buildings))

    def test_api_camera_initialization(self):
        """Test correct cameras after initialization"""
        main_building = next(iter(self.carson.buildings))
        cameras = main_building.cameras
        self.assertEqual(2, len(cameras))

    def test_api_door_initialization(self):
        """Test correct doors after initialization"""
        main_building = next(iter(self.carson.buildings))
        doors = main_building.doors
        self.assertEqual(3, len(doors))
