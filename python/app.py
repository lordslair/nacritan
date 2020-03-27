# -*- encoding: utf-8 -*-
import os
import sqlite3
import json

from datetime import datetime
from flask import Flask

app = Flask(__name__)

# dict_factory will help to format the SQLite as a JSON
# From: http://www.cdotson.com/2014/06/generating-json-documents-from-sqlite-databases-in-python/
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/greet')
def say_hello():
  return '[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] Hello from Server: ' + os.uname().nodename

@app.route('/pcs/id/<int:pcs_id>')
def send_pcs_info(pcs_id):
  sqliteConnection             = sqlite3.connect('/code/nacridan.db', timeout=20)
  sqliteConnection.row_factory = dict_factory
  sqliteSelectQuery            = """SELECT * FROM pcs WHERE id = ?"""

  cursor = sqliteConnection.cursor()
  cursor.execute(sqliteSelectQuery, (pcs_id,))
  results = cursor.fetchall()

  cursor.close()
  sqliteConnection.close()
  if results:
    return json.dumps(results, ensure_ascii=False)
  else:
    return '[{}]'
