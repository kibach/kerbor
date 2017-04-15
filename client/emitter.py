import requests
from shared import messages


class Emitter(object):
    remote_url = ''
    proxies = {}

    def __init__(self, _server):
        self.remote_url = _server

    def set_proxies(self, _proxies):
        self.proxies = _proxies

    def emit(self, message):
        method = ''
        if isinstance(message, messages.AuthenticateMeMessage):
            method = 'logmein'
        elif isinstance(message, messages.TicketRequestMessage):
            method = 'getmeticket'
        elif isinstance(message, messages.ServiceRequestMessage):
            method = 'getmeservice'

        data = message.serialize()
        r = requests.post('{}{}'.format(self.remote_url, method), data=data, proxies=self.proxies)

        response = None
        if method == 'logmein':
            class_name, response = messages.AuthenticationResponseMessage.deserialize(r.content)
            assert(class_name == 'AuthenticationResponseMessage')
        elif method == 'getmeticket':
            class_name, response = messages.TicketGrantingMessage.deserialize(r.content)
            assert (class_name == 'TicketGrantingMessage')
        elif method == 'getmeservice':
            class_name, response = messages.ServiceGrantingMessage.deserialize(r.content)
            assert (class_name == 'ServiceGrantingMessage')

        return response
