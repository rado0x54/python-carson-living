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
    'User-Agent': 'Carson/1.0.171 (live.carson.app; build:245; iOS 13.1.0) '
                  'Alamofire/1.0.171',
    'X-App-Version': '1.0.171(245)',
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

# API endpoints
API_VERSION = 'v1.4.0'
API_URI = 'https://api.carson.live/api/' + API_VERSION

AUTH_ENDPOINT = '/auth/login/'
ME_ENDPOINT = '/me/'

EAGLEEYE_SESSION_ENDPOINT = '/properties/buildings/{}/eagleeye/session/'
