from shared import messages


class KerborClient(object):
    user_name = ''
    user_password = ''
    user_secret = ''
    emitter = None

    def __init__(self, _username, _password):
        self.user_name = _username
        self.user_password = _password
        self.user_secret = 'SECRETsecretSECRETsecret12345678'

    def set_emitter(self, _emitter):
        self.emitter = _emitter

    def authenticate_for_service(self, tgs, service):
        if self.emitter is None:
            raise TypeError("emitter should be instance of Emitter")

        auth = messages.AuthenticateMeMessage(self.user_name, tgs)
        auth_response = self.emitter.emit(auth)

        tgs_sess_key = auth_response.get_sess_key(self.user_secret)
        id_message = messages.IDMessage(self.user_name)
        ticket_request = messages.TicketRequestMessage(service, id_message, tgs_sess_key, auth_response.tgt)
        ticket_response = self.emitter.emit(ticket_request)

        service_sess_key = ticket_response.get_c_s_key(tgs_sess_key)
        service_request = messages.ServiceRequestMessage(id_message, service_sess_key, ticket_response.grant)
        service_response = self.emitter.emit(service_request)

        return service_response.verify_time(service_sess_key, id_message.timestamp)
