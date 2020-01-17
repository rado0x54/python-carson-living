# -*- coding: utf-8 -*-
"""Base Module for Carson Living tests."""

import unittest

from carson_living import (Carson, CarsonAuth)
from tests.const import (USERNAME, PASSWORD)


class CarsonUnitTestBase(unittest.TestCase):
    """Carson Living base test class."""

    def setUp(self):
        """Setup unit test and load mock."""

        auth = CarsonAuth(USERNAME, PASSWORD)

        self.carson = Carson(auth)

        # Until a query is made, login should not be executed.
        self.assertTrue(hasattr(self.carson, "get_doors"))
