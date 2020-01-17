import unittest
import jwt
import time
import requests_mock

from carson_living import (CarsonAuth, CarsonAPIError, CarsonTokenError, CarsonAuthenticationError)
from tests.helpers import load_fixture
from tests.const import USERNAME, PASSWORD, TOKEN_PAYLOAD_TEMPLATE

FIXTURE_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.' \
                'eyJ1c2VyX2lkIjo5OTk5LCJ1c2VybmFtZSI6I' \
                'mZiMTIzNDUiLCJleHAiOjIwNjU4OTU1ODgsIm' \
                'VtYWlsIjoiZm9vQGJhci5kZSJ9.4ki8y9q_10' \
                '6tsa89lNM4va0pyxEkvJ60iBLkObtyVLc'


class TestCarsonAuth(unittest.TestCase):
    """Top level Carson Living test class."""

    def test_auth_init(self):
        auth = CarsonAuth(USERNAME, PASSWORD)
        self.assertIsNone(auth.token)
        self.assertIsNone(auth.token_payload)
        self.assertIsNone(auth.token_expiration_date)
        self.assertEqual(auth._username, USERNAME)
        self.assertEqual(auth._password, PASSWORD)
        self.assertFalse(auth.valid_token())

    def test_auth_invalid_token_throws(self):
        with self.assertRaises(CarsonTokenError):
            CarsonAuth(USERNAME, PASSWORD, 'asdkfjajdskf')

        with self.assertRaises(CarsonTokenError):
            CarsonAuth(USERNAME, PASSWORD, '')

    def test_auth_valid_token_init(self):
        token_payload = {'exp': int(time.time() + 60)}
        token_payload.update(TOKEN_PAYLOAD_TEMPLATE)

        token = jwt.encode(token_payload, 'secret', algorithm='HS256')
        auth = CarsonAuth(USERNAME, PASSWORD, token)
        self.assertEqual(auth.token, token)
        self.assertEqual(auth.token_payload, token_payload)
        self.assertEqual(auth.token_expiration_date, token_payload.get('exp'))
        self.assertEqual(auth._username, USERNAME)
        self.assertEqual(auth._password, PASSWORD)
        self.assertTrue(auth.valid_token())

    @requests_mock.Mocker()
    def test_update_token_success(self, mock):
        mock.post('https://api.carson.live/api/v1.4.0/auth/login/',
                  text=load_fixture('carson_login.json'))

        auth = CarsonAuth(USERNAME, PASSWORD)
        auth.update_token()

        self.assertEqual(FIXTURE_TOKEN, auth.token)
        self.assertTrue(mock.called)

    @requests_mock.Mocker()
    def test_update_token_fail(self, mock):
        mock.post('https://api.carson.live/api/v1.4.0/auth/login/',
                  text=load_fixture('carson_auth_failure.json'),
                  status_code=401)

        auth = CarsonAuth(USERNAME, PASSWORD)

        with self.assertRaises(CarsonAuthenticationError):
            auth.update_token()

        self.assertTrue(mock.called)

    def test_expired_token_is_invalid(self):
        token_payload = {'exp': int(time.time() - 60)}
        token_payload.update(TOKEN_PAYLOAD_TEMPLATE)

        token = jwt.encode(token_payload, 'secret', algorithm='HS256')

        auth = CarsonAuth(USERNAME, PASSWORD, token)
        self.assertFalse(auth.valid_token())

    @requests_mock.Mocker()
    def test_successful_query_without_initial_token(self, mock):
        mock.post('https://api.carson.live/api/v1.4.0/auth/login/',
                  text=load_fixture('carson_login.json'))
        query_url = 'https://api.carson.live/api/v1.4.0/me/'
        mock.get(query_url,
                  text=load_fixture('carson_me.json'))

        auth = CarsonAuth(USERNAME, PASSWORD)

        auth.query(query_url)

        # Token unchanged
        self.assertEqual(FIXTURE_TOKEN, auth.token)
        self.assertEqual(2, mock.call_count)
        self.assertEqual('JWT {}'.format(FIXTURE_TOKEN), mock.last_request.headers.get('Authorization'))

    @requests_mock.Mocker()
    def test_successful_query_with_initial_token(self, mock):
        query_url = 'https://api.carson.live/api/v1.4.0/me/'
        mock.get(query_url,
                  text=load_fixture('carson_me.json'))

        token_payload = {'exp': int(time.time() + 60)}
        token_payload.update(TOKEN_PAYLOAD_TEMPLATE)

        token = jwt.encode(token_payload, 'secret', algorithm='HS256')
        auth = CarsonAuth(USERNAME, PASSWORD, token)

        auth.query(query_url)

        # Token unchanged
        self.assertEqual(token, auth.token)
        self.assertEqual(1, mock.call_count)
        self.assertEqual('JWT {}'.format(token), mock.last_request.headers.get('Authorization'))


    @requests_mock.Mocker()
    def test_recursive_retry(self, mock):
        mock.post('https://api.carson.live/api/v1.4.0/auth/login/',
                  text=load_fixture('carson_login.json'))
        query_url = 'https://api.carson.live/api/v1.4.0/me/'
        mock.get(query_url,
                  text=load_fixture('carson_auth_failure.json'),
                 status_code=401)

        auth = CarsonAuth(USERNAME, PASSWORD)

        with self.assertRaises(CarsonAPIError):
            auth.query(query_url, retry_auth=2)

        # Token unchanged
        self.assertEqual(FIXTURE_TOKEN, auth.token)
        self.assertEqual(6, mock.call_count)
        self.assertEqual('JWT {}'.format(FIXTURE_TOKEN), mock.last_request.headers.get('Authorization'))



