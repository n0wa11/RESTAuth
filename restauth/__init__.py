#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, traceback, time

# change timezone
os.environ['TZ'] = 'Asia/Shanghai'
time.tzset()

from flask import Flask, request, g, abort, jsonify
app = Flask(__name__)

import config
app.config.from_object('config')

# register views
from restauth.freeradius import views as freeradiusModule
app.register_blueprint(freeradiusModule)

# catch all error here
@app.errorhandler(Exception)
def catch_all(e):
    app.logger.error( "%s"%e )
    app.logger.error( "%s"% traceback.format_exc() )

    return jsonify(), 500