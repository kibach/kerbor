from cryptography.fernet import Fernet
from storage import DictStorage
import base64


class BaseUserServer(object):
    pass


class User(object):
    username = ''
    password = ''
    secret_key = ''
    tgt = ''
    sess_key = ''
    perms = []

    def _get_key(self):
        return Fernet.generate_key()[:32]

    def __init__(self, _dict):
        if 'username' in _dict:
            self.username = _dict['username']

        if 'password' in _dict:
            self.password = _dict['password']

        if 'secret_key' in _dict:
            self.secret_key = _dict['secret_key']

        if 'tgt' in _dict:
            self.tgt = _dict['tgt']

        if 'sess_key' in _dict:
            self.sess_key = _dict['sess_key']

    def make_sess_key(self):
        self.sess_key = self._get_key()
        return self.sess_key

    def make_tgt(self):
        self.tgt = self._get_key()
        return self.tgt


class UserServer(BaseUserServer):
    user_storage = DictStorage()

    def lookup(self, username):
        obj = self.user_storage.get('user_' + username)
        if obj is None:
            obj = User({
                'username': username,
                'password': '123456',
                'secret_key': 'SECRETsecretSECRETsecret12345678'
            })
            self.user_storage.persist('user_' + username, obj)

        return obj

    def update(self, user):
        if not isinstance(user, User):
            raise TypeError("user must be an instance of User")

        self.user_storage.persist('user_' + user.username, user)

    def associate_tgt(self, user):
        self.user_storage.persist('tgt_' + user.tgt, user.username)

    def resolve_tgt(self, tgt):
        username = self.user_storage.get('tgt_' + tgt)
        if username is None:
            return None

        return self.lookup(username)
