# -*- coding: utf-8 -*-
"""Python Carson Living wrapper."""
import logging

_LOGGER = logging.getLogger(__name__)


class Carson:
    """A Python Abstraction object to Carson Living."""

    def __init__(self, username, password, debug=False, persist_token=False):
        """Initialize the Carson Living object."""
        self.is_connected = None
        self.token = None
        self.params = None
        self._persist_token = persist_token

        self.debug = debug
        self.username = username
        self.password = password

    @property
    def token(self):
        """Dummy Implementation"""
        return self.token

    @property
    def params(self):
        """Dummy Implementation"""
        return self.params
