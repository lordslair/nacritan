# -*- coding: utf8 -*-

import datetime

from flask import abort, Blueprint, jsonify, request
from flask_httpauth import HTTPTokenAuth
from loguru import logger

from mongo.models import PlayerDocument

from variables import TOKENS

# Initialize Blueprint and Auth
pc_post_bp = Blueprint('pc', __name__)
auth = HTTPTokenAuth('Basic')


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        logger.success(f'{token} @{TOKENS[token]}')
        return TOKENS[token]


@pc_post_bp.route('/pc/<int:pc_id>', methods=['POST'])
@auth.login_required
def post_pc(pc_id):
    if request.json:
        logger.trace(request.json)
    else:
        abort(400)

    player = request.json
    if player['id'] and player['race'] is None:
        player['race'] = ''  # Dirty fix for unknown races
#    if player['caracs']['pc'] is None:
#        logger.success(player['caracs']['pc'])
#        logger.success(type(player['caracs']['pc']))
#        player['caracs']['pc'] = 100

    Player = PlayerDocument.objects(_id=player['id']).modify(
        upsert=True,
        new=True,
        set_on_insert__created=datetime.datetime.utcnow(),
        set__level=player['level'],
        set_on_insert__name=player['name'],
        set__user=auth.current_user(),
        set__x=player['x'],
        set__y=player['y'],

        set__attM=player['caracs']['attM'],
        set__arm=player['caracs']['arm'],
        set__dla=player['dla'],
        set__defM=player['caracs']['defM'],
        set__degM=player['caracs']['degM'],
        set__img=player['img'],
        set__mmM=player['caracs']['mmM'],
        set__pas=player['pas'],
        set__pc=player['caracs']['pc'],
        set__pos=player['pos'],
        set__pv=player['caracs']['pv'],
        set__pvMax=player['caracs']['pvMax'],
        set__xp=player['xp'],
        set__xpMax=player['xpMax'],
        set__updated=datetime.datetime.utcnow()
        )
    if Player.created == Player.updated:
        logger.info(f"[+] [{Player.id}] {Player.name}")
    else:
        logger.debug(f"[=] [{Player.id}] {Player.name}")

    return jsonify({"Info": "Job done"})
