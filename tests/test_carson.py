# -*- coding: utf-8 -*-
"""Carson API Module for Carson Living tests."""

import requests_mock
import json

from tests.test_base import CarsonUnitTestBase
from tests.helpers import load_fixture


class TestCarson(CarsonUnitTestBase):
    """Carson Living API test class."""

    @requests_mock.Mocker()
    def test_get_eagle_eye_session(self, mock):
        building_id = 1000
        query_url = 'https://api.carson.live/api/v1.4.0/properties/buildings/{}/eagleeye/session/'.format(building_id)
        response = load_fixture('carson_eagleeye_session.json')
        mock.get(query_url,
                 text=response)

        eagle_eye_session = self.carson.get_eagleeye_session(building_id)

        self.assertTrue(mock.called)
        self.assertDictEqual(eagle_eye_session, json.loads(response).get('data'))


