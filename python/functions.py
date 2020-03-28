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

def funct_greet():
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    host = os.uname().nodename
    json = '{"host": "' + host + '", "date": "' + date + '"}'
    return json
