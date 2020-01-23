# -*- coding: utf-8 -*-
"""Authentication Module for Carson Living tests."""

import unittest
import requests_mock

# 2.7 support fallback
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


from carson_living import (EagleEye,
                           CarsonError)

from tests.helpers import (setup_ee_device_list_mock,
                           setup_ee_camera_mock)

FIXTURE_SESSION_AUTH_KEY = 'sample_auth_key'
FIXTURE_BRANDED_SUBDOMAIN = 'sd'


class TestEagleEye(unittest.TestCase):
    """Carson Living authentication test class."""

    def setUp(self):
        with requests_mock.Mocker() as mock:
            setup_ee_device_list_mock(mock, FIXTURE_BRANDED_SUBDOMAIN)
            setup_ee_camera_mock(mock, FIXTURE_BRANDED_SUBDOMAIN)

            self.mock_session_callback = Mock(
                return_value=(FIXTURE_SESSION_AUTH_KEY,
                              FIXTURE_BRANDED_SUBDOMAIN))

            self.eagle_eye = EagleEye(self.mock_session_callback)

    def test_correct_initialization(self):
        """Correct Initialization of EagleEye"""
        self.mock_session_callback.assert_called_once_with()
        self.assertEqual(8, len(self.eagle_eye.cameras))

    @requests_mock.Mocker()
    def test_authenticated_query(self, mock):
        """Test basic authenticated query mechanism"""
        query_url = 'https://test.com'
        mock.get(query_url, text='{}')

        self.eagle_eye.authenticated_query(query_url)

        self.assertTrue(mock.called_once)

    @requests_mock.Mocker()
    def test_update_session_on_401(self, mock):
        """Test Retry principle"""
        query_url = 'https://test.com'
        mock.get(query_url, status_code=401)

        retries = 3

        with self.assertRaises(CarsonError):
            self.eagle_eye.authenticated_query(query_url, retry_auth=retries)

        self.assertEqual(retries + 1, mock.call_count)
        self.assertEqual(retries + 1, self.mock_session_callback.call_count)

    @requests_mock.Mocker()
    def test_initialization_with_bad_cb_raises_callback_failure(self, mock):
        """Test exception on faulty callback"""
        mock_callback = Mock(
            return_value=(FIXTURE_SESSION_AUTH_KEY, None))

        with self.assertRaises(CarsonError):
            EagleEye(mock_callback)

        mock_callback.assert_called_once_with()
        self.assertEqual(0, mock.call_count)

    @requests_mock.Mocker()
    def test_api_updates_entities(self, mock):
        """Test exception on faulty callback"""
        setup_ee_device_list_mock(
            mock, FIXTURE_BRANDED_SUBDOMAIN, 'device_list_update.json')
        mock_camera_update = setup_ee_camera_mock(
            mock, FIXTURE_BRANDED_SUBDOMAIN, 'device_camera_update.json')

        self.eagle_eye.update()

        self.assertEqual(9, len(self.eagle_eye.cameras))

        for camera in self.eagle_eye.cameras:
            self.assertEqual(mock_camera_update['name'], camera.name)
