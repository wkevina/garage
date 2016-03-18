import hashlib
import uuid
import os

from tornado.options import define, options

HASH_ROUNDS = 1000

define('admin_username', default=None, type=str)
define('admin_password', default=None, type=str)

def install_admin():
    if options.admin_username and options.admin_password:
        add_user(options.admin_username, options.admin_password)

options.add_parse_callback(install_admin)

def hash_password(clear_password, salt):
        """Generates a secure hash of password"""
        return hashlib.pbkdf2_hmac('sha256',
                                   clear_password.encode(),
                                   salt,
                                   HASH_ROUNDS)

def is_equal(a, b):
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0

def check_password(clear_password, hashed_password, salt):
    return is_equal(hash_password(clear_password, salt), hashed_password)


_users = {}
_user_ids = {}

def add_user(username, password):
    global _users, _user_ids
    salt = os.urandom(32)
    hashed = hash_password(password, salt)
    user_id = uuid.uuid4()

    user = dict(
        id=user_id,
        password=hashed,
        salt=salt,
        name=username
    )

    _users[username] = user
    _user_ids[user_id] = username

def get_username(user_id):
    if isinstance(user_id, bytes):
        try:
            user_id = uuid.UUID(bytes=user_id)
        except:
            return None

    if user_id in _user_ids:
        return _user_ids[user_id]
    return None

def get_user_id(username):
    if username in _users:
        return _users[username]['id']
    return None

def authenticate(username, password):
    if username in _users:
        # check password
        user = _users[username]

        return check_password(
            password,
            user['password'],
            user['salt']
        )

    return False
