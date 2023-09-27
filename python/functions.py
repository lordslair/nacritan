# -*- coding: utf8 -*-

# From: http://www.cdotson.com/2014/06/generating-json-documents-from-sqlite-databases-in-python/ # noqa
# Used to force SQL output as a dict, to format it as a JSON later
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def funct_worldmap(width, height, path):
    from PIL import Image
    from queries import query

    terrains_rgb = {
        "Plaine": (51, 204, 51),
        "Océan": (0, 102, 255),
        "Espace pavé": (128, 128, 128),
        "Terre battue": (153, 102, 51),
        "Plaine fleurie": (51, 153, 51,),
        }

    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = img.load()

    SQL_terrains = """SELECT DISTINCT type FROM tiles"""
    result_terrains = query(SQL_terrains, '', False, True)

    for terrain in result_terrains:
        SQL = """SELECT x,y FROM tiles WHERE type = ? """
        result = query(SQL, terrain, False, True)
        for (x, y) in result:
            pixels[x, y] = terrains_rgb[terrain[0]]

    img.save(path, 'PNG')
