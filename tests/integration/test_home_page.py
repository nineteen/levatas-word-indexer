import json

import pytest

from levatas_indexer.application import app


@pytest.fixture(scope='function')
def test_client():
    with app.test_client() as test_client:
        yield test_client


def test_home_page(test_client):
    response = test_client.get('/')

    assert response.status_code == 200
    assert b'Levatas Word Indexer' in response.data


def test_index_url(test_client):
    query_string = {'url': 'http://google.com'}
    response = test_client.get('/index', query_string=query_string)

    assert response.status_code == 200

    deserialized = json.loads(response.data.decode())

    assert isinstance(deserialized, dict)


def test_index_url_without_url(test_client):
    response = test_client.get('/index')

    assert response.status_code == 400


def test_index_url_with_invalid_url(test_client):
    query_string = {'url': 'google.com'}
    response = test_client.get('/index', query_string=query_string)

    assert response.status_code == 400
