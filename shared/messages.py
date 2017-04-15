from cryptography.fernet import Fernet
from json import loads, dumps
import datetime
import time
import base64


class BaseMessage(object):
    _fernet = None

    def _set_key(self, key):
        self._fernet = Fernet(base64.urlsafe_b64encode(key))

    def _encrypt(self, message):
        return self._fernet.encrypt(message)

    def _decrypt(self, message):
        return self._fernet.decrypt(message)

    def serialize(self):
        fields = [('__classname', type(self).__name__)]
        for property_name, value in vars(self).iteritems():
            if not property_name.startswith('_') and not callable(value):
                fields.append((property_name, value))

        return dumps(fields)

    @classmethod
    def deserialize(cls, representation):
        try:
            fields = loads(representation)
        except Exception:
            return 'FailMessage', FailMessage()

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


class IDMessage(BaseMessage):
    username = ''
    timestamp = 0
    id_session_key = ''

    def __init__(self, _username):
        self.username = _username
        self.timestamp = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        self.id_session_key = '123'


class TicketRequestMessage(BaseMessage):
    server = ''
    id_message = ''
    tgt = ''

    def __init__(self, _server, _id, _sess_key, _tgt):
        self.server = _server
        self._set_key(_sess_key)
        self.id_message = self._encrypt(_id.serialize())
        self.tgt = _tgt

    def get_tgt(self, tgs_key):
        self._set_key(tgs_key)
        return self._decrypt(self.tgt)

    def get_id(self, _sess_key):
        self._set_key(_sess_key)
        representation = self._decrypt(self.id_message)
        return IDMessage.deserialize(representation)


class TicketMessage(BaseMessage):
    username = ''
    remote_address = ''
    valid_for = 0
    sess_key = ''

    def gen_sess_key(self):
        return base64.urlsafe_b64decode(self._fernet.generate_key())

    def __init__(self, _username, _address, _valid):
        self.username = _username
        self.remote_address = _address
        self.valid_for = _valid
        self.sess_key = self.gen_sess_key()


class GrantMessage(BaseMessage):
    server = ''
    ticket = ''

    def __init__(self, _server, _ticket, _serv_key):
        self.server = _server
        self._set_key(_serv_key)
        self.ticket = self._encrypt(_ticket.serialize())

    def get_ticket(self, _serv_key):
        self._set_key(_serv_key)
        representation = self._decrypt(self.ticket)
        return TicketMessage.deserialize(representation)


class TicketGrantingMessage(BaseMessage):
    grant = ''
    c_s_session_key = ''

    def __init__(self, _grant, _serv_key, _c_s_sess, _sess_key):
        self._set_key(_serv_key)
        self.grant = self._encrypt(_grant.serialize())
        self._set_key(_sess_key)
        self.c_s_session_key = self._encrypt(_c_s_sess)

    def get_c_s_key(self, _sess_key):
        self._set_key(_sess_key)
        return self._decrypt(self.c_s_session_key)


class ServiceRequestMessage(BaseMessage):
    grant = ''
    id_message = ''

    def __init__(self, _id, _sess_key, _grant):
        self._set_key(_sess_key)
        self.id_message = self._encrypt(_id.serialize())
        self.grant = _grant

    def get_id(self, _sess_key):
        self._set_key(_sess_key)
        representation = self._decrypt(self.id_message)
        return IDMessage.deserialize(representation)

    def get_grant(self, _serv_key):
        self._set_key(_serv_key)
        representation = self._decrypt(self.grant)
        return GrantMessage.deserialize(representation)


class ServiceGrantingMessage(BaseMessage):
    timestamp = ''

    def __init__(self, _time, _sess_key):
        self._set_key(_sess_key)
        self.timestamp = self._encrypt(str(_time))

    def verify_time(self, _sess_key, _expected_time):
        self._set_key(_sess_key)
        t = self._decrypt(self.timestamp)
        try:
            if int(t) == _expected_time:
                return True
        finally:
            return False
