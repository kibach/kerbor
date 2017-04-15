#!/usr/bin/python
from flask import Flask
from flask import make_response
from flask import request

from server.kerborsrv import KerborAuthenticationServer, KerborTicketGrantingServer, KerborServiceServer
from server.userserver import UserServer

app = Flask(__name__)
us = UserServer()
kerbor_as = KerborAuthenticationServer(us)
kerbor_tgs = KerborTicketGrantingServer(us)
kerbor_service = KerborServiceServer(us)


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


@app.route("/getmeticket", methods=['POST', 'GET'])
def get_me_ticket():
    if request.method == "GET":
        return "I expect TicketRequestMessage to be POSTed"

    json_obj = kerbor_tgs.handle(request.get_data())
    resp = make_response(json_obj)
    resp.headers['Content-Type'] = 'application/json'

    return resp


@app.route("/getmeservice", methods=['POST', 'GET'])
def get_me_service():
    if request.method == "GET":
        return "I expect ServiceRequestMessage to be POSTed"

    json_obj = kerbor_service.handle(request.get_data())
    resp = make_response(json_obj)
    resp.headers['Content-Type'] = 'application/json'

    return resp

if __name__ == '__main__':
    app.run()
