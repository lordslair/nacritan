# -*- coding: utf8 -*-

import json

from flask import Blueprint, jsonify
from flask_httpauth import HTTPTokenAuth
from loguru import logger
from mongoengine import Q

from mongo.models import (
    PlayerDocument,
    PlaceDocument,
    ResourceDocument,
    TileDocument,
    )

from variables import TOKENS

# Initialize Blueprint and Auth
minimap_get_bp = Blueprint('minimap', __name__)
auth = HTTPTokenAuth('Basic')


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        logger.success(f'{token} @{TOKENS[token]}')
        return TOKENS[token]


@minimap_get_bp.route('/minimap/<int:x>/<int:y>/<int:n>', methods=['GET'])
@auth.login_required
def get_minimap(x, y, n):
    # We fetch the player from DB
    try:
        logger.debug(f"[P] Looking for Player: {auth.current_user()}")
        query = (Q(name=auth.current_user()) & Q(guildId__exists=True))
        Player = PlayerDocument.objects(query).get()
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
        Guilders = PlayerDocument.objects(guildId=Player.guildId)
    except PlayerDocument.DoesNotExist:
        msg = "[G] PlayerDocument Query KO (404)"
        logger.debug(msg)
        return jsonify(msg), 404
    except Exception as e:
        logger.error(f'[G] PlayerDocument Query KO [{e}]')
    else:
        logger.trace(f'[G] {[Guilder.id for Guilder in Guilders]}]')

    # We Query the same rows that /tiles/x/y/n
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

    Tiles = TileDocument.objects.filter(query).exclude('created', 'user', 'updated').all()
    logger.debug(f'[T] {Tiles.count()} tiles found')
    # We convert the list of objects into a Python dict()
    tile_rows_dict = json.loads(Tiles.to_json())
    # tile_rows_dict = [Tile.to_mongo().to_dict() for Tile in Tiles]
    # We query with a SELECT ALL the tables to loop over
    # Way uglier, but way faster
    Places = PlaceDocument.objects(query)
    logger.debug(f'[P] {Places.count()} Places found')
    Resources = ResourceDocument.objects(query)
    logger.debug(f'[R] {Resources.count()} Resources found')
    Players = PlayerDocument.objects(query).filter(guildId=Player.guildId)
    logger.debug(f'[J] {Players.count()} Players found')

    # We loop over tiles to insert additional data
    for row in tile_rows_dict:
        # Little crappy trick to have same id fields like in v1
        row['id'] = row['_id']
        del row['_id']
        # Used for logging
        posxy = f"@({row['x']},{row['y']})"

        if Player.guildId:
            gdc_players = [
                Guilder for Guilder in Guilders if Guilder.x == row["x"] and Guilder.y == row["y"]
                ]
            if gdc_players and len(gdc_players) > 0:
                gdc_player = gdc_players[0]
                logger.trace(f"[G] {posxy}: [{gdc_player.id}] {gdc_player.name}")
                row.update({'on_tile': {'gdc': gdc_player.name}})

        pc_players = [
            Player for Player in Players if Player.x == row["x"] and Player.y == row["y"]
            ]
        if pc_players and len(pc_players) > 0:
            pc_player = pc_players[0]
            logger.trace(f"[J] {posxy}: [{pc_player.id}] {pc_player.name}")
            row.update({'on_tile': {'pc': pc_player.name}})

        places = [
            Place for Place in Places if Place.x == row["x"] and Place.y == row["y"]
            ]
        if places and len(places) > 0:
            place = places[0]
            logger.trace(f"[P] {posxy}: [{place.id}] {place.name}")
            row.update({'on_tile': {'place': place.name}})

        resources = [
            Resource for Resource in Resources if Resource.x == row["x"] and Resource.y == row["y"]
            ]
        if resources and len(resources) > 0:
            resource = resources[0]
            logger.trace(f"[R] {posxy}: [{resource.id}] {resource.name}")
            row.update({
                'on_tile': {
                    'resource': resource.name,
                    'level': resource.level,
                    }
                })

    return jsonify(tile_rows_dict), 200
