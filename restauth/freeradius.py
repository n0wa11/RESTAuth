#!/usr/bin/env python
# coding=utf8
import datetime, requests, urllib

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, abort, jsonify
from restauth import app, cache

views = Blueprint('freeradius', __name__, url_prefix='/freeradius')

@views.route('/debug', methods=['GET'])
def debug():
    print request.environ
    return jsonify()

import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary

#http://stackoverflow.com/questions/9413566/flask-cache-memoize-url-query-string-parameters-as-well
def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return urllib.quote( (path + args).encode('utf-8') )

@views.route('/auth', methods=['GET'])
@cache.cached(timeout=30, key_prefix=make_cache_key)
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
            #print "status 200"
            return jsonify(), 200
        else:
            #print "status 403"
            return jsonify(), 403

    else:
        #print "status 400"
        return jsonify(), 400

