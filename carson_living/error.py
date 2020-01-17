# -*- coding: utf-8 -*-
"""Python Carson Living Custom Exceptions"""


class CarsonError(Exception):
    pass


class CarsonTokenError(Exception):
    pass


class CarsonCommunicationError(CarsonError):
    pass


class CarsonAPIError(CarsonError):
    pass


class CarsonAuthenticationError(CarsonAPIError):
    pass



