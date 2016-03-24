import shelve

class PersistentConfig():
    def __init__(self, file_path=None):
        self.file_path = file_path

    def get_option(self, key):
        try:
            with shelve.open(self.file_path) as db:
                return db[key]
        except:
            return None

    def set_option(self, key, value):
        with shelve.open(self.file_path) as db:
            db[key] = value

__config = None

def init(file_path):
    global __config

    __config = PersistentConfig(file_path)

def get_option(key):
    return __config.get_option(key)

def set_option(key, value):
    __config.set_option(key, value)
