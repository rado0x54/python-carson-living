#!/usr/bin/env python
"""Command line tool for interacting with the Carson Living API"""

import getpass
import argparse
from carson_living import Carson, CarsonAuth


def _header():
    _bar()
    print("Carson CLI")


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
    auth = CarsonAuth(args.username, args.password, args.token)
    Carson(auth)

    res = auth.authenticated_query('https://api.carson.live/api/v1.4.0/me/')
    print(res)

    _bar()


if __name__ == '__main__':
    main()
