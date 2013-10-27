#!/usr/bin/env python
# coding=utf8
import datetime, requests

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort, jsonify
from restauth import app

views = Blueprint('freeradius', __name__, url_prefix='/freeradius')

@views.route('/debug', methods=['GET'])
def debug():
    print request.environ
    return jsonify()

import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary

@views.route('/auth', methods=['GET'])
def auth():

    username = request.args.get('username', None)
    password = request.args.get('password', None)

    rad_server = app.config.get('FREERADIUS_SERVER')
    rad_secret = app.config.get('FREERADIUS_SECRET')
    rad_nas = app.config.get('FREERADIUS_NAS')

    assert rad_server and rad_secret and rad_nas, "Oops.."

    if username and password:

        srv=Client( server  = rad_server,
                    secret  = rad_secret,
                    dict    = Dictionary("dictionary")
                )

        req=srv.CreateAuthPacket(
                    code = pyrad.packet.AccessRequest,
                    User_Name = username,
                    NAS_Identifier = rad_nas
                )
        req["User-Password"]=req.PwCrypt(password)

        reply=srv.SendPacket(req)
        if reply.code==pyrad.packet.AccessAccept:
            print "access accepted"
            return jsonify(), 200
        else:
            print "access denied"
            return jsonify(), 403

    else:
        return jsonify(), 403

