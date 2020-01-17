# -*- coding:utf-8 -*-
"""Define basic data for unittests."""
import os
import unittest
import requests_mock
from tests.helpers import load_fixture
from carson_living import Carson, CarsonAuth
from tests.const import (USERNAME, PASSWORD)


class CarsonUnitTestBase(unittest.TestCase):
    """Top level Carson Living test class."""

    @requests_mock.Mocker()
    def setUp(self, mock):
        """Setup unit test and load mock."""

        mock.post('https://api.carson.live/api/v1.4.0/auth/login/',
                  text=load_fixture('carson_login.json'))

        auth = CarsonAuth(USERNAME, PASSWORD)

        self.carson = Carson(auth)

        # Until a query is made, login should not be executed.
        self.assertFalse(mock.called)
        self.assertTrue(hasattr(self.carson, "update"))


