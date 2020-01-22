# -*- coding: utf-8 -*-
"""Base Module for Carson Living tests."""

import unittest
import json
import requests_mock

from carson_living import (Carson)
from tests.const import (USERNAME, PASSWORD)
from tests.helpers import load_fixture, get_encoded_token


class CarsonUnitTestBase(unittest.TestCase):
    """Carson Living base test class."""

    @requests_mock.Mocker()
    def setUp(self, mock):
        # pylint: disable=arguments-differ
        """Setup unit test and load mock."""

        self.token, _ = get_encoded_token()

        query_url = 'https://api.carson.live/api/v1.4.1/me/'
        mock_response = load_fixture('carson.live', 'carson_me.json')
        mock.get(query_url, text=mock_response)
        self.init_me_mock = mock
        self.mock_carson_me = json.loads(mock_response).get('data')

        self.carson = Carson(USERNAME, PASSWORD, self.token)

        self.first_building = self.carson.first_building
        self.user = self.carson.first_building
        self.first_camera = next(iter(self.first_building.cameras))
        self.first_door = next(iter(self.first_building.doors))
