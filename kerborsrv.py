import messages


tgs_keys = {
    'default': '9xziLRNZuqKUP5TmxIfObNvPQDR2PGw7O5_817IkQDw='
}


class KerborAuthenticationServer(object):
    user_server = None

    def __init__(self, _user_server):
        self.user_server = _user_server

    def handle(self, path, message):
        if not isinstance(message, basestring):
            raise TypeError("message must be a json-encoded string")

        if path == 'logmein':
            class_name, message_object = messages.AuthenticateMeMessage.deserialize(message)
            if class_name != "AuthenticateMeMessage":
                return messages.FailMessage().serialize()

            return self.authenticate_user(message_object).serialize()

    def authenticate_user(self, message):
        user = self.user_server.lookup(message.username)
        if user is None:
            return messages.FailMessage()

        if message.tgs not in tgs_keys:
            return messages.FailMessage()

        response = messages.AuthenticationResponseMessage(
            user.make_sess_key(),
            user.secret_key,
            user.make_tgt(),
            tgs_keys[message.tgs]
        )

        return response
