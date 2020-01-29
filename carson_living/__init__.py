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

from carson_living.const import (EEN_ASSET_REF_ASSET,
                                 EEN_ASSET_REF_PREV,
                                 EEN_ASSET_REF_NEXT,
                                 EEN_ASSET_REF_AFTER,
                                 EEN_ASSET_CLS_ALL,
                                 EEN_ASSET_CLS_PRE,
                                 EEN_ASSET_CLS_THUMB,
                                 EEN_VIDEO_FORMAT_FLV,
                                 EEN_VIDEO_FORMAT_MP4)


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
           'CarsonUser',
           'EEN_ASSET_REF_ASSET',
           'EEN_ASSET_REF_PREV',
           'EEN_ASSET_REF_NEXT',
           'EEN_ASSET_REF_AFTER',
           'EEN_ASSET_CLS_ALL',
           'EEN_ASSET_CLS_PRE',
           'EEN_ASSET_CLS_THUMB',
           'EEN_VIDEO_FORMAT_FLV',
           'EEN_VIDEO_FORMAT_MP4']
