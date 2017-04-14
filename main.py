#!/usr/bin/python


class KerborAuthenticationServer(object):
    user_server = None

    def __init__(self, _user_server):
        self.user_server = _user_server

    def authenticate_user(self, message):
        pass
