class BaseStorage(object):
    pass


class DictStorage(object):
    storage = {}

    def get(self, key):
        if key in self.storage:
            return self.storage[key]
        else:
            return None

    def persist(self, key, _object):
        self.storage[key] = _object
