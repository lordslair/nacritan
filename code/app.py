#!/usr/bin/env python3
# -*- coding: utf8 -*-

from datetime import datetime
from flask import Flask, request, abort, send_file, jsonify
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
from PIL import Image
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin
import os

app = Flask(__name__)
CORS(app)

os.environ.get("DISCORD_TOKEN", None)

MYSQL_USER = os.environ.get('MYSQL_USER', 'nacritan')
MYSQL_PASS = os.environ.get('MYSQL_PASS')
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_BASE = os.environ.get('MYSQL_BASE', 'nacritan')
MYSQL_URI = f'{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_BASE}'

# SQLAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_URI}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

auth = HTTPTokenAuth('Basic')

tokens = eval(os.environ['AUTH_TOKENS'])


#
# SQL Models (NEW)
#
class Player(db.Model, SerializerMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    level = db.Column(db.Integer)
    name = db.Column(db.Text, nullable=False)
    wounds = db.Column(db.Text)
    guildId = db.Column(db.Integer)
    guildName = db.Column(db.Text)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    user = db.Column(db.Text)

    race = db.Column(db.Text)
    img = db.Column(db.Text)
    dla = db.Column(db.Text)
    pas = db.Column(db.Text)
    pos = db.Column(db.Text)
    xp = db.Column(db.Text)
    xpMax = db.Column(db.Text)

    pv = db.Column(db.Integer)
    pvMax = db.Column(db.Integer)
    attM = db.Column(db.Integer)
    defM = db.Column(db.Integer)
    degM = db.Column(db.Integer)
    arm = db.Column(db.Integer)
    mmM = db.Column(db.Integer)
    pc = db.Column(db.Integer)

    date = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __init__(
      self,
      id,
      name,
      race=None,
      level=None,
      wounds=None,
      guildId=None,
      guildName=None,
      x=None,
      y=None,
      user=None,
      img=None,
      dla=None,
      pas=None,
      pos=None,
      xp=None,
      xpMax=None,
      pv=None,
      pvMax=None,
      attM=None,
      defM=None,
      degM=None,
      arm=None,
      mmM=None,
      pc=None,
      ):
        self.id = id
        self.level = level
        self.name = name
        self.wounds = wounds
        self.guildId = guildId
        self.guildName = guildName
        self.x = x
        self.y = y
        self.user = user
        self.race = race
        self.img = img
        self.dla = dla
        self.pas = pas
        self.pos = pos
        self.xp = xp
        self.xpMax = xpMax
        self.pv = pv
        self.pvMax = pvMax
        self.attM = attM
        self.defM = defM
        self.degM = degM
        self.arm = arm
        self.mmM = mmM
        self.pc = pc


class Place(db.Model, SerializerMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    townId = db.Column(db.Integer)
    townName = db.Column(db.Text)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    user = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __init__(
      self,
      id,
      level,
      name,
      townId,
      townName,
      x,
      y,
      user
      ):
        self.id = id
        self.level = level
        self.name = name
        self.townId = townId
        self.townName = townName
        self.x = x
        self.y = y
        self.user = user


class Monster(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    wounds = db.Column(db.Text)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    user = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __init__(
      self,
      id,
      level,
      name,
      wounds,
      x,
      y,
      user
      ):
        self.id = id
        self.level = level
        self.name = name
        self.wounds = wounds
        self.x = x
        self.y = y
        self.user = user


class Object(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    user = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __init__(
      self,
      id,
      name,
      x,
      y,
      user
      ):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.user = user


class Resource(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    user = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __init__(
      self,
      level,
      name,
      x,
      y,
      user
      ):
        self.level = level
        self.name = name
        self.x = x
        self.y = y
        self.user = user


class Tile(db.Model, SerializerMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    type = db.Column(db.Text, nullable=False)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    user = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def __init__(
      self,
      type,
      x,
      y,
      user
      ):
        self.type = type
        self.x = x
        self.y = y
        self.user = user


#
# API Routes
#

@auth.verify_token
def verify_token(token):
    if token in tokens:
        logger.success(f'{token} @{tokens[token]}')
        return tokens[token]


@app.route('/infos', methods=['GET'])
@auth.login_required
def get_infos():
    if request.remote_addr == "127.0.0.1":
        return {
            "host": os.uname().nodename,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": auth.current_user(),
        }
    else:
        abort(403)


@app.route('/tiles/<int:x>/<int:y>/<int:n>')
@auth.login_required
def send_tiles_info(x, y, n):
    tile_rows = Tile.query.filter(
        (
            (
                func.abs(x - Tile.x)
                + func.abs(y - Tile.y)
                + func.abs((-x - y) - (-Tile.x - Tile.y))
            )
            / 2
        )
        <= n
    ).all()

    logger.debug(f'[I] {len(tile_rows)} tiles found')
    return jsonify([row.to_dict() for row in tile_rows]), 200


@app.route('/view', methods=['POST'])
@auth.login_required
def post_view():
    if request.json:
        logger.trace(request.json)
    else:
        abort(400)

    # Now time to insert tiles
    for elem in request.json:
        # Here we have a tile
        # We may need to INSERT in DB if it doesn't exist on (x,y) coords
        # We check if already in DB or not
        if Tile.query.filter_by(
            type=elem['type'],
            x=elem['x'],
            y=elem['y']
        ).first():
            logger.debug(f"[=] {elem['type']} @({elem['x']},{elem['y']})")
            continue

        tile_new = Tile(
            type=elem['type'],
            x=elem['x'],
            y=elem['y'],
            user=auth.current_user()
            )
        db.session.add(tile_new)
        logger.debug(f"[+] {elem['type']} @({elem['x']},{elem['y']})")
        # Whatever happened, we commit()
        db.session.commit()

    # Now time to insert places
    for elem in request.json:
        if elem['items']['places']:
            # Here we have a place
            # We may need to INSERT in DB if it doesn't exist on (x,y) coords
            for place in elem['items']['places']:
                # We check if already in DB or not
                if Place.query.filter_by(id=place['id']).first():
                    logger.debug(f"[=] [{place['id']}] {place['name']}")
                    continue

                # We can INSERT
                if 'Portail' in place['name']:
                    place['townId'] = None  # Portals have no townId
                if 'Portail' in place['name']:
                    place['townName'] = None  # Portals have no townName

                place_new = Place(
                    id=place['id'],
                    level=place['level'],
                    name=place['name'],
                    townId=place['townId'],
                    townName=place['townName'],
                    x=elem['x'],
                    y=elem['y'],
                    user=auth.current_user()
                    )
                db.session.add(place_new)
                logger.debug(f"[+] [{place['id']}] {place['name']}")
                # Whatever happened, we commit()
                db.session.commit()
        else:
            # Here we are on coords (x,y) without a place
            # we should do nothing
            # BUT, maybe there was a place before, and vanished
            # We need to DELETE the row in that case
            place_todelete = Place.query.filter_by(
                x=elem['x'],
                y=elem['y'],
                ).one_or_none()
            if place_todelete:
                logger.debug(f"[-] [{place_todelete.id}] {place_todelete.name}") # noqa
                db.session.delete(place_todelete)
                # Whatever happened, we commit()
                db.session.commit()

    # Now time to insert players
    for elem in request.json:
        if elem['items']['pcs']:
            # Here we have a player
            # We may need to INSERT in DB if it doesn't exist on (x,y) coords
            for player in elem['items']['pcs']:
                if player['id'] is None or player['id'] == 'None':
                    # Weird shit, usually invoked creatures (ex: Feu Fol)
                    # We skip
                    continue

                # We check if already in DB or not
                player_db = Player.query.filter_by(id=player['id']).first()
                if player_db:
                    # Player already in DB, we just UPDATE some fields
                    logger.debug(f"[=] [{player['id']}] {player['name']}")
                    player_db.level = player['level']
                    player_db.guildId = player['guildId']
                    player_db.guildName = player['guildName']
                    player_db.wounds = player['wounds']
                    player_db.x = elem['x']
                    player_db.y = elem['y']
                else:
                    # Player not in DB, we can INSERT
                    player_new = Player(
                        id=player['id'],
                        guildId=player['guildId'],
                        guildName=player['guildName'],
                        level=player['level'],
                        name=player['name'],
                        wounds=player['wounds'],
                        x=elem['x'],
                        y=elem['y'],
                    )
                    db.session.add(player_new)
                    logger.debug(f"[+] [{player['id']}] {player['name']}")
                # Whatever happened, we commit()
                db.session.commit()
        else:
            # Here we are on coords (x,y) without a Player
            # we should do nothing
            # BUT, maybe there was a Player before, and vanished, died, moved.
            # We need to UPDATE his row in that case
            player_toupdate = Player.query.filter_by(
                x=elem['x'],
                y=elem['y'],
                ).one_or_none()
            if player_toupdate:
                player_toupdate.x = None
                player_toupdate.y = None
                logger.debug(f"[>] [{player_toupdate.id}] {player_toupdate.name}") # noqa
                # Whatever happened, we commit()
                db.session.commit()

    # Now time to insert npcs
    for elem in request.json:
        if elem['items']['npcs']:
            # Here we have a monster
            # We may need to INSERT in DB if it doesn't exist on (x,y) coords
            for monster in elem['items']['pcs']:
                if monster['id'] is None or monster['id'] == 'None':
                    # Weird shit, usually invoked creatures (ex: Feu Fol)
                    # We skip
                    continue

                # We check if already in DB or not
                monster_db = Monster.query.filter_by(id=monster['id']).first()
                if monster_db:
                    # Monster already in DB, we just UPDATE some fields
                    logger.trace(f"[=] [{monster['id']}] {monster['name']}")
                    monster_db.level = monster['level']
                    monster_db.wounds = monster['wounds']
                    monster_db.x = elem['x']
                    monster_db.y = elem['y']
                else:
                    # Monster not in DB, we can INSERT
                    monster_new = Monster(
                        id=monster['id'],
                        guildId=monster['guildId'],
                        guildName=monster['guildName'],
                        level=monster['level'],
                        name=monster['name'],
                        wounds=monster['wounds'],
                        x=elem['x'],
                        y=elem['y'],
                    )
                    db.session.add(monster_new)
                    logger.trace(f"[+] [{monster['id']}] {monster['name']}")
                # Whatever happened, we commit()
                db.session.commit()
        else:
            # Here we are on coords (x,y) without a Monster
            # we should do nothing
            # BUT, maybe there was a Monster before, and vanished, died, moved.
            # We need to DELETE the row in that case
            monster_todelete = Monster.query.filter_by(
                x=elem['x'],
                y=elem['y'],
                ).one_or_none()
            if monster_todelete:
                logger.trace(f"[-] [{monster_todelete.id}] {monster_todelete.name}") # noqa
                db.session.delete(monster_todelete)
                # Whatever happened, we commit()
                db.session.commit()

    # Now time to insert resources
    for elem in request.json:
        if elem['items']['resources']:
            # Here we have a resource
            # We may need to INSERT in DB if it doesn't exist on (x,y) coords
            for resource in elem['items']['resources']:
                # We check if already in DB or not
                if Resource.query.filter_by(
                    name=resource['name'],
                    x=elem['x'],
                    y=elem['y']
                ).first():
                    logger.trace(f"[=] {resource['name']} @({elem['x']},{elem['y']})") # noqa
                    continue

                resource_new = Resource(
                    level=resource['level'],
                    name=resource['name'],
                    x=elem['x'],
                    y=elem['y'],
                    user=auth.current_user()
                    )
                db.session.add(resource_new)
                logger.trace(f"[+] {resource['name']} @({elem['x']},{elem['y']})") # noqa
                # Whatever happened, we commit()
                db.session.commit()
        else:
            # Here we are on coords (x,y) without a resource
            # we should do nothing
            # BUT, maybe there was a resource before, and vanished
            # We need to DELETE the row in that case
            resource_todelete = Resource.query.filter_by(
                x=elem['x'],
                y=elem['y'],
                ).one_or_none()
            if resource_todelete:
                logger.trace(f"[-] {resource_todelete.name} @({elem['x']},{elem['y']})") # noqa
                db.session.delete(resource_todelete)
                # Whatever happened, we commit()
                db.session.commit()

    # Now time to insert objects
    for elem in request.json:
        if elem['items']['objects']:
            # Here we have an object
            # We may need to INSERT in DB if it doesn't exist on (x,y) coords
            for object in elem['items']['objects']:
                # We check if already in DB or not
                if Object.query.filter_by(id=object['id']).first():
                    logger.debug(f"[=] [{object['id']}] {object['name']}")
                    continue

                object_new = Object(
                    id=object['id'],
                    name=object['name'],
                    x=elem['x'],
                    y=elem['y'],
                    user=auth.current_user()
                    )
                db.session.add(object_new)
                logger.debug(f"[+] [{object['id']}] {object['name']}")
                # Whatever happened, we commit()
                db.session.commit()
        else:
            # Here we are on coords (x,y) without an object
            # we should do nothing
            # BUT, maybe there was an object before, and vanished
            # We need to DELETE the row in that case
            object_todelete = Object.query.filter_by(
                x=elem['x'],
                y=elem['y'],
                ).one_or_none()
            if object_todelete:
                logger.debug(f"[-] [{object_todelete.id}] {object_todelete.name}") # noqa
                db.session.delete(object_todelete)
                # Whatever happened, we commit()
                db.session.commit()

    return '{"Info": "Job done"}'


@app.route('/pc/<int:pc_id>', methods=['POST'])
@auth.login_required
def post_pc(pc_id):
    if request.json:
        logger.trace(request.json)
        if request.json['id']:
            if request.json['race'] is None:
                request.json['race'] = ''  # Dirty fix for unknown races

        player = Player.query.filter_by(id=request.json['id']).one_or_none()
        if player:
            # We need to UPDATE
            logger.debug(f"[=] [{player.id}] {player.name}")

            player.attM = request.json['caracs']['attM']
            player.arm = request.json['caracs']['arm']
            player.defM = request.json['caracs']['defM']
            player.degM = request.json['caracs']['degM']
            player.dla = request.json['dla']
            player.img = request.json['img']
            player.level = request.json['level'],
            player.mmM = request.json['caracs']['mmM']
            player.pas = request.json['pas']
            player.pc = request.json['caracs']['pc']
            player.pos = request.json['pos']
            player.pv = request.json['caracs']['pv']
            player.pvMax = request.json['caracs']['pvMax']
            player.x = request.json['x']
            player.xp = request.json['xp']
            player.xpMax = request.json['xpMax']
            player.y = request.json['y']
        else:
            logger.debug(f"[+] [{request.json['id']}] {request.json['name']}") # noqa
            player_new = Player(
                id=request.json['id'],
                attM=request.json['caracs']['attM'],
                arm=request.json['caracs']['arm'],
                defM=request.json['caracs']['defM'],
                degM=request.json['caracs']['degM'],
                dla=request.json['dla'],
                img=request.json['img'],
                level=request.json['level'],
                mmM=request.json['caracs']['mmM'],
                name=request.json['name'],
                pas=request.json['pas'],
                pc=request.json['caracs']['pc'],
                pos=request.json['pos'],
                pv=request.json['caracs']['pv'],
                pvMax=request.json['caracs']['pvMax'],
                race=request.json['race'],
                x=request.json['x'],
                xp=request.json['xp'],
                xpMax=request.json['xpMax'],
                y=request.json['y'],
            )
            db.session.add(player_new)
        db.session.commit()
        return '{"Info": "Job done"}'
    else:
        return '{"Info": "Not an JSON document"}'


@app.route('/gdc', methods=['GET'])
@auth.login_required
def get_gdc():
    # First, we fetch the player from DB
    player = Player.query.filter_by(name=auth.current_user()).first()
    logger.debug(player)
    if player is None:
        msg = '{"Info": "Job KO - Player NotFound"}'
        logger.warning(msg)
        return jsonify(msg), 200

    logger.debug(player)
    if player.guildId is None:
        msg = '{"Info": "Job OK - Player not in a GdC"}'
        logger.warning(msg)
        return jsonify(msg), 200

    # OK, we can query the GdC based on GuildId
    gdc_rows = Player.query.filter_by(guildId=player.guildId).all()

    return jsonify([row.to_dict() for row in gdc_rows]), 200


@app.route('/gdc', methods=['POST'])
@auth.login_required
def post_gdc():
    if request.json:
        pass
    else:
        abort(400)

    logger.trace(request.json)
    for elem in request.json:
        logger.trace(f'{elem}')
        if elem['id']:
            player = Player.query.filter_by(name=auth.current_user()).first()
            if player:
                # Player exists, we update only the Health & Position
                logger.debug(f"[=] [{elem['id']}] {elem['name']}")
                player.pc = elem['pc']
                player.x = elem['x'],
                player.y = elem['y'],
            else:
                # We create a new player from the GdC
                logger.debug(f"[+] [{elem['id']}] {elem['name']}")
                player = Player(
                    id=elem['id'],
                    name=elem['name'],
                    race=elem['race'],
                    level=elem['level'],
                    x=elem['x'],
                    y=elem['y'],
                    pc=elem['pc'],
                )
                db.session.add(player)

            # Whatever happened, we commit()
            db.session.commit()
    return '{"Info": "Job done"}'


@app.route('/worldmap')
def get_worldmap():
    terrains_rgb = {
        "Plaine": (51, 204, 51),
        "Océan": (0, 102, 255),
        "Espace pavé": (128, 128, 128),
        "Terre battue": (153, 102, 51),
        "Plaine fleurie": (51, 153, 51,),
        "Rivière": (0, 102, 255),
        "Montagne": (165, 42, 42),
        "Forêt": (107, 142, 35),
        "Désert": (255, 204, 153),
        "Marais": (51, 102, 0),
        }

    img = Image.new('RGBA', (1000, 500), (0, 0, 0, 0))
    pixels = img.load()

    tiles = Tile.query.with_entities(Tile.x, Tile.y, Tile.type).all()
    for tile in tiles:
        pixels[tile.x, tile.y] = terrains_rgb[tile.type]

    img.save('/var/tmp/worldmap.png', 'PNG')
    return send_file('/var/tmp/worldmap.png', as_attachment=False)


@app.route('/minimap/<int:x>/<int:y>/<int:n>')
@auth.login_required
def get_minimap(x, y, n):
    # We fetch the player from DB
    player = Player.query.filter_by(name=auth.current_user()).first()
    logger.trace(player)

    # We Query the same rows that /tiles/x/y/n
    tile_rows = Tile.query.filter(
        (
            (
                func.abs(x - Tile.x)
                + func.abs(y - Tile.y)
                + func.abs((-x - y) - (-Tile.x - Tile.y))
            )
            / 2
        )
        <= n
    ).all()
    logger.debug(f'[I] {len(tile_rows)} tiles found')

    # We convert the list of objects into a Python dict()
    tile_rows_dict = [row.to_dict() for row in tile_rows]
    # We query with a SELECT ALL the tables to loop over
    # Way uglier, but way faster
    places_db = Place.query.all()
    resources_db = Resource.query.all()
    players_db = Player.query.all()

    # We loop over tiles to insert additional data
    for row in tile_rows_dict:
        posxy = f"@({row['x']},{row['y']})"

        if player.guildId:
            gdc_players = [
                gdc_player
                for gdc_player in players_db
                if (
                    gdc_player.x == row["x"]
                    and gdc_player.y == row["y"]
                    and gdc_player.guildId == player.guildId
                    )
            ]
            if gdc_players and len(gdc_players) > 0:
                gdc_player = gdc_players[0]
                logger.debug(
                    f"[G] {posxy}: [{gdc_player.id}] {gdc_player.name}"
                    )
                row.update({'on_tile': {'gdc': gdc_player.name}})

        pc_players = [
            pc_player
            for pc_player in players_db
            if (
                pc_player.x == row["x"]
                and pc_player.y == row["y"]
                and pc_player.guildId != player.guildId
                )
        ]
        if pc_players and len(pc_players) > 0:
            pc_player = pc_players[0]
            logger.debug(f"[J] {posxy}: [{pc_player.id}] {pc_player.name}")
            row.update({'on_tile': {'pc': pc_player.name}})

        places = [
                place
                for place in places_db
                if place.x == row["x"] and place.y == row["y"]
            ]
        if places and len(places) > 0:
            place = places[0]
            logger.debug(f"[P] {posxy}: [{place.id}] {place.name}")
            row.update({'on_tile': {'place': place.name}})

        resources = [
                resource
                for resource in resources_db
                if resource.x == row["x"] and resource.y == row["y"]
            ]
        if resources and len(resources) > 0:
            resource = resources[0]
            logger.debug(f"[R] {posxy}: [{resource.id}] {resource.name}")
            row.update({
                'on_tile': {
                    'resource': resource.name,
                    'level': resource.level,
                    }
                })

    return jsonify(tile_rows_dict), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
