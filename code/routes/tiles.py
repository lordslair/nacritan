# -*- coding: utf8 -*-

import json

from flask import Blueprint, jsonify
from flask_httpauth import HTTPTokenAuth
from loguru import logger
from mongoengine import Q

from mongo.models import TileDocument

from variables import TOKENS

# Initialize Blueprint and Auth
tiles_get_bp = Blueprint('tiles', __name__)
auth = HTTPTokenAuth('Basic')


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        logger.success(f'{token} @{TOKENS[token]}')
        return TOKENS[token]


@tiles_get_bp.route('/tiles/<int:x>/<int:y>/<int:n>', methods=['GET'])
@auth.login_required
def tiles_get(x, y, n):

    maxx = x + n
    minx = x - n
    maxy = y + n
    miny = y - n

    query = (
        Q(x__gte=minx)
        & Q(x__lte=maxx)
        & Q(y__gte=miny)
        & Q(y__lte=maxy)
        )

    Tiles = TileDocument.objects.filter(query).exclude('created', 'user', 'updated')
    logger.debug(f'[I] {Tiles.count()} tiles found')
    # We convert the list of objects into a Python dict()
    tile_rows_dict = json.loads(Tiles.to_json())

    for row in tile_rows_dict:
        # Little crappy trick to have same id fields like in v1
        row['id'] = row['_id']
        del row['_id']

    return jsonify(tile_rows_dict), 200
