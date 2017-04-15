import messages


tgs_keys = {
    'default': '9xziLRNZuqKUP5TmxIfObNvPQDR2PGw7'
}


class KerborBaseServer(object):
    user_server = None
    accepted_message = messages.FailMessage

    def __init__(self, _user_server):
        self.user_server = _user_server

    def handle(self, message):
        if not isinstance(message, basestring):
            raise TypeError("message must be a json-encoded string")

        class_name, message_object = self.accepted_message.deserialize(message)
        if class_name != str(type(self.accepted_message).__name__):
            return messages.FailMessage().serialize()

        return self.dispatch(message_object).serialize()

    def dispatch(self, message):
        return messages.FailMessage()


class KerborAuthenticationServer(KerborBaseServer):
    accepted_message = messages.AuthenticateMeMessage

    def dispatch(self, message):
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
