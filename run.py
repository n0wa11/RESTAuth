#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --
import os, sys
if '-g' in sys.argv:
    os.environ['PSYCOGREEN'] = '1'


from restauth import app
from flask import request

app.run(debug=True, threaded=True, port=8005)

#PSYCOGREEN=true gunicorn restauth:app -k gevent -b 127.0.0.1:8005
