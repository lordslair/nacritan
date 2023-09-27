# -*- coding: utf8 -*-

from queries import (
    query_insert_fulljson,
    query_insert_gdc,
    query_insert_tiles,
    query_insert_places,
    query_insert_pc,
    query_insert_pcs,
    query_insert_npcs,
    query_insert_resources,
    query_insert_objects,
    query_tiles_all,
    query_tiles_minimap,
    query_tiles_zone,
    query_select_gdc,
)
from functions import funct_infos, funct_worldmap
from variables import tokens

from flask import Flask, request, g, abort, send_file
from flask_cors import CORS
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


@app.route('/infos', methods=['GET'])
@auth.login_required
def get_infos():
    if request.remote_addr == "127.0.0.1":
        return funct_infos(g.current_user)
    else:
        abort(403)


@app.route('/tiles')
@auth.login_required
def send_tiles_all_info():
    result = query_tiles_all()  # result is JSON
    if result:
        return result
    else:
        return '{}'


@app.route('/tiles/<int:x>/<int:y>/<int:n>')
@auth.login_required
def send_tiles_info(x, y, n):
    result = query_tiles_zone(x, y, n)  # result is JSON
    if result:
        return result
    else:
        return '{}'


@app.route('/view', methods=['POST'])
@auth.login_required
def post_view():
    if request.json:
        result = query_insert_fulljson(request.json)
        if result:
            # Full JSON SUCCESSFULLY inserted
            # Now time to insert tiles
            query_insert_tiles(request.json, g.current_user)
            # Now time to insert places
            query_insert_places(request.json, g.current_user)
            # Now time to insert pcs
            query_insert_pcs(request.json, g.current_user)
            # Now time to insert npcs
            query_insert_npcs(request.json, g.current_user)
            # Now time to insert resources
            query_insert_resources(request.json, g.current_user)
            # Now time to insert objects
            query_insert_objects(request.json, g.current_user)
            return '{"Info": "Job done (' + str(result) + ')"}'
        else:
            return '{"Info": "Job failed"}'
    else:
        return '{"Info": "Not an JSON document"}'


@app.route('/pc/<int:pc_id>', methods=['POST'])
@auth.login_required
def post_pc(pc_id):
    if request.json:
        result = query_insert_pc(request.json, g.current_user)
        if result:
            return '{"Info": "Job done"}'
        else:
            return '{"Info": "Job failed"}'
    else:
        return '{"Info": "Not an JSON document"}'


@app.route('/gdc', methods=['GET'])
@auth.login_required
def get_gdc():
    result = query_select_gdc(g.current_user)
    if result:
        return result
    else:
        return '{"Info": "Job failed"}'


@app.route('/gdc', methods=['POST'])
@auth.login_required
def post_gdc():
    if request.json:
        result = query_insert_gdc(request.json, g.current_user)
    if result:
        return '{"Info": "Job done (' + str(result) + ')"}'
    else:
        return '{"Info": "Job failed (' + str(result) + ')"}'


@app.route('/worldmap')
def get_worldmap():
    path = '/var/tmp/worldmap.png'
    funct_worldmap(1000, 500, path)
    return send_file(path, as_attachment=False)


@app.route('/minimap/<int:x>/<int:y>/<int:n>')
@auth.login_required
def get_minimap(x, y, n):
    result = query_tiles_minimap(x, y, n, g.current_user)  # result is JSON
    if result:
        return result
    else:
        return '{}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)