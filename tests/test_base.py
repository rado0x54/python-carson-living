# -*- coding: utf-8 -*-
"""Base Module for Carson Living tests."""

import unittest

from carson_living import (Carson, CarsonAuth)
from tests.const import (USERNAME, PASSWORD)
from tests.helpers import get_encoded_token


class CarsonUnitTestBase(unittest.TestCase):
    """Carson Living base test class."""

    def setUp(self):
        """Setup unit test and load mock."""
        token, _ = get_encoded_token()

        auth = CarsonAuth(USERNAME, PASSWORD, token)

        self.carson = Carson(auth)

