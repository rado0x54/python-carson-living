# -*- coding: utf-8 -*-
"""Carson Living API Module."""

import logging

_LOGGER = logging.getLogger(__name__)


# pylint: disable=useless-object-inheritance
class Carson(object):
    """A Python Abstraction object to the Carson Living API.

        Attributes:
            carson_auth: The Carson Authentication class to use
    """

    def __init__(self, carson_auth):
        self.carson_auth = carson_auth

    def get_doors(self):
        """Return door objects"""

    def get_cameras(self):
        """Return camera objects"""
