# -*- coding: utf8 -*-

from queries        import *
from functions      import funct_infos
from variables      import tokens

from flask          import Flask, request, g
from flask_cors     import CORS
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
CORS(app)

auth = HTTPTokenAuth('Basic')

@auth.verify_token
def verify_token(token):
    if token in tokens:
        g.current_user = tokens[token]
        return True
    return False

@app.route('/infos')
@auth.login_required
def send_infos():
  return funct_infos(g.current_user)

@app.route('/pcs/id/<int:pcs_id>')
@auth.login_required
def send_pcs_info(pcs_id):
  result = query_pcs_id(pcs_id) # result will be a JSON
  if result:
    return result
  else:
    return '{}'

@app.route('/tiles')
@auth.login_required
def send_tiles_all_info():
  result = query_tiles_all() # result will be a JSON
  if result:
    return result
  else:
    return '{}'

@app.route('/tiles/<int:x>/<int:y>/<int:n>')
@auth.login_required
def send_tiles_info(x,y,n):
  result = query_tiles_zone(x,y,n) # result will be a JSON
  if result:
    return result
  else:
    return '{}'

@app.route('/foo', methods=['POST'])
@auth.login_required
def foo():
  if request.json:
    result = query_insert_fulljson(request.json)
    if result:
      return '{"Info": "Job done (' + str(result) + ')"}'
    else:
      return '{"Info": "Job failed"}'
  else:
    return '{"Info": "Not an JSON document"}'
