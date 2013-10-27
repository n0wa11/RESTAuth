#!/usr/bin/env python
# -*- coding: utf-8 -*-

from restauth import app
from flask import request

# --
app.run(debug=True, threaded=True, port=8005)

