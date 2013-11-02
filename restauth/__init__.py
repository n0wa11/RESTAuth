#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, traceback, time

# change timezone
os.environ['TZ'] = 'Asia/Shanghai'
time.tzset()

from flask import Flask, request, g, abort, jsonify
from flask.ext.cache import Cache

app = Flask(__name__)

cache = Cache()
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

import config
if os.path.isfile('_config.py'):
    # _config.py is for my testing, not in the depo
    app.config.from_object('_config')
else:
    # config.py is supposed to be edited by users
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
