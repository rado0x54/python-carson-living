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

from carson_living.const import (EEN_API_URI,
                                 EEN_IS_AUTH_ENDPOINT)
from tests.helpers import setup_ee_device_list_mock

FIXTURE_SESSION_AUTH_KEY = 'sample_auth_key'
FIXTURE_BRANDED_SUBDOMAIN = 'sd'


class TestEagleEye(unittest.TestCase):
    """Carson Living authentication test class."""

    def setUp(self):
        with requests_mock.Mocker() as mock:
            setup_ee_device_list_mock(mock, FIXTURE_BRANDED_SUBDOMAIN)

            self.mock_session_callback = Mock(
                return_value=(FIXTURE_SESSION_AUTH_KEY,
                              FIXTURE_BRANDED_SUBDOMAIN))

            self.eagle_eye = EagleEye(self.mock_session_callback)
            self.eagle_eye.update()

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

        broken_eagle_eye = EagleEye(mock_callback)
        with self.assertRaises(CarsonError):
            broken_eagle_eye.update()

        mock_callback.assert_called_once_with()
        self.assertEqual(0, mock.call_count)

    @requests_mock.Mocker()
    def test_api_updates_entities(self, mock):
        """Test exception on faulty callback"""
        mock_camera_update = setup_ee_device_list_mock(
            mock, FIXTURE_BRANDED_SUBDOMAIN, 'device_list_update.json')

        mock_camera_dict = {d[1]: d for d in mock_camera_update}

        self.eagle_eye.update()

        self.assertEqual(9, len(self.eagle_eye.cameras))
        for camera in self.eagle_eye.cameras:
            mock_camera = mock_camera_dict[camera.entity_id]
            self.assertEqual(mock_camera[2], camera.name)

    def test_check_auth_false_on_empty_auth_key(self):
        """Correct Initialization of EagleEye"""
        mock_session_callback = Mock()

        eagle_eye = EagleEye(mock_session_callback)

        auth = eagle_eye.check_auth(refresh=False)
        self.assertEqual(False, auth)
        mock_session_callback.assert_not_called()

    @requests_mock.Mocker()
    def test_check_auth_auto_refreshes(self, mock):
        """Correct Initialization of EagleEye"""
        mock.get(EEN_API_URI.format(FIXTURE_BRANDED_SUBDOMAIN)
                 + EEN_IS_AUTH_ENDPOINT, status_code=200, text='true')

        auth = self.eagle_eye.check_auth(refresh=False)
        self.assertEqual(True, auth)
        self.assertEqual(1, mock.call_count)

    @requests_mock.Mocker()
    def test_check_auth_fails_on_zero_refresh(self, mock):
        """Correct Initialization of EagleEye"""
        mock.get(EEN_API_URI.format(FIXTURE_BRANDED_SUBDOMAIN)
                 + EEN_IS_AUTH_ENDPOINT, status_code=401)

        auth = self.eagle_eye.check_auth(refresh=False)
        self.assertEqual(False, auth)
        self.assertEqual(1, mock.call_count)
