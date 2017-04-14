class BaseMessage(object):
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

    def __init__(self, _sess_key, _tgt):
        self.session_key = _sess_key
        self.tgt = _tgt


