# -*- coding: utf8 -*-

import os

from queries import *

from datetime import datetime
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/greet')
def say_hello():
  return '[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] Hello from Server: ' + os.uname().nodename

@app.route('/pcs/id/<int:pcs_id>')
def send_pcs_info(pcs_id):
  result = query_pcs_id(pcs_id) # result will be a JSON
  if result:
    return result
  else:
    return '{}'
