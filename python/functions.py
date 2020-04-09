# -*- coding: utf8 -*-

import os

from datetime import datetime

# From: http://www.cdotson.com/2014/06/generating-json-documents-from-sqlite-databases-in-python/
# Used to force SQL output as a dict, to format it as a JSON later
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def funct_infos(current_user):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    host = os.uname().nodename
    json = '{"host": "' + host + '", "date": "' + date + '", "user": "' + current_user + '"}'
    return json

def funct_worldmap(width, height, path):
    from PIL       import Image
    from variables import terrains_rgb
    from queries   import query

    img    = Image.new('RGBA', (width,height), (0, 0, 0, 0))
    pixels = img.load()

    SQL_terrains    = """SELECT DISTINCT type FROM tiles"""
    result_terrains = query(SQL_terrains, '', False, True)

    for terrain in result_terrains:
        SQL     = """SELECT x,y FROM tiles WHERE type = ? """
        result  = query(SQL, terrain, False, True)
        for (x,y) in result: pixels[x,y] = terrains_rgb[terrain[0]]

    img.save(path, 'PNG')
