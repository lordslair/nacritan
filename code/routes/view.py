# -*- coding: utf8 -*-

import datetime

from flask import abort, Blueprint, jsonify, request
from flask_httpauth import HTTPTokenAuth
from loguru import logger

from mongo.models import MonsterDocument
from mongo.models import ObjectDocument
from mongo.models import PlaceDocument
from mongo.models import PlayerDocument
from mongo.models import ResourceDocument
from mongo.models import TileDocument

from variables import TOKENS

# Initialize Blueprint and Auth
view_post_bp = Blueprint('view', __name__)
auth = HTTPTokenAuth('Basic')


def processing_tile(elem):
    Tile = TileDocument.objects(type=elem['type'], x=elem['x'], y=elem['y']).modify(
        upsert=True,
        new=True,
        set_on_insert__created=datetime.datetime.utcnow(),
        set__type=elem['type'],
        set__user=auth.current_user(),
        set__x=elem['x'],
        set__y=elem['y'],
        set__updated=datetime.datetime.utcnow()
        )
    if Tile.created == Tile.updated:
        logger.info(f"[+] {Tile.type} @({Tile.x},{Tile.y})")
    else:
        logger.debug(f"[=] {Tile.type} @({Tile.x},{Tile.y})")


def processing_place(elem):
    if elem['items']['places']:
        # Here we have a place
        # We may need to INSERT in DB if it doesn't exist on (x,y) coords
        for place in elem['items']['places']:
            if 'Portail' in place['name']:
                place['townId'] = None  # Portals have no townId
                place['townName'] = None  # Portals have no townName

            Place = PlaceDocument.objects(_id=place['id']).modify(
                upsert=True,
                new=True,
                set_on_insert__created=datetime.datetime.utcnow(),
                set__level=place['level'],
                set__name=place['name'],
                set__townId=place['townId'],
                set__townName=place['townName'],
                set__user=auth.current_user(),
                set__x=elem['x'],
                set__y=elem['y'],
                set__updated=datetime.datetime.utcnow()
                )
            if Place.created == Place.updated:
                logger.info(f"[+] [{Place.id}] {Place.name}")
            else:
                logger.debug(f"[=] [{Place.id}] {Place.name}")
    else:
        # Here we are on coords (x,y) without a place
        # we should do nothing
        # BUT, maybe there was a place before, and vanished
        # We need to DELETE the row in that case
        Place = PlaceDocument.objects.filter(x=elem['x'], y=elem['y'])
        if Place:
            Place.delete()
            logger.warning(f"[-] [{Place.id}] {Place.name}")


def processing_player(elem):
    if elem['items']['pcs']:
        # Here we have a player
        # We may need to INSERT in DB if it doesn't exist on (x,y) coords
        for player in elem['items']['pcs']:
            if player['id'] is None or player['id'] == 'None':
                # Weird shit, usually invoked creatures (ex: Feu Fol)
                # We skip
                continue

            Player = PlayerDocument.objects(_id=player['id']).modify(
                upsert=True,
                new=True,
                set_on_insert__created=datetime.datetime.utcnow(),
                set__level=player['level'],
                set__name=player['name'],
                set__guildId=player['guildId'],
                set__guildName=player['guildName'],
                set__user=auth.current_user(),
                set__wounds=player['wounds'],
                set__x=elem['x'],
                set__y=elem['y'],
                set__updated=datetime.datetime.utcnow()
                )
            if Player.created == Player.updated:
                logger.info(f"[+] [{Player.id}] {Player.name}")
            else:
                logger.debug(f"[=] [{Player.id}] {Player.name}")
    else:
        # Here we are on coords (x,y) without a Player
        # we should do nothing
        # BUT, maybe there was a Player before, and vanished, died, moved.
        # We need to UPDATE his row in that case
        # Player = PlayerDocument.objects.filter(x=elem['x'], y=elem['y']).get()
        # if Player:
        #     Player.delete()
        #     logger.warning(f"[-] [{Player.id}] {Player.name}")
        # return True
        pass


def processing_npc(elem):
    if elem['items']['npcs']:
        # Here we have a monster
        # We may need to INSERT in DB if it doesn't exist on (x,y) coords
        for monster in elem['items']['npcs']:
            if monster['id'] is None or monster['id'] == 'None':
                # Weird shit, usually invoked creatures (ex: Feu Fol)
                # We skip
                continue

            Monster = MonsterDocument.objects(_id=monster['id']).modify(
                upsert=True,
                new=True,
                set_on_insert__created=datetime.datetime.utcnow(),
                set__level=monster['level'],
                set__name=monster['name'],
                set__user=auth.current_user(),
                set__wounds=monster['wounds'],
                set__x=elem['x'],
                set__y=elem['y'],
                set__updated=datetime.datetime.utcnow()
                )
            if Monster.created == Monster.updated:
                logger.info(f"[+] [{Monster.id}] {Monster.name}")
            else:
                logger.debug(f"[=] [{Monster.id}] {Monster.name}")
    else:
        # Here we are on coords (x,y) without a Monster
        # we should do nothing
        # BUT, maybe there was a Monster before, and vanished, died, moved.
        # We need to DELETE the row in that case
        Monster = MonsterDocument.objects.filter(x=elem['x'], y=elem['y'])
        if Monster:
            Monster.delete()
            logger.warning(f"[-] [{Monster.id}] {Monster.name}")
        return True


def processing_resource(elem):
    if elem['items']['resources']:
        # Here we have a resource
        # We may need to INSERT in DB if it doesn't exist on (x,y) coords
        for resource in elem['items']['resources']:
            Resource = ResourceDocument.objects(name=resource['name'], x=elem['x'], y=elem['y']).modify(  # noqa E501
                upsert=True,
                new=True,
                set_on_insert__created=datetime.datetime.utcnow(),
                set__level=resource['level'],
                set__name=resource['name'],
                set__user=auth.current_user(),
                set__x=elem['x'],
                set__y=elem['y'],
                set__updated=datetime.datetime.utcnow()
                )
            if Resource.created == Resource.updated:
                logger.info(f"[+] {Resource.name} @({Resource.x},{Resource.y})")
            else:
                logger.debug(f"[=] {Resource.name} @({Resource.x},{Resource.y})")
    else:
        # Here we are on coords (x,y) without a resource
        # we should do nothing
        # BUT, maybe there was a resource before, and vanished
        # We need to DELETE the row in that case
        Resource = ResourceDocument.objects.filter(x=elem['x'], y=elem['y'])
        if Resource:
            Resource.delete()
            logger.warning(f"[-] {Resource.name} @({Resource.x},{Resource.y})")


def processing_object(elem):
    if elem['items']['objects']:
        # Here we have an object
        # We may need to INSERT in DB if it doesn't exist on (x,y) coords
        for object in elem['items']['objects']:
            Object = ObjectDocument.objects(_id=object['id']).modify(
                upsert=True,
                new=True,
                set_on_insert__created=datetime.datetime.utcnow(),
                set__name=object['name'],
                set__user=auth.current_user(),
                set__x=elem['x'],
                set__y=elem['y'],
                set__updated=datetime.datetime.utcnow()
                )
            if Object.created == Object.updated:
                logger.info(f"[+] [{Object.id}] {Object.name}")
            else:
                logger.debug(f"[=] [{Object.id}] {Object.name}")
    else:
        # Here we are on coords (x,y) without an object
        # we should do nothing
        # BUT, maybe there was an object before, and vanished
        # We need to DELETE the row in that case
        Object = ObjectDocument.objects.filter(x=elem['x'], y=elem['y'])
        if Object:
            Object.delete()
            logger.warning(f"[-] [{Object.id}] {Object.name}")
        return True


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        logger.success(f'{token} @{TOKENS[token]}')
        return TOKENS[token]


@view_post_bp.route('/view', methods=['POST'])
@auth.login_required
def post_view():
    if request.json:
        logger.trace(request.json)
    else:
        abort(400)

    # Now time to insert tiles
    # process_tiles(request.json)
    for elem in request.json:
        processing_tile(elem)

    # Now time to insert places
    for elem in request.json:
        processing_place(elem)

    # Now time to insert players
    for elem in request.json:
        processing_player(elem)

    # Now time to insert npcs
    for elem in request.json:
        processing_npc(elem)

    # Now time to insert resources
    for elem in request.json:
        processing_resource(elem)

    # Now time to insert objects
    for elem in request.json:
        processing_object(elem)

    return jsonify({"Info": "Job done"}), 200
