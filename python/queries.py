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
        if dict:
            # We dump result into a JSON
            # ensure_ascii is used to avoid unicode and have UTF-8
            return json.dumps(result, ensure_ascii=False)
        else:
            # We simply return values
            return result
    else:
        return None

# Meta Query (for INSERT)
#                 ┌ string - SQL query
#                 |    ┌ array - params for placeholders
#                 v    v
def query_insert(SQL,params):
    db             = sqlite3.connect(db_name, timeout=20)
    cursor         = db.cursor()

    try:
        cursor.execute(SQL, params)
        db.commit()
        db.close()
        return cursor.lastrowid
    except sqlite3.Error as e:
        import sys
        sys.stderr.write("SQLite INSERT Error %s:" % e.args[0])
        return None

def query_tiles_zone(x,y,n):
    SQL     = """SELECT id,x,y,type \
                 FROM tiles \
                 WHERE ( \
                           ABS(? - tiles.x) + ABS(? - tiles.y) \
                           + ABS((- ? - ?) - (- tiles.x - tiles.y))
                       ) / 2 <= ?"""
    result = query(SQL,(x,y,x,y,n),True,True)
    if result:
        return result

def query_tiles_minimap(x,y,n):
    SQL     = """SELECT x,y,type \
                 FROM tiles \
                 WHERE ( \
                           ABS(? - tiles.x) + ABS(? - tiles.y) \
                           + ABS((- ? - ?) - (- tiles.x - tiles.y))
                       ) / 2 <= ?"""
    result = query(SQL,(x,y,x,y,n),True,True)
    if result:
        result_json = json.loads(result)
        for elem in result_json:
            SQL_tile_res    = """SELECT name FROM resources WHERE ( x = ? AND y = ? )"""
            result_tile_res = query(SQL_tile_res,(elem['x'],elem['y'],),False,False)

            SQL_tile_pcs    = """SELECT name FROM pcs WHERE ( x = ? AND y = ? )"""
            result_tile_pcs = query(SQL_tile_pcs,(elem['x'],elem['y'],),False,False)

            SQL_tile_pla    = """SELECT name FROM places WHERE ( x = ? AND y = ? )"""
            result_tile_pla = query(SQL_tile_pla,(elem['x'],elem['y'],),False,False)

            if result_tile_res:
                elem.update({'on_tile': {'resource': result_tile_res[0]}})
            elif result_tile_pcs:
                elem.update({'on_tile': {'pc': result_tile_pcs[0]}})
            elif result_tile_pla:
                elem.update({'on_tile': {'place': result_tile_pla[0]}})
            else:
                elem.update({'on_tile': {}})
        return json.dumps(result_json)

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
            # Here we have a place, we may need to INSERT in DB if it doesn't exist on (x,y) coords
            for place in elem['items']['places']:
                if place['id']:
                    id = place['id']
                    if 'Portail' in place['name']: place['townId']   = None # Portals have no townId
                    if 'Portail' in place['name']: place['townName'] = None # Portals have no townName
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
        else:
            # Here we are on coords (x,y) without a place, we should do nothing
            # BUT, maybe there was a place before, and vanished. We need to DELETE the row in that case
            SQL_places = """DELETE FROM places WHERE x = ? AND y = ?"""
            query_insert(SQL_places, (elem['x'], elem['y']))

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
                                                COALESCE(?, (SELECT id        FROM npcs WHERE id = {} )),
                                                COALESCE(?, (SELECT level     FROM npcs WHERE id = {} )),
                                                COALESCE(?, (SELECT name      FROM npcs WHERE id = {} )),
                                                COALESCE(?, (SELECT wounds    FROM npcs WHERE id = {} )),
                                                COALESCE(?, (SELECT x         FROM npcs WHERE id = {} )),
                                                COALESCE(?, (SELECT y         FROM npcs WHERE id = {} )),
                                                COALESCE(?, (SELECT user      FROM npcs WHERE id = {} ))
                                               )""").format(id, id, id, id, id, id, id)
                    query_insert(SQL_npcs, (npc['id'], npc['level'], npc['name'], npc['wounds'], elem['x'], elem['y'], user))
        else:
            # Here we are on coords (x,y) without a npcs, we should do nothing
            # BUT, maybe there was a npc before, and vanished, died, moved. We need to DELETE the row in that case
            SQL_npcs = """DELETE FROM npcs WHERE x = ? AND y = ?"""
            query_insert(SQL_npcs, (elem['x'], elem['y']))

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

def query_insert_pc(rawjson,user):
    if rawjson['id']:
        if rawjson['race'] is None: rawjson['race'] = '' # Dirty fix waiting for race to be populated
        # INSERT OR UPDATE INTO pcsInfos
        SQL_pcinfos = """INSERT INTO pcsInfos ( id, name, race, img, dla, pas, pos, xp, xpMax, user )
                         VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
                         ON CONFLICT(id)
                         DO UPDATE SET img   = ?,
                                       dla   = ?,
                                       pas   = ?,
                                       pos   = ?,
                                       xp    = ?,
                                       xpMax = ?,
                                       user  = ?,
                                       date  = datetime('now');"""

        result_pcinfos =  query_insert(SQL_pcinfos,
                                       (rawjson['id'],
                                        rawjson['name'],
                                        rawjson['race'],  rawjson['img'],
                                        rawjson['dla'],   rawjson['pas'],
                                        rawjson['pos'],   rawjson['xp'],
                                        rawjson['xpMax'], user,
                                        rawjson['img'],
                                        rawjson['dla'],   rawjson['pas'],
                                        rawjson['pos'],   rawjson['xp'],
                                        rawjson['xpMax'], user))

        if rawjson['caracs']:
            # INSERT OR UPDATE INTO pcsCaracs
            SQL_pccaracs = """INSERT INTO pcsCaracs ( id, name, pv, pvMax, attM, defM, degM, arm, mmM, user )
                              VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
                              ON CONFLICT(id)
                              DO UPDATE SET pv    = ?,
                                            pvMax = ?,
                                            attM  = ?,
                                            defM  = ?,
                                            degM  = ?,
                                            arm   = ?,
                                            mmM   = ?,
                                            user  = ?,
                                            date  = datetime('now');"""

            result_pccaracs = query_insert(SQL_pccaracs,
                                           (rawjson['id'],
                                            rawjson['name'],
                                            rawjson['caracs']['pv'],   rawjson['caracs']['pvMax'],
                                            rawjson['caracs']['attM'], rawjson['caracs']['defM'],
                                            rawjson['caracs']['degM'], rawjson['caracs']['arm'],
                                            rawjson['caracs']['mmM'],  user,
                                            rawjson['caracs']['pv'],   rawjson['caracs']['pvMax'],
                                            rawjson['caracs']['attM'], rawjson['caracs']['defM'],
                                            rawjson['caracs']['degM'], rawjson['caracs']['arm'],
                                            rawjson['caracs']['mmM'],  user))

        if result_pcinfos and result_pccaracs:
            return 'OK'

def query_select_gdc(user):
    SQL_gdc_user_guildId    = """SELECT guildId
                                 FROM pcs
                                 WHERE name = ?
                                 LIMIT 1"""
    result_gdc_user_guildId = query(SQL_gdc_user_guildId, (user,), False, False)

    if result_gdc_user_guildId:

        guildId    = result_gdc_user_guildId[0]
        SQL_gdc    = """SELECT pcsInfos.id,pcsInfos.name,race,img,dla,pas,pos,xp,xpMax,pc,
                        pv,pvMax,attM,defM,degM,arm,mmM
                        FROM pcsInfos
                        INNER JOIN pcsCaracs on pcsInfos.id = pcsCaracs.id
                        INNER JOIN pcs on pcsInfos.id = pcs.id
                        WHERE pcs.guildId = ?"""
        result_gdc = query(SQL_gdc, (guildId,), True, True)

        if result_gdc:
            return result_gdc
        else:
            return '{"Info": "guildId (' + str(guildId) + ') received, but no SQL data retrieved"}'
    else:
        return '{"Info": "No guildId returned"}'

def query_insert_gdc(rawjson,user):
    count_elem   = 0
    SQL_gdc_race = """UPDATE pcsInfos
                      SET    race = ?
                      WHERE  id   = ?"""
    SQL_gdc_pc   = """UPDATE pcsCaracs
                      SET    pc   = ?
                      WHERE  id   = ?"""
    for elem in rawjson:
        count_elem += 1
        if elem['id']:
            result_gdc_race = query_insert(SQL_gdc_race, (elem['race'], elem['id']))
            if elem['pc']:
                result_gdc_pc = query_insert(SQL_gdc_pc, (elem['pc'], elem['id']))
        if result_gdc_race >= 0 and result_gdc_pc >= 0: count_elem -= 1
    return count_elem
