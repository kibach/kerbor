from shared import messages
import time, datetime


tgs_keys = {
    'default': '9xziLRNZuqKUP5TmxIfObNvPQDR2PGw7'
}

server_keys = {
    'database': 'YO4xNirT45SKSOsLSLZt7VNpvhyqfNES'
}


class KerborBaseServer(object):
    user_server = None
    accepted_message = None

    def __init__(self, _user_server):
        self.user_server = _user_server

    def handle(self, message):
        if not isinstance(message, basestring):
            raise TypeError("message must be a json-encoded string")

        class_name, message_object = self.accepted_message.deserialize(message)
        if class_name != str(self.accepted_message.__name__):
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

        self.user_server.associate_tgt(user)

        return response


class KerborTicketGrantingServer(KerborBaseServer):
    accepted_message = messages.TicketRequestMessage
    tgs_key = 'default'

    def dispatch(self, message):
        if message.server not in server_keys:
            return messages.FailMessage()

        tgt = message.get_tgt(tgs_keys[self.tgs_key])
        user = self.user_server.resolve_tgt(tgt)
        id = message.get_id(user.sess_key)
        current_timestamp = int(time.mktime(datetime.datetime.utcnow().timetuple()))

        if id.username != user.username or abs(id.timestamp - current_timestamp) > 30:
            return messages.FailMessage()

        ticket = messages.TicketMessage(user.username, '127.0.0.1', 86400)
        grant = messages.GrantMessage(message.server, ticket, server_keys[message.server])
        response = messages.TicketGrantingMessage(
            grant,
            server_keys[message.server],
            ticket.sess_key,
            user.sess_key
        )

        return response


class KerborServiceServer(KerborBaseServer):
    accepted_message = messages.ServiceRequestMessage
    server_key = 'database'

    def dispatch(self, message):
        grant = message.get_grant(server_keys[self.server_key])
        ticket = grant.get_ticket(server_keys[self.server_key])
        sess_key = ticket.sess_key

        id = message.get_id(sess_key)

        if grant.server != self.server_key:
            return messages.FailMessage()

        current_timestamp = int(time.mktime(datetime.datetime.utcnow().timetuple()))

        if ticket.remote_address != '127.0.0.1' or current_timestamp - id.timestamp - ticket.valid_for > 30:
            return messages.FailMessage()

        if ticket.username != id.username:
            return messages.FailMessage()

        response = messages.ServiceGrantingMessage(id.timestamp, sess_key)
        return response
