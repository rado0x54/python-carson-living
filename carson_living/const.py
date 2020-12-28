# coding: utf-8
"""Carson Constants."""

CARSON_RESPONSE = {
    'CODE': 'code',
    'STATUS': 'status',
    'DATA': 'data',
    'MSG': 'msg'
}

BASE_HEADERS = {
    'User-Agent': 'okhttp/4.9.0',
    'X-App-Version': '2.1.5',
    'X-Device-Type': 'android'
}

# number of attempts to refresh token
RETRY_TOKEN = 1

# Carson API endpoints
# Beware URLs end in '/', otherwise it returns a
# HTTP/1.1 301 Moved Permanently to the correct version.
C_API_VERSION = 'v1.4.4'
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
