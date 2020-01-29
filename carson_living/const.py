# coding: utf-8
"""Carson Constants."""

CARSON_RESPONSE = {
    'CODE': 'code',
    'STATUS': 'status',
    'DATA': 'data',
    'MSG': 'msg'
}

"""Pretend to be Carson iOS Installation v1.0.171"""
BASE_HEADERS = {
    'User-Agent': 'Carson/1.0.200 (live.carson.app; build:315; iOS 13.3.0) '
                  'Alamofire/1.0.200',
    'X-App-Version': '1.0.200(315)',
    'X-Device-Type': 'ios'
}

# number of attempts to refresh token
# RETRY_TOKEN = 3

# default suffix for session cache file
# CACHE_ATTRS = {'account': None, 'alerts': None, 'token': None}
#
# try:
#     CACHE_FILE = os.path.join(os.getenv("HOME"),
#                               '.carson_living-session.cache')
# except (AttributeError, TypeError):
#     CACHE_FILE = os.path.join('.', '.carson_living-session.cache')


# code when item was not found
# NOT_FOUND = -1

# Carson API endpoints
# Beware URLs end in '/', otherwise it returns a
# HTTP/1.1 301 Moved Permanently to the correct version.
C_API_VERSION = 'v1.4.1'
C_API_URI = 'https://api.carson.live/api/' + C_API_VERSION

C_AUTH_ENDPOINT = '/auth/login/'
C_ME_ENDPOINT = '/me/'

C_DOOR_OPEN_ENDPOINT = '/doors/{}/open/'
C_EEN_SESSION_ENDPOINT = '/properties/buildings/{}/eagleeye/session/'

# Eagle Eye API endpoints
# Beware URLs DO NOT end in '/', otherwise it returns a 500
EEN_API_URI = 'https://{}.eagleeyenetworks.com'
EEN_DEVICE_ENDPOINT = '/g/device'
EEN_DEVICE_LIST_ENDPOINT = '/g/device/list'
EEN_GET_IMAGE_ENDPOINT = '/asset/{}/image.jpeg'
EEN_GET_VIDEO_ENDPOINT = '/asset/play/video.{}'
EEN_IS_AUTH_ENDPOINT = '/g/aaa/isauth'

# Eagle Eye Network Interface options
EEN_ASSET_REF_ASSET = 'asset'
EEN_ASSET_REF_PREV = 'prev'
EEN_ASSET_REF_NEXT = 'next'
EEN_ASSET_REF_AFTER = 'after'

EEN_ASSET_CLS_ALL = 'all'
EEN_ASSET_CLS_PRE = 'pre'
EEN_ASSET_CLS_THUMB = 'thumb'

EEN_VIDEO_FORMAT_FLV = 'flv'
EEN_VIDEO_FORMAT_MP4 = 'mp4'
