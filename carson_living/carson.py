# -*- coding: utf-8 -*-
"""Python Carson Living API Class."""

import logging

_LOGGER = logging.getLogger(__name__)


class Carson(object):
    """A Python Abstraction object to the Carson Living API."""

    def __init__(self, carson_auth):
        self.carson_auth = carson_auth


    def update(self):
        """Update Devices"""

