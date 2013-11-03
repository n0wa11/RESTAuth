#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# freeradius
FREERADIUS_SERVER = '127.0.0.1'
FREERADIUS_SECRET = 'secret'
FREERADIUS_NAS = 'nas'

AUTH_HEADER = 'X-Auth-Info' # Its value should be 'username/password' in clear text


