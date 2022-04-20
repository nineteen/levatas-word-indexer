"""This module is responsible for configuring the flask applicaiton
and connecting the routes.
"""
import json
import logging.config
import logging
import os

from flask import Flask

from .paths import LOGGING_PATH
from .routes import app_bp

with open(LOGGING_PATH, encoding='utf-8') as fd:
    logging_config = json.load(fd)

logging.config.dictConfig(logging_config)

env = os.environ.get('APP_ENVIRONMENT', 'production')
app = Flask(__name__)

if env == 'dev':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


app.register_blueprint(app_bp)
