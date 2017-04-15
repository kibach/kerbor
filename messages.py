from cryptography.fernet import Fernet
from json import loads, dumps


class BaseMessage(object):
    _fernet = None

    def _set_key(self, key):
        self._fernet = Fernet(key)

    def _encrypt(self, message):
        return self._fernet.encrypt(message)

    def _decrypt(self, message):
        return self._fernet.decrypt(message)

    def serialize(self):
        fields = [('__classname', type(self).__name__)]
        for property_name, value in vars(self).iteritems():
            if not property_name.startswith('_') and not isinstance(value, callable):
                fields.append((property_name, value))

        return dumps(fields)

    @classmethod
    def deserialize(cls, representation):
        fields = loads(representation)
        _, class_name = fields.pop(0)

        msg = cls.__new__(cls)
        for property_name, value in fields:
            setattr(msg, property_name, value)

        return class_name, msg


class FailMessage(BaseMessage):
    pass


class AuthenticateMeMessage(BaseMessage):
    username = ''
    tgs = ''

    def __init__(self, _username, _tgs):
        self.username = _username
        self.tgs = _tgs


class AuthenticationResponseMessage(BaseMessage):
    session_key = ''
    tgt = ''

    def __init__(self, _sess_key, _secret_key, _tgt, _tgs_key):
        self._set_key(_secret_key)
        self.session_key = self._encrypt(_sess_key)
        self._set_key(_tgs_key)
        self.tgt = self._encrypt(_tgt)

