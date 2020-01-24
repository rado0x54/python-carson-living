# -*- coding: utf-8 -*-
"""Python Module to use with Carson Living

Contains classes to authenticate against Carson Living and query various
entities and expose their functionality.
"""

from carson_living.auth import CarsonAuth
from carson_living.carson import Carson
from carson_living.error import (CarsonAuthenticationError,
                                 CarsonAPIError,
                                 CarsonError,
                                 CarsonCommunicationError,
                                 CarsonTokenError)

from carson_living.eagleeye import EagleEye
from carson_living.eagleeye_entities import EagleEyeCamera
from carson_living.carson_entities import (CarsonDoor,
                                           CarsonBuilding,
                                           CarsonUser)


__all__ = ['CarsonAuth',
           'Carson',
           'CarsonAuthenticationError',
           'CarsonAPIError',
           'CarsonError',
           'CarsonCommunicationError',
           'CarsonTokenError',
           'EagleEye',
           'EagleEyeCamera',
           'CarsonDoor',
           'CarsonBuilding',
           'CarsonUser']
