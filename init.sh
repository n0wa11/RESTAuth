#!/usr/bin/env bash
# -*- coding: utf-8 -*-

sudo apt-get install -y python-dev python-pip
pip install virtualenv
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt
