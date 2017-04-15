#!/usr/bin/python
from flask import Flask
from flask import make_response
from flask import request

from server.kerborsrv import KerborAuthenticationServer
from server.userserver import UserServer

app = Flask(__name__)
kerbor_as = KerborAuthenticationServer(UserServer())


@app.route("/")
def hello():
    resp = make_response("""Kerbor Srv
    / - help
    /logmein - Step1
    /getmeticket - Step2
    /getmeservice - Step3""")
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@app.route("/logmein", methods=['POST', 'GET'])
def log_me_in():
    if request.method == "GET":
        return "I expect AuthenticateMeMessage to be POSTed"

    json_obj = kerbor_as.handle(request.get_data())
    resp = make_response(json_obj)
    resp.headers['Content-Type'] = 'application/json'

    return resp

if __name__ == '__main__':
    app.run()
