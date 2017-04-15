from simplekv.fs import FilesystemStore
import pickle


class BaseStorage(object):
    storage = None

    def get(self, key):
        pass

    def persist(self, key, _object):
        pass


class DictStorage(BaseStorage):
    def __init__(self):
        self.storage = {}

    def get(self, key):
        if key in self.storage:
            return self.storage[key]
        else:
            return None

    def persist(self, key, _object):
        self.storage[key] = _object


class SimpleKVStorage(BaseStorage):
    def __init__(self):
        self.storage = FilesystemStore('./.data')

    def get(self, key):
        if key in self.storage:
            return pickle.loads(self.storage.get(key))
        else:
            return None

    def persist(self, key, _object):
        self.storage.put(key, pickle.dumps(_object))
