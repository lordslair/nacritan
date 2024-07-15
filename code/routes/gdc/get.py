# -*- coding: utf8 -*-

import json

from flask import Blueprint, jsonify
from flask_httpauth import HTTPTokenAuth
from loguru import logger
from mongoengine import Q

from mongo.models import PlayerDocument

from variables import TOKENS

# Initialize Blueprint and Auth
gdc_get_bp = Blueprint('gdc', __name__)
auth = HTTPTokenAuth('Basic')


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        logger.success(f'{token} @{TOKENS[token]}')
        return TOKENS[token]


@gdc_get_bp.route('/gdc', methods=['GET'])
@auth.login_required
def gdc_get():
    try:
        logger.debug(f"[P] Looking for Player: {auth.current_user()}")
        query = (Q(name=auth.current_user()) & Q(guildId__exists=True))
        Player = PlayerDocument.objects.filter(query).only('guildId').get()
    except PlayerDocument.DoesNotExist:
        msg = "[P] PlayerDocument Query KO (404)"
        logger.debug(msg)
        return jsonify(msg), 404
    except Exception as e:
        logger.error(f'[P] PlayerDocument Query KO [{e}]')
    else:
        logger.trace(f'[P] {Player.to_mongo().to_dict()}')

    # OK, we can query the GdC based on GuildId
    try:
        logger.debug(f"[G] Looking for Guild: {Player.guildId}")
        Guilders = PlayerDocument.objects.filter(guildId=Player.guildId).exclude('created', 'updated').all() # noqa E501
        guild_rows_dict = json.loads(Guilders.to_json())
    except PlayerDocument.DoesNotExist:
        msg = "[G] PlayerDocument Query KO (404)"
        logger.debug(msg)
        return jsonify(msg), 404
    except Exception as e:
        logger.error(f'[G] PlayerDocument Query KO [{e}]')
    else:
        logger.trace(f'[G] {[Guilder.id for Guilder in Guilders]}]')

    guilders = []
    for row in guild_rows_dict:
        row['id'] = row['_id']
        del row['_id']
        guilders.append(row)

    return jsonify(guilders), 200
