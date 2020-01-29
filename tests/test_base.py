# -*- coding: utf-8 -*-
"""Base Module for Carson Living tests."""

import unittest
import json
import requests_mock

from carson_living import (Carson)
from carson_living.const import (C_API_URI,
                                 C_ME_ENDPOINT,
                                 C_EEN_SESSION_ENDPOINT)

from tests.const import (USERNAME, PASSWORD)
from tests.helpers import (load_fixture,
                           get_encoded_token,
                           setup_ee_device_list_mock)


class CarsonUnitTestBase(unittest.TestCase):
    """Carson Living base test class."""

    def setUp(self):
        """Setup unit test and load mock."""
        with requests_mock.Mocker() as mock:
            # Setup URL Mocking
            self.token, _ = get_encoded_token()

            self._init_default_mocks(mock, 'carson_me.json')

            self.carson = Carson(USERNAME, PASSWORD, self.token)
            self.first_building = self.carson.first_building
            self.user = self.carson.first_building
            self.first_camera = next(iter(self.first_building.cameras))
            self.first_door = next(iter(self.first_building.doors))

    def _init_default_mocks(self, mock, c_mock_me_filename):
        c_mock_me_txt = load_fixture('carson.live', c_mock_me_filename)
        self.c_mock_me = json.loads(c_mock_me_txt).get('data')
        self.c_mock_first_property = self.c_mock_me['properties'][0]
        self.c_mock_first_door = self.c_mock_first_property['doors'][0]
        self.c_mock_first_camera = self.c_mock_first_property['cameras'][0]

        # ME Mock
        mock.get(C_API_URI + C_ME_ENDPOINT,
                 text=c_mock_me_txt)

        # Eagle Eye Session Mock
        c_mock_esession_txt = load_fixture(
            'carson.live', 'carson_eagleeye_session.json')
        self.c_mock_esession = json.loads(c_mock_esession_txt).get('data')

        for b_id in [p['id'] for p in self.c_mock_me.get('properties')]:
            mock.get(
                C_API_URI + C_EEN_SESSION_ENDPOINT.format(b_id),
                text=c_mock_esession_txt
            )

        # Device list Mock
        self.e_mock_device_list = setup_ee_device_list_mock(
            mock, self.c_mock_esession['activeBrandSubdomain'])
