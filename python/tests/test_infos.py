import json
import sys
import os

code = os.path.dirname(os.environ['FLASK_APP'])
sys.path.append(code)

from app import app

route  = '/infos'

def test_nacritan_infos_auth():
    # Check if wrong token issues an 401 Unauthorized
    token     = 'NMyWrongToken=='
    app_token = json.loads('{"Authorization": "Basic ' + token + '"}')

    response  = app.test_client().open(route, headers=app_token)

    assert response.status_code == 401

def test_nacritan_infos_return():
    # Check if proper token issues a 200 OK, and info received
    tokens    = eval(os.environ['AUTH_TOKENS'])
    token     = list(tokens.keys())[list(tokens.values()).index('PyTest')]
    app_token = json.loads('{"Authorization": "Basic ' + token + '"}')

    response  = app.test_client().open(route, headers=app_token)

    assert response.status_code == 200
    assert b'PyTest' in response.data
