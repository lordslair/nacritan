# -*- coding: utf8 -*-

from flask import Blueprint, jsonify, send_file
from loguru import logger
from PIL import Image

from mongo.models import TileDocument

# Initialize Blueprint and Auth
worldmap_get_bp = Blueprint('worldmap', __name__)


@worldmap_get_bp.route('/worldmap', methods=['GET'])
def worldmap_get():
    terrains_rgb = {
        "Plaine": (51, 204, 51),
        "Océan": (0, 102, 255),
        "Espace pavé": (128, 128, 128),
        "Terre battue": (153, 102, 51),
        "Plaine fleurie": (51, 153, 51,),
        "Rivière": (0, 102, 255),
        "Montagne": (165, 42, 42),
        "Forêt": (107, 142, 35),
        "Désert": (255, 204, 153),
        "Marais": (51, 102, 0),
        }

    img = Image.new('RGBA', (1000, 500), (0, 0, 0, 0))
    pixels = img.load()

    try:
        Tiles = TileDocument.objects().only('x', 'y', 'type')
    except TileDocument.DoesNotExist:
        msg = "TileDocument Query KO (404)"
        logger.debug(msg)
        return jsonify(msg), 404
    except Exception as e:
        logger.error(f'TileDocument Query KO [{e}]')
    else:
        logger.trace(Tiles)

    for Tile in Tiles:
        pixels[Tile.x, Tile.y] = terrains_rgb[Tile.type]

    img.save('/var/tmp/worldmap.png', 'PNG')
    return send_file('/var/tmp/worldmap.png', as_attachment=False)
