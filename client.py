from client import emitter, kerborclient
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username to authenticate with")
    parser.add_argument("password", help="Password to use")
    parser.add_argument("--proxy", help="Use HTTP proxy server")
    parser.add_argument("--server", help="Set Kerbor server manually", default='127.0.0.1:5000')

    args = parser.parse_args()
    http_emitter = emitter.Emitter('http://{}/'.format(args.server))
    if args.proxy:
        http_emitter.set_proxies({
            'http': 'http://{}'.format(args.proxy),
            'https': 'http://{}'.format(args.proxy)
        })

    client = kerborclient.KerborClient(args.username, args.password)
    client.set_emitter(http_emitter)

    print client.authenticate_for_service('default', 'database')
