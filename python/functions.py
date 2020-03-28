# -*- coding: utf8 -*-

# From: http://www.cdotson.com/2014/06/generating-json-documents-from-sqlite-databases-in-python/
# Used to force SQL output as a dict, to format it as a JSON later
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
