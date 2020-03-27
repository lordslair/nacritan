import os

from datetime import datetime
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return 'Server Works!'

@app.route('/greet')
def say_hello():
  return '[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] Hello from Server: ' + os.uname().nodename
