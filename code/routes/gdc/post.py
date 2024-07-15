# -*- coding: utf8 -*-

import datetime

from flask import abort, Blueprint, jsonify, request
from flask_httpauth import HTTPTokenAuth
from loguru import logger

from mongo.models import PlayerDocument

from variables import TOKENS

# Initialize Blueprint and Auth
gdc_post_bp = Blueprint('gdc_post', __name__)
auth = HTTPTokenAuth('Basic')


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        logger.success(f'{token} @{TOKENS[token]}')
        return TOKENS[token]


@gdc_post_bp.route('/gdc', methods=['POST'])
@auth.login_required
def gdc_post():
    if request.json:
        pass
    else:
        abort(400)

    logger.trace(request.json)
    for elem in request.json:
        logger.trace(f'{elem}')
        if elem['id']:
            Player = PlayerDocument.objects(_id=elem['id']).modify(
                upsert=True,
                new=True,
                set_on_insert__created=datetime.datetime.utcnow(),
                set__level=elem['level'],
                set_on_insert__name=elem['name'],
                set__pc=elem['pc'],
                set_on_insert__race=elem['race'],
                set__user=auth.current_user(),
                set__x=elem['x'],
                set__y=elem['y'],
                set__updated=datetime.datetime.utcnow()
                )
            if Player.created == Player.updated:
                logger.info(f"[+] [{Player.id}] {Player.name}")
            else:
                logger.debug(f"[=] [{Player.id}] {Player.name}")

    return jsonify({"Info": "Job done"}), 200
