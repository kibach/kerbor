#!/usr/bin/python
from flask import Flask
from flask import make_response
from flask import request

from server.kerborsrv import KerborAuthenticationServer, KerborTicketGrantingServer, KerborServiceServer
from server.userserver import UserServer
from server.storage import SimpleKVStorage

app = Flask(__name__)
store = SimpleKVStorage()
us = UserServer(store)
kerbor_as = KerborAuthenticationServer(us)
kerbor_tgs = KerborTicketGrantingServer(us)
kerbor_service = KerborServiceServer(us)


@app.before_request
def log_request():
    logfile.write('{} {}\n'.format(request.method, request.path))
    logfile.write('{}\n\n->\n\n'.format(request.get_data()))


@app.after_request
def log_response(response):
    logfile.write('{}\n\n---\n\n'.format(response.get_data()))
    return response


@app.route('/')
def hello():
    resp = make_response("""Kerbor Srv
    / - help
    /newuser - Register a new user (web only)
    /logmein - Step1
    /getmeticket - Step2
    /getmeservice - Step3""")
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@app.route('/logmein', methods=['POST', 'GET'])
def log_me_in():
    if request.method == 'GET':
        return 'I expect AuthenticateMeMessage to be POSTed'

    json_obj = kerbor_as.handle(request.get_data())
    resp = make_response(json_obj)
    resp.headers['Content-Type'] = 'application/json'

    return resp


@app.route('/getmeticket', methods=['POST', 'GET'])
def get_me_ticket():
    if request.method == 'GET':
        return 'I expect TicketRequestMessage to be POSTed'

    json_obj = kerbor_tgs.handle(request.get_data())
    resp = make_response(json_obj)
    resp.headers['Content-Type'] = 'application/json'

    return resp


@app.route('/getmeservice', methods=['POST', 'GET'])
def get_me_service():
    if request.method == 'GET':
        return 'I expect ServiceRequestMessage to be POSTed'

    json_obj = kerbor_service.handle(request.get_data())
    resp = make_response(json_obj)
    resp.headers['Content-Type'] = 'application/json'

    return resp


@app.route('/newuser', methods=['POST', 'GET'])
def new_user():
    if request.method == 'GET':
        return """<form method=post>
          <input type=text placeholder=Username name=username><br>
          <input type=password placeholder=Password name=password><br>
          <input type=submit value=Submit>
        </form>"""
    else:
        if 'username' in request.form and 'password' in request.form:
            us.register(
                request.form['username'],
                request.form['password']
            )
            return 'Success'
        else:
            return 'Failure'

if __name__ == '__main__':
    logfile = open('reqs.log', 'w')
    app.run()
    logfile.close()
