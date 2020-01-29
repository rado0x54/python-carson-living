# -*- coding: utf-8 -*-
"""Helper Module for Carson Living tests."""
import os
import time
import json
import jwt

from carson_living import (EEN_ASSET_REF_PREV,
                           EEN_VIDEO_FORMAT_FLV)

from carson_living.const import (EEN_API_URI,
                                 EEN_DEVICE_ENDPOINT,
                                 EEN_DEVICE_LIST_ENDPOINT,
                                 EEN_GET_IMAGE_ENDPOINT,
                                 EEN_GET_VIDEO_ENDPOINT)

from tests.const import TOKEN_PAYLOAD_TEMPLATE


def load_fixture(folder, filename, mode='r'):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__),
                        'fixtures', folder, filename)
    with open(path, mode) as fdp:
        return fdp.read()


def get_encoded_token(expiration_from_now_s=600):
    """Generate a standard Carson Living Token with variable expiration

    Args:
        expiration_from_now_s: delta in s to the current_time

    Returns:
        (tuple): tuple containing:

            token(str): encoded token
            token_payload(dict): decoded token payload
    """
    token_payload = {'exp': int(time.time() + expiration_from_now_s)}
    token_payload.update(TOKEN_PAYLOAD_TEMPLATE)

    token = jwt.encode(token_payload, 'secret', algorithm='HS256')

    return token, token_payload


def setup_ee_camera_mock(mock, active_brand_subdomain,
                         filename='device_camera.json'):
    """Setup a EE Device endpoint

    Args:
        mock: requests_mock mock
        active_brand_subdomain: subdomain to replace in url
        filename: optional reply payload filename

    Returns: filename payload as json

    """
    # Camera ID Mocks
    e_mock_camera_txt = load_fixture(
        'eagleeyenetworks.com', filename)
    e_mock_camera = json.loads(e_mock_camera_txt)
    mock.get(
        EEN_API_URI.format(
            active_brand_subdomain)
        + EEN_DEVICE_ENDPOINT,
        text=e_mock_camera_txt
    )

    return e_mock_camera


def setup_ee_device_list_mock(mock, active_brand_subdomain,
                              filename='device_list.json'):
    """Setup a EE Device list endpoint

    Args:
        mock: requests_mock mock
        active_brand_subdomain: subdomain to replace in url
        filename: optional reply payload filename

    Returns: filename payload as json

    """
    e_mock_list_txt = load_fixture(
        'eagleeyenetworks.com', filename)
    e_mock_list = json.loads(e_mock_list_txt)
    mock.get(
        EEN_API_URI.format(
            active_brand_subdomain)
        + EEN_DEVICE_LIST_ENDPOINT,
        text=e_mock_list_txt
    )

    return e_mock_list


def setup_ee_image_mock(mock, active_brand_subdomain,
                        filename='camera_image.jpeg',
                        asset_ref=EEN_ASSET_REF_PREV):
    """Setup a EE Device endpoint

    Args:
        mock: requests_mock mock
        active_brand_subdomain: subdomain to replace in url
        filename: binary image file to load
        asset_ref: asset reff string in url

    Returns: filename payload as binary

    """
    binary_image = load_fixture(
        'eagleeyenetworks.com', filename, 'rb')
    mock.get(
        EEN_API_URI.format(
            active_brand_subdomain)
        + EEN_GET_IMAGE_ENDPOINT.format(asset_ref),
        content=binary_image
    )
    return binary_image


def setup_ee_video_mock(mock, active_brand_subdomain,
                        video_format=EEN_VIDEO_FORMAT_FLV,
                        filename='camera_video.flv'):
    """Setup a EE Device endpoint

    Args:
        mock: requests_mock mock
        active_brand_subdomain: subdomain to replace in url
        video_format: flv or mp4
        filename: binary video file to load

    Returns: filename payload as binary

    """
    binary_video = load_fixture(
        'eagleeyenetworks.com', filename, 'rb')
    mock.get(
        EEN_API_URI.format(
            active_brand_subdomain)
        + EEN_GET_VIDEO_ENDPOINT.format(
            video_format
        ),
        content=binary_video
    )
    return binary_video
