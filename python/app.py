# -*- coding: utf8 -*-

from queries    import *
from functions  import funct_greet
from flask      import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/greet')
def say_hello():
  return funct_greet()

@app.route('/pcs/id/<int:pcs_id>')
def send_pcs_info(pcs_id):
  result = query_pcs_id(pcs_id) # result will be a JSON
  if result:
    return result
  else:
    return '{}'

@app.route('/tiles')
def send_tiles_all_info():
  result = query_tiles_all() # result will be a JSON
  if result:
    return result
  else:
    return '{}'

@app.route('/tiles/<int:x>/<int:y>/<int:n>')
def send_tiles_info(x,y,n):
  result = query_tiles_zone(x,y,n) # result will be a JSON
  if result:
    return result
  else:
    return '{}'

@app.route('/foo', methods=['POST'])
def foo():
  if request.json:
    result = query_insert_fulljson(request.json)
    if result:
      return '{"Info": "Job done (' + str(result) + ')"}'
    else:
      return '{"Info": "Job failed"}'
  else:
    return '{"Info": "Not an JSON document"}'
