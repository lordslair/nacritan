# -*- coding: utf8 -*-

import sqlite3
import os
import json

from functions import dict_factory

db_name   = os.environ['SQLITE_DB_NAME']

# Meta Query
#          ┌ string - SQL query
#          |    ┌ array - params for placeholders
#          |    |    ┌ boolean - for row_factory
#          |    |    |       ┌ boolean - to switch between fetchone/fetchall
#          v    v    v       v
def query(SQL,params,dict,fetchall):
    db             = sqlite3.connect(db_name, timeout=20)
    if dict: db.row_factory = dict_factory # To force output as a dict
    cursor         = db.cursor()

    cursor.execute(SQL, params)

    if fetchall:
        result = cursor.fetchall()
    else:
        result = cursor.fetchone()

    cursor.close()
    db.close()
    if result:
        # We dump result into a JSON
        # ensure_ascii is used to avoid unicode and have UTF-8
        return json.dumps(result, ensure_ascii=False)
    else:
        return None

# Meta Query (for INSERT)
#                 ┌ string - SQL query
#                 |    ┌ array - params for placeholders
#                 v    v
def query_insert(SQL,params):
    db             = sqlite3.connect(db_name, timeout=20)
    cursor         = db.cursor()

    cursor.execute(SQL, params)

    db.commit()
    db.close()
    return cursor.lastrowid

def query_pcs_id(pcs_id):
    SQL     = """SELECT * FROM pcs WHERE id = ?"""
    result = query(SQL,(pcs_id,),True,False)
    if result:
        return result

def query_tiles_zone(x,y,n):
    SQL     = """SELECT * \
                 FROM tiles \
                 WHERE ( \
                           ABS(? - tiles.x) + ABS(? - tiles.y) \
                           + ABS((- ? - ?) - (- tiles.x - tiles.y))
                       ) / 2 <= ?"""
    result = query(SQL,(x,y,x,y,n),True,True)
    if result:
        return result

def query_tiles_all():
    SQL     = """SELECT * FROM tiles WHERE ?"""
    result = query(SQL,(1,),True,True)
    if result:
        return result

def query_insert_fulljson(rawjson):
    SQL     = """INSERT INTO jsons(data) VALUES (?)"""
    result  = query_insert(SQL, (json.dumps(rawjson),))
    if result:
        return result

def query_insert_tiles(rawjson,user):
    SQL_tiles = """REPLACE INTO tiles ( x, y, type, user )
                   SELECT ?, ?, ?, ?
                   WHERE NOT EXISTS
                   (SELECT 1 FROM tiles WHERE x = ? AND y = ? )"""
    for elem in rawjson:
        query_insert(SQL_tiles, (elem['x'],elem['y'],elem['type'],user,elem['x'],elem['y']))

def query_insert_places(rawjson,user):
    for elem in rawjson:
        if elem['items']['places']:
            for place in elem['items']['places']:
                if place['id']:
                    id = place['id']
                    if place['name'] == 'Portail': place['townId']   = None # Portals have no townId
                    if place['name'] == 'Portail': place['townName'] = None # Portals have no townName
                    SQL_places = ("""INSERT OR REPLACE INTO places ( id, level, name, townId, townName, x, y, user )
                                           VALUES (
                                                   COALESCE(?, (SELECT id        FROM places WHERE id = {} )),
                                                   COALESCE(?, (SELECT level     FROM places WHERE id = {} )),
                                                   COALESCE(?, (SELECT name      FROM places WHERE id = {} )),
                                                   COALESCE(?, (SELECT townId    FROM places WHERE id = {} )),
                                                   COALESCE(?, (SELECT townName  FROM places WHERE id = {} )),
                                                   COALESCE(?, (SELECT x         FROM places WHERE id = {} )),
                                                   COALESCE(?, (SELECT y         FROM places WHERE id = {} )),
                                                   COALESCE(?, (SELECT user      FROM places WHERE id = {} ))
                                                  )""").format(id, id, id, id, id, id, id, id)
                    query_insert(SQL_places, (place['id'], place['level'], place['name'], place['townId'], place['townName'], elem['x'], elem['y'], user))

def query_insert_pcs(rawjson,user):
    for elem in rawjson:
        if elem['items']['pcs']:
            for pc in elem['items']['pcs']:
                    id = pc['id']
                    SQL_pcs = ("""INSERT OR REPLACE INTO pcs ( id, level, name, wounds, guildId, guildName, x, y, user )
                                        VALUES (
                                                COALESCE(?, (SELECT id        FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT level     FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT name      FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT wounds    FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT guildId   FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT guildName FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT x         FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT y         FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT user      FROM pcs WHERE id = {} ))
                                               )""").format(id, id, id, id, id, id, id, id, id)
                    query_insert(SQL_pcs, (pc['id'], pc['level'], pc['name'], pc['wounds'], pc['guildId'], pc['guildName'], elem['x'], elem['y'], user))

def query_insert_npcs(rawjson,user):
    for elem in rawjson:
        if elem['items']['npcs']:
            for npc in elem['items']['npcs']:
                    id = npc['id']
                    SQL_npcs = ("""INSERT OR REPLACE INTO npcs ( id, level, name, wounds, x, y, user )
                                        VALUES (
                                                COALESCE(?, (SELECT id        FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT level     FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT name      FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT wounds    FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT x         FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT y         FROM pcs WHERE id = {} )),
                                                COALESCE(?, (SELECT user      FROM pcs WHERE id = {} ))
                                               )""").format(id, id, id, id, id, id, id)
                    query_insert(SQL_npcs, (pc['id'], pc['level'], pc['name'], pc['wounds'], elem['x'], elem['y'], user))

def query_insert_resources(rawjson,user):
    for elem in rawjson:
        if elem['items']['resources']:
            # Here we have a ressource, we may need to INSERT in DB if it doesn't exist on (x,y) coords
            for resource in elem['items']['resources']:
                SQL_resources = """REPLACE INTO resources ( level, name, x, y, user )
                                   SELECT ?, ?, ?, ?, ?
                                   WHERE NOT EXISTS
                                   (SELECT 1 FROM resources WHERE x = ? AND y = ? )"""
                query_insert(SQL_resources, (resource['level'], resource['name'], elem['x'], elem['y'], user, elem['x'], elem['y']))
        else:
            # Here we are on coords (x,y) without a ressource, we should do nothing
            # BUT, maybe there was a ressource before, and vanished. We need to DELETE the row in that case
            SQL_resources = """DELETE FROM resources WHERE x = ? AND y = ?"""
            query_insert(SQL_resources, (elem['x'], elem['y']))

def query_insert_objects(rawjson,user):
    for elem in rawjson:
        if elem['items']['objects']:
            # Here we have an object, we may need to INSERT in DB if it doesn't exist on (x,y) coords
            for object in elem['items']['objects']:
                SQL_objects = """REPLACE INTO objects ( id, name, x, y, user )
                                 SELECT ?, ?, ?, ?, ?
                                 WHERE NOT EXISTS
                                 (SELECT 1 FROM objects WHERE id = ? )"""
                query_insert(SQL_objects, (object['id'], object['name'], elem['x'], elem['y'], user, object['id']))
        else:
            # Here we are on coords (x,y) without a object, we should do nothing
            # BUT, maybe there was a object before, and vanished. We need to DELETE the row in that case
            SQL_objects = """DELETE FROM objects WHERE x = ? AND y = ?"""
            query_insert(SQL_objects, (elem['x'], elem['y']))
