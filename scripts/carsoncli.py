#!/usr/bin/env python

import getpass
import argparse
from carson_living import Carson, CarsonAuth


def _header():
    _bar()
    print("Carson CLI")


def _bar():
    print('---------------------------------')


def get_username():
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
                        help='existing token to reuse for the Carson Living Account')

    args = parser.parse_args()
    _header()

    if not args.username:
        args.username = get_username()

    if not args.password:
        args.password = getpass.getpass("Password: ")

    # connect to Carson Living account
    auth = CarsonAuth(args.username, args.password, args.token)
    carson = Carson(auth)

    res = auth.query('https://api.carson.live/api/v1.4.0/me/')
    print(res)


    _bar()


if __name__ == '__main__':
    main()
