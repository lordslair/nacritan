# -*- coding: utf8 -*-

import os

from datetime import datetime
from flask import abort, Blueprint, request
from flask_httpauth import HTTPTokenAuth
from loguru import logger

from variables import TOKENS

# Initialize Blueprint and Auth
infos_get_bp = Blueprint('infos', __name__)
auth = HTTPTokenAuth('Basic')


@auth.verify_token
def verify_token(token):
    if token in TOKENS:
        logger.success(f'{token} @{TOKENS[token]}')
        return TOKENS[token]


@infos_get_bp.route('/infos', methods=['GET'])
@auth.login_required
def get_infos():
    if request.remote_addr in ["127.0.0.1", "172.17.0.1"]:
        return {
            "host": os.uname().nodename,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "user": auth.current_user(),
        }
    else:
        abort(403)
