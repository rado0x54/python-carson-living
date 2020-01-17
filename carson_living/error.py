# -*- coding: utf-8 -*-
"""Carson Living custom exceptions."""


class CarsonError(Exception):
    """Carson Living base error"""


class CarsonTokenError(CarsonError):
    """Carson Living token error"""


class CarsonCommunicationError(CarsonError):
    """Carson Living communication error"""


class CarsonAPIError(CarsonError):
    """Carson Living client-side API error"""


class CarsonAuthenticationError(CarsonAPIError):
    """Carson Living authentication error"""
