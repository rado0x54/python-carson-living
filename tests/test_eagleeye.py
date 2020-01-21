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

FIXTURE_SESSION_AUTH_KEY = 'sample_auth_key'
FIXTURE_BRANDED_SUBDOMAIN = 'sd'


class TestCarsonAuth(unittest.TestCase):
    """Carson Living authentication test class."""

    @requests_mock.Mocker()
    def test_authenticated_query(self, mock):
        """Test Callback mechanism"""
        mock_callback = Mock(
            return_value=(FIXTURE_SESSION_AUTH_KEY, FIXTURE_BRANDED_SUBDOMAIN))

        query_url = 'https://test.com'
        mock.get(query_url, text='{}')

        eagle_eye = EagleEye(mock_callback)
        eagle_eye.authenticated_query(query_url)

        mock_callback.assert_called_once_with()
        self.assertTrue(mock.called_once)

    @requests_mock.Mocker()
    def test_authenticated_query_raises_callback_failure(self, mock):
        """Test exception on faulty callback"""
        mock_callback = Mock(
            return_value=(FIXTURE_SESSION_AUTH_KEY, None))

        query_url = 'https://test.com'
        mock.get(query_url, text='{}')

        eagle_eye = EagleEye(mock_callback)
        with self.assertRaises(CarsonError):
            eagle_eye.authenticated_query(query_url)

        mock_callback.assert_called_once_with()
        self.assertEqual(0, mock.call_count)
