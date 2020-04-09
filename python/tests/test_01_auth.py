import json
import sys
import os

code = os.path.dirname(os.environ['FLASK_APP'])
sys.path.append(code)

from app import app

# We work with a fake token, and aim to receive 401 Unauthorized
header_ko = json.loads('{"Authorization": "Basic NMyWrongToken=="}')

def test_nacritan_auth_MyWrongToken_infos():
    route     = '/infos'
    response  = app.test_client().open(route, headers=header_ko)
    assert response.status_code == 401

def test_nacritan_auth_MyWrongToken_tiles():
    route     = '/tiles'
    response  = app.test_client().open(route, headers=header_ko)
    assert response.status_code == 401

def test_nacritan_auth_MyWrongToken_gdc():
    route     = '/gdc'
    response  = app.test_client().open(route, headers=header_ko)
    assert response.status_code == 401

# We work with the real token, and aim to receive 200 OK
tokens    = eval(os.environ['AUTH_TOKENS'])
token     = list(tokens.keys())[list(tokens.values()).index('PyTest')]
header_ok = json.loads('{"Authorization": "Basic ' + token + '"}')

def test_nacritan_auth_MyRightToken_infos():
    route     = '/infos'
    response  = app.test_client().open(route, headers=header_ok)
    assert response.status_code == 200

def test_nacritan_auth_MyRightToken_tiles():
    route     = '/tiles'
    response  = app.test_client().open(route, headers=header_ok)
    assert response.status_code == 200

def test_nacritan_auth_MyRightToken_gdc():
    route     = '/gdc'
    response  = app.test_client().open(route, headers=header_ok)
    assert response.status_code == 200

# We work without token, as it is 'public' URLs
def test_nacritan_auth_public_worldmap():
    route     = '/worldmap'
    response  = app.test_client().open(route)
    assert response.status_code == 200
