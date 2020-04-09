import json
import sys
import os

code = os.path.dirname(os.environ['FLASK_APP'])
sys.path.append(code)

from app import app

# We work with the real token, and aim to receive 200 OK
tokens    = eval(os.environ['AUTH_TOKENS'])
token     = list(tokens.keys())[list(tokens.values()).index('PyTest')]
header_ok = json.loads('{"Authorization": "Basic ' + token + '"}')

def test_nacritan_data_infos():
    route  = '/infos'
    response  = app.test_client().open(route, headers=header_ok)

    assert json.loads(response.data.decode('utf8'))
    assert b'PyTest' in response.data

def test_nacritan_data_tiles():
    route  = '/tiles'
    response  = app.test_client().open(route, headers=header_ok)

    assert json.loads(response.data.decode('utf8'))
    # Tonak, has coords { "x": 553, "y": 317 }
    assert b'"x": 553, "y": 317' in response.data
