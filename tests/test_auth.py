# -*- coding: utf-8 -*-
"""Authentication Module for Carson Living tests."""

import unittest
import requests_mock

# 2.7 support fallback
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from carson_living import (CarsonAuth,
                           CarsonAPIError,
                           CarsonTokenError,
                           CarsonCommunicationError,
                           CarsonAuthenticationError)
from tests.helpers import load_fixture, get_encoded_token
from tests.const import (USERNAME,
                         PASSWORD)

FIXTURE_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.' \
                'eyJ1c2VyX2lkIjo5OTk5LCJ1c2VybmFtZSI6I' \
                'mZiMTIzNDUiLCJleHAiOjIwNjU4OTU1ODgsIm' \
                'VtYWlsIjoiZm9vQGJhci5kZSJ9.4ki8y9q_10' \
                '6tsa89lNM4va0pyxEkvJ60iBLkObtyVLc'


class TestCarsonAuth(unittest.TestCase):
    """Carson Living authentication test class."""

    def test_auth_init(self):
        """Test default class initialization"""
        auth = CarsonAuth(USERNAME, PASSWORD)

        self.assertEqual(auth.username, USERNAME)
        self.assertIsNone(auth.token)
        self.assertIsNone(auth.token_payload)
        self.assertIsNone(auth.token_expiration_date)
        self.assertFalse(auth.valid_token())

    def test_auth_invalid_token_throws(self):
        """Test invalid class initialization"""
        with self.assertRaises(CarsonTokenError):
            CarsonAuth(USERNAME, PASSWORD, 'this_is_not_a_valid_jwt')

        with self.assertRaises(CarsonTokenError):
            CarsonAuth(USERNAME, PASSWORD, '')

    def test_auth_valid_token_init(self):
        """Test default class initialization with token"""
        token, token_payload = get_encoded_token()

        mock_token_update_cb = Mock()

        auth = CarsonAuth(USERNAME, PASSWORD, token, mock_token_update_cb)

        self.assertEqual(auth.username, USERNAME)
        self.assertEqual(auth.token, token)
        self.assertEqual(auth.token_payload, token_payload)
        self.assertEqual(auth.token_expiration_date, token_payload.get('exp'))
        self.assertTrue(auth.valid_token())

        # make sure that token update cb is not executed with an initial token.
        mock_token_update_cb.assert_not_called()

    @requests_mock.Mocker()
    def test_update_token_success(self, mock):
        """Test token update"""
        mock.post('https://api.carson.live/api/v1.4.4/auth/login/',
                  text=load_fixture('carson.live', 'carson_login.json'))

        mock_token_update_cb = Mock()

        auth = CarsonAuth(USERNAME, PASSWORD,
                          token_update_cb=mock_token_update_cb)
        token = auth.update_token()

        self.assertEqual(auth.username, USERNAME)
        self.assertEqual(FIXTURE_TOKEN, token)
        self.assertEqual(FIXTURE_TOKEN, auth.token)
        self.assertTrue(mock.called)
        self.assertEqual(USERNAME,
                         mock.last_request.json().get('username'))
        self.assertEqual(PASSWORD,
                         mock.last_request.json().get('password'))
        mock_token_update_cb.assert_called_once_with(FIXTURE_TOKEN)

    @requests_mock.Mocker()
    def test_update_token_fail(self, mock):
        """Test authentication failure in token update"""
        mock.post('https://api.carson.live/api/v1.4.4/auth/login/',
                  text=load_fixture('carson.live', 'carson_auth_failure.json'),
                  status_code=401)

        auth = CarsonAuth(USERNAME, PASSWORD)

        with self.assertRaises(CarsonAuthenticationError):
            auth.update_token()

        self.assertTrue(mock.called)

    def test_expired_token_is_invalid(self):
        """Test expired token validation"""
        token, _ = get_encoded_token(-60)

        auth = CarsonAuth(USERNAME, PASSWORD, token)
        self.assertFalse(auth.valid_token())

    @requests_mock.Mocker()
    def test_successful_query_without_initial_token(self, mock):
        """Test automatic authentication on query without initial token"""
        mock.post('https://api.carson.live/api/v1.4.4/auth/login/',
                  text=load_fixture('carson.live', 'carson_login.json'))
        query_url = 'https://api.carson.live/api/v1.4.4/me/'
        mock.get(query_url,
                 text=load_fixture('carson.live', 'carson_me.json'))

        auth = CarsonAuth(USERNAME, PASSWORD)

        auth.authenticated_query(query_url)

        # Token unchanged
        self.assertEqual(FIXTURE_TOKEN, auth.token)
        self.assertEqual(2, mock.call_count)
        self.assertEqual('JWT {}'.format(FIXTURE_TOKEN),
                         mock.last_request.headers.get('Authorization'))

    @requests_mock.Mocker()
    def test_successful_query_with_initial_token(self, mock):
        """Test query with initial valid token"""
        query_url = 'https://api.carson.live/api/v1.4.4/me/'
        mock.get(query_url,
                 text=load_fixture('carson.live', 'carson_me.json'))

        token, _ = get_encoded_token()

        auth = CarsonAuth(USERNAME, PASSWORD, token)

        auth.authenticated_query(query_url)

        # Token unchanged
        self.assertEqual(token, auth.token)
        self.assertEqual(1, mock.call_count)
        self.assertEqual('JWT {}'.format(token),
                         mock.last_request.headers.get('Authorization'))

    @requests_mock.Mocker()
    def test_recursive_retry(self, mock):
        """"Test recursive query retry on Authentication Failure"""
        mock.post('https://api.carson.live/api/v1.4.4/auth/login/',
                  text=load_fixture('carson.live', 'carson_login.json'))
        query_url = 'https://api.carson.live/api/v1.4.4/me/'
        mock.get(query_url,
                 text=load_fixture('carson.live', 'carson_auth_failure.json'),
                 status_code=401)

        auth = CarsonAuth(USERNAME, PASSWORD)

        with self.assertRaises(CarsonAPIError):
            auth.authenticated_query(query_url, retry_auth=2)

        # Token unchanged
        self.assertEqual(FIXTURE_TOKEN, auth.token)
        self.assertEqual(6, mock.call_count)
        self.assertEqual('JWT {}'.format(FIXTURE_TOKEN),
                         mock.last_request.headers.get('Authorization'))

    @requests_mock.Mocker()
    def test_raise_communication_error_on_empty(self, mock):
        """Test failure on empty response"""
        query_url = 'https://api.carson.live/api/v1.4.4/me/'
        mock.get(query_url,
                 status_code=500)

        token, _ = get_encoded_token()

        auth = CarsonAuth(USERNAME, PASSWORD, token)

        with self.assertRaises(CarsonCommunicationError):
            auth.authenticated_query(query_url)

        self.assertTrue(mock.called)

    @requests_mock.Mocker()
    def test_raise_communication_error_wrong_json(self, mock):
        """Test failure on response with missing keys"""
        query_url = 'https://api.carson.live/api/v1.4.4/me/'
        mock.get(query_url,
                 text=load_fixture('carson.live', 'carson_missing_keys.json'))

        token, _ = get_encoded_token()

        auth = CarsonAuth(USERNAME, PASSWORD, token)

        with self.assertRaises(CarsonCommunicationError):
            auth.authenticated_query(query_url)

        self.assertTrue(mock.called)
