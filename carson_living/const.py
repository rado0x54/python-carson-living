# coding: utf-8
"""Constants."""
import os
from uuid import uuid4 as uuid

#
# Sample Carson Headers
#

# GET /api/v1.4.0/me/ HTTP/1.1
# Host: api.carson.live
# Accept: */*
# Connection: close
# X-Device-Type: ios
# Accept-Encoding: gzip, deflate
# User-Agent: Carson/1.0.171 (live.carson.app; build:245; iOS 13.1.0) Alamofire/1.0.171
# X-App-Version: 1.0.171(245)


CARSON_RESPONSE = {
    'CODE': 'code',
    'STATUS': 'status',
    'DATA': 'data',
    'MSG': 'msg'
}

"""Pretend to be Carson iOS Installation v1.0.171"""
BASE_HEADERS = {
    # 'Content-Type': 'application/json',
    'User-Agent': 'Carson/1.0.171 (live.carson.app; build:245; iOS 13.1.0) Alamofire/1.0.171',
    'X-App-Version': '1.0.171(245)',
    'X-Device-Type': 'ios',
    'Accept-Encoding': 'gzip, deflate'
}

# number of attempts to refresh token
RETRY_TOKEN = 3

# default suffix for session cache file
CACHE_ATTRS = {'account': None, 'alerts': None, 'token': None}

try:
    CACHE_FILE = os.path.join(os.getenv("HOME"),
                              '.carson_living-session.cache')
except (AttributeError, TypeError):
    CACHE_FILE = os.path.join('.', '.carson_living-session.cache')


# code when item was not found
NOT_FOUND = -1

# API endpoints
API_VERSION = 'v1.4.0'
API_URI = 'https://api.carson.live/api/' + API_VERSION

AUTH_ENDPOINT = '/auth/login/'
ME_ENDPOINT = '/me/' #GET


# ---------------------------- RING STUFF
CHIMES_ENDPOINT = '/clients_api/chimes/{0}'
DEVICES_ENDPOINT = '/clients_api/ring_devices'
DINGS_ENDPOINT = '/clients_api/dings/active'
DOORBELLS_ENDPOINT = '/clients_api/doorbots/{0}'
PERSIST_TOKEN_ENDPOINT = '/clients_api/device'

HEALTH_DOORBELL_ENDPOINT = DOORBELLS_ENDPOINT + '/health'
HEALTH_CHIMES_ENDPOINT = CHIMES_ENDPOINT + '/health'
LIGHTS_ENDPOINT = DOORBELLS_ENDPOINT + '/floodlight_light_{1}'
LINKED_CHIMES_ENDPOINT = CHIMES_ENDPOINT + '/linked_doorbots'
LIVE_STREAMING_ENDPOINT = DOORBELLS_ENDPOINT + '/vod'
NEW_SESSION_ENDPOINT = '/clients_api/session'
RINGTONES_ENDPOINT = '/ringtones'
SIREN_ENDPOINT = DOORBELLS_ENDPOINT + '/siren_{1}'
SNAPSHOT_ENDPOINT = "/clients_api/snapshots/image/{0}"
SNAPSHOT_TIMESTAMP_ENDPOINT = "/clients_api/snapshots/timestamps"
TESTSOUND_CHIME_ENDPOINT = CHIMES_ENDPOINT + '/play_sound'
URL_DOORBELL_HISTORY = DOORBELLS_ENDPOINT + '/history'
URL_RECORDING = '/clients_api/dings/{0}/recording'

# chime test sound kinds
KIND_DING = 'ding'
KIND_MOTION = 'motion'
CHIME_TEST_SOUND_KINDS = (KIND_DING, KIND_MOTION)

# default values
CHIME_VOL_MIN = 0
CHIME_VOL_MAX = 10

DOORBELL_VOL_MIN = 0
DOORBELL_VOL_MAX = 11

DOORBELL_EXISTING_TYPE = {
    0: 'Mechanical',
    1: 'Digital',
    2: 'Not Present'}

SIREN_DURATION_MIN = 0
SIREN_DURATION_MAX = 120

# device model kinds
CHIME_KINDS = ['chime']
CHIME_PRO_KINDS = ['chime_pro']

DOORBELL_KINDS = ['doorbot', 'doorbell', 'doorbell_v3']
DOORBELL_2_KINDS = ['doorbell_v4', 'doorbell_v5']
DOORBELL_PRO_KINDS = ['lpd_v1', 'lpd_v2']
DOORBELL_ELITE_KINDS = ['jbox_v1']

FLOODLIGHT_CAM_KINDS = ['hp_cam_v1', 'floodlight_v2']
SPOTLIGHT_CAM_BATTERY_KINDS = ['stickup_cam_v4']
SPOTLIGHT_CAM_WIRED_KINDS = ['hp_cam_v2']
STICKUP_CAM_KINDS = ['stickup_cam', 'stickup_cam_v3']
STICKUP_CAM_BATTERY_KINDS = ['cocoa_camera', 'stickup_cam_lunar']
STICKUP_CAM_WIRED_KINDS = ['stickup_cam_elite']

# error strings
MSG_BOOLEAN_REQUIRED = "Boolean value is required."
MSG_EXISTING_TYPE = "Integer value where {0}.".format(DOORBELL_EXISTING_TYPE)
MSG_GENERIC_FAIL = 'Sorry.. Something went wrong...'
FILE_EXISTS = 'The file {0} already exists.'
MSG_VOL_OUTBOUND = 'Must be within the {0}-{1}.'
MSG_ALLOWED_VALUES = 'Only the following values are allowed: {0}.'

# structure acquired from reverse engineering to create auth token
OAUTH_DATA = {
    "client_id": "ring_official_android",
    "grant_type": "password",
    "scope": "client",
    "username": None,
    "password": None,
}

POST_DATA = {
    'api_version': API_VERSION,
    'device[hardware_id]': str(uuid()),
    'device[os]': 'android',
    'device[app_brand]': 'ring',
    'device[metadata][device_model]': 'KVM',
    'device[metadata][device_name]': 'Python',
    'device[metadata][resolution]': '600x800',
    'device[metadata][app_version]': '1.3.806',
    'device[metadata][app_instalation_date]': '',
    'device[metadata][manufacturer]': 'Qemu',
    'device[metadata][device_type]': 'desktop',
    'device[metadata][architecture]': 'desktop',
    'device[metadata][language]': 'en'}

PERSIST_TOKEN_DATA = {
    'api_version': API_VERSION,
    'device[metadata][device_model]': 'KVM',
    'device[metadata][device_name]': 'Python',
    'device[metadata][resolution]': '600x800',
    'device[metadata][app_version]': '1.3.806',
    'device[metadata][app_instalation_date]': '',
    'device[metadata][manufacturer]': 'Qemu',
    'device[metadata][device_type]': 'desktop',
    'device[metadata][architecture]': 'x86',
    'device[metadata][language]': 'en'}
