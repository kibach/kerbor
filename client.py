from client import emitter, kerborclient

if __name__ == '__main__':
    http_emitter = emitter.Emitter('http://127.0.0.1:5000/')
    http_emitter.set_proxies({
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    })
    client = kerborclient.KerborClient('test', '123456')
    client.set_emitter(http_emitter)
    print client.authenticate_for_service('default', 'database')
