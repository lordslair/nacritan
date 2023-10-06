import json
import os

from app import app

# We work with the real token, and aim to receive 200 OK
tokens = eval(os.environ['AUTH_TOKENS'])
token = list(tokens.keys())[list(tokens.values()).index('PyTest')]
header_ok = json.loads('{"Authorization": "Basic ' + token + '"}')


def test_nacritan_data_infos():
    route = '/infos'
    response = app.test_client().open(route, headers=header_ok)

    assert json.loads(response.data.decode('utf8'))
    assert b'PyTest' in response.data


def test_nacritan_data_worldmap():
    route = '/worldmap'
    worldmap = '/tmp/test_nacritan_data_worldmap.png'
    response = app.test_client().open(route, headers=header_ok)
    open(worldmap, 'wb').write(response.data)

    from PIL import Image
    assert Image.open(worldmap)
    os.remove(worldmap)
