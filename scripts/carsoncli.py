#!/usr/bin/env python
"""Command line tool for interacting with the Carson Living API"""

import getpass
import argparse
import logging

from datetime import timedelta

from carson_living import Carson


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(message)s')


def _header():
    _bar()
    print("Carson CLI")
    _bar()


def _bar():
    print('---------------------------------')


def get_username():
    """read username from STDIN"""
    try:
        username = raw_input("Username: ")
    except NameError:
        username = input("Username: ")
    return username


# def _format_filename(event):
#     if not isinstance(event, dict):
#         return
#
#     if event['answered']:
#         answered_status = 'answered'
#     else:
#         answered_status = 'not_answered'
#
#     filename = "{}_{}_{}_{}".format(event['created_at'],
#                                     event['kind'],
#                                     answered_status,
#                                     event['id'])
#
#     filename = filename.replace(' ', '_').replace(':', '.')+'.mp4'
#     return filename


def main():
    """main function"""

    parser = argparse.ArgumentParser(
        description='Carson Living',
        epilog='https://github.com/rado0x54/python-carson-living',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-u',
                        '--username',
                        dest='username',
                        type=str,
                        help='username for Carson Living account')

    parser.add_argument('-p',
                        '--password',
                        type=str,
                        dest='password',
                        help='username for Carson Living account')

    parser.add_argument('-t',
                        '--token',
                        type=str,
                        dest='token',
                        help='existing token for the Carson Living account')

    args = parser.parse_args()
    _header()

    if not args.username:
        args.username = get_username()

    if not args.password:
        args.password = getpass.getpass("Password: ")

    # connect to Carson Living account
    carson = Carson(args.username, args.password, args.token)
    # print(carson.token)

    # print some info
    _bar()
    print('Carson user info')
    print(carson.user)
    _bar()

    for building in carson.buildings:
        print('Carson building information')
        print(building)
        _bar()

        for camera in building.cameras:
            print('Eagle Eye camera information')
            print(camera)
            _bar()

        for door in building.doors:
            print('Carson door information')
            print(door)
            _bar()

        # download all images
        for camera in building.cameras:
            with open('image_{}.jpeg'.format(camera.entity_id), 'wb') as file:
                camera.get_image(file)

        for camera in building.cameras:
            with open('video_{}.flv'.format(camera.entity_id), 'wb') as file:
                camera.get_live_video(file, timedelta(seconds=2))

    # Open all Unit Doors of Main Building
    # for door in carson.first_building.doors:
    #     if door.is_unit_door:
    #         print('Opening Unit Door {}'.format(door.name))
    #         door.open()

    _bar()


if __name__ == '__main__':
    main()
