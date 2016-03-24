import argparse
import getpass

import config
import auth
import server

def add_user(args):
    print("Set password for user {}".format(args.user_name))
    password = getpass.getpass()
    confirm = getpass.getpass(prompt='Confirm password: ')

    if password != confirm:
        print('Error: passwords do not match')
    else:
        auth.init()
        auth.add_user(args.user_name, password)
        print('User database updated')

def remove_user(args):
    print("Removing user {}".format(args.user_name))
    auth.init()
    auth.remove_user(args.user_name)

def clear_users(args):
    print('Are you sure you want to delete all users?')
    answer = input('(yes/no): ')

    if answer.lower() == 'yes':
        auth.init()
        auth.clear()
        print('Deleted all users')
    else:
        print('Cancelled')


if __name__ == '__main__':
    parent_parser = argparse.ArgumentParser()

    subparsers = parent_parser.add_subparsers(
        dest='subparser_name',
        help='Commands'
    )

    users_parser = subparsers.add_parser('users')

    users_subparsers = users_parser.add_subparsers(
        dest='users_command',
        help='Sub-commands'
    )

    # USERS ADD
    add_parser = users_subparsers.add_parser('add')
    add_parser.add_argument('user_name')
    add_parser.set_defaults(func=add_user)

    # USERS REMOVE
    remove_parser = users_subparsers.add_parser('remove')
    remove_parser.add_argument('user_name')
    remove_parser.set_defaults(func=remove_user)

    # USERS REMOVE
    clear_parser = users_subparsers.add_parser('clearall')
    clear_parser.set_defaults(func=clear_users)

    args = parent_parser.parse_args()
    if hasattr(args, 'func'):
        config.init(server.persistent_path)
        args.func(args)
    else:
        parent_parser.print_help()
