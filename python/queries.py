# -*- coding: utf8 -*-

import sqlite3
import os
import json

from functions import dict_factory

db_name   = os.environ['SQLITE_DB_NAME']

# Meta Query using one parameter, and a fetchone()
def query_fetchone(SQL,param,dict):
    db             = sqlite3.connect(db_name, timeout=20)
    if dict: db.row_factory = dict_factory # To force output as a dict
    cursor         = db.cursor()

    cursor.execute(SQL, (param,))
    result = cursor.fetchone()

    cursor.close()
    db.close()
    if result:
        # We dump result into a JSON
        # ensure_ascii is used to avoid unicode and have UTF-8
        return json.dumps(result, ensure_ascii=False)
    else:
        return None

# Meta Query using one parameter, and a fetchall()
def query_fetchone(SQL,param,dict):
    db             = sqlite3.connect(db_name, timeout=20)
    if dict: db.row_factory = dict_factory # To force output as a dict
    cursor         = db.cursor()

    cursor.execute(SQL, (param,))
    result = cursor.fetchall()

    cursor.close()
    db.close()
    if result:
        # We dump result into a JSON
        # ensure_ascii is used to avoid unicode and have UTF-8
        return json.dumps(result, ensure_ascii=False)
    else:
        return None

def query_pcs_id(pcs_id):
    SQL     = """SELECT * FROM pcs WHERE id = ?"""
    result = query_fetchone(SQL,pcs_id,True)
    if result:
        return result

def query_tiles_zone(x,y,n):
    SQL     = """SELECT * \
                 FROM tiles \
                 WHERE ( \
                           ABS(? - tiles.x) + ABS(? - tiles.y) \
                         + ABS((- ? - ?) - (- tiles.x - tiles.y))
                       ) / 2 <= ?"""
    result = query_fetchall(SQL,(x,y,x,y,n),True)
    if result:
        return result

def query_tiles_all():
    SQL     = """SELECT * FROM tiles WHERE ?"""
    result = query_fetchall(SQL,(1,),True)
    if result:
        return result
