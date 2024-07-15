#!/usr/bin/env python3
# -*- coding: utf8 -*-

from flask import Flask
from flask_cors import CORS

from routes.gdc.get import gdc_get_bp
from routes.gdc.post import gdc_post_bp
from routes.infos import infos_get_bp
from routes.minimap import minimap_get_bp
from routes.pc import pc_post_bp
from routes.tiles import tiles_get_bp
from routes.view import view_post_bp
from routes.worldmap import worldmap_get_bp

app = Flask(__name__)
CORS(app)


#
# API Routes
#
app.register_blueprint(gdc_get_bp)
app.register_blueprint(gdc_post_bp)
app.register_blueprint(infos_get_bp)
app.register_blueprint(minimap_get_bp)
app.register_blueprint(pc_post_bp)
app.register_blueprint(tiles_get_bp)
app.register_blueprint(view_post_bp)
app.register_blueprint(worldmap_get_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
