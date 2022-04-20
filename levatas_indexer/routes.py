"""Flask URL routing

This module contains all of the routes for the flask application.
"""
from flask import Blueprint, jsonify, render_template, request
import validators  # type: ignore

from . import indexer

app_bp = Blueprint('app', __name__)


@app_bp.route('/')
def home():
    """Serve the home page of the web app"""
    return render_template('index.html')


@app_bp.route('/index')
def index_url():
    """Index the documents specified by the URL"""
    url = request.args.get('url', '')

    if not validators.url(url):
        return {'error': 'Must include a valid url'}, 400

    default_indexer = indexer.get_default_indexer()
    result = indexer.index_html_documents(url, default_indexer)

    return jsonify(result)
