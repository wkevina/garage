import hashlib
import uuid
import os

from services import config

HASH_ROUNDS = 1000

def hash_password(clear_password, salt):
        """Generates a secure hash of password"""
        return hashlib.pbkdf2_hmac('sha256',
                                   clear_password.encode(),
                                   salt,
                                   HASH_ROUNDS)

def check_password(clear_password, hashed_password, salt):
    return is_equal(hash_password(clear_password, salt), hashed_password)

def is_equal(a, b):
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0

def get_username(user_id):
    return _manager.get_username(user_id)

def get_user_id(username):
    return _manager.get_user_id(username)

def authenticate(username, password):
    return _manager.authenticate(username, password)


class AuthManager():
    def __init__(self):
        # Maps UUIDs to user info dicts
        self._users = {}
        # Maps user names to UUIDs
        self._user_ids = {}

    def sync(self):
        config.set_option('auth_users', self._users)
        config.set_option('auth_user_ids', self._user_ids)

    def load(self):
        self._users = config.get_option('auth_users') or {}
        self._user_ids = config.get_option('auth_user_ids') or {}

    def add_user(self, username, password):
        if username in self._user_ids:
            # Retrieve UUID for username
            user_id = self._user_ids[username]
            user_info = self._users[user_id]

            old_salt = user_info['salt']
            new_hash = hash_password(password, old_salt)

            # Compare old and new passwords
            if not is_equal(new_hash, user_info['password']):
                # Replace salt and password hash
                salt = os.urandom(32)
                hashed = hash_password(password, salt)
                user_info['salt'] = salt
                user_info['password'] = hashed

                # Save changes
                self.sync()

        else:
            salt = os.urandom(32)
            hashed = hash_password(password, salt)
            user_id = uuid.uuid4()

            user = dict(
                id=user_id,
                password=hashed,
                salt=salt,
                name=username
            )

            self._users[username] = user
            self._user_ids[user_id] = username

            # Save changes
            self.sync()

    def remove_user(self, username):
        if username in self._user_ids:
            user_id = self._user_ids[username]
            del self._user_ids[username]

            if user_id in self._users:
                del self._users[user_id]

            self.sync()

    def get_username(self, user_id):
        if isinstance(user_id, bytes):
            try:
                user_id = uuid.UUID(bytes=user_id)
            except:
                return None

        if user_id in self._user_ids:
            return self._user_ids[user_id]
        return None

    def get_user_id(self, username):
        if username in self._users:
            return self._users[username]['id']
        return None

    def authenticate(self, username, password):
        if username in self._users:
            # check password
            user = self._users[username]

            return check_password(
                password,
                user['password'],
                user['salt']
            )

        return False


_manager = AuthManager()


def clear():
    """Erase stored user credentials"""
    _manager._users = {}
    _manager._user_ids = {}
    _manager.sync()

def add_user(username, password):
    """Add user to auth system"""
    _manager.add_user(username, password)

def remove_user(username):
    _manager.remove_user(username)

def init():
    _manager.load()
