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
