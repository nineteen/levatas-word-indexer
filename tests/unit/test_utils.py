from unittest import mock
from unittest.mock import Mock

from bs4 import BeautifulSoup
import pytest

from levatas_indexer import utils


class TestFetchPage:

    def test_handles_status_code(self, monkeypatch):
        mock_get = Mock()
        mock_get.return_value.status_code = 400
        mock_get.return_value.text = 'Some error message'
        monkeypatch.setattr('requests.get', mock_get)

        result = utils.fetch_page('https://google.com')

        assert result == ''

    def test_returns_document(self, monkeypatch):
        mock_get = Mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = 'Some content'
        monkeypatch.setattr('requests.get', mock_get)

        result = utils.fetch_page('https://google.com')

        assert result == 'Some content'


class TestParseHtml:

    def test_returns_soup(self):
        result = utils.parse_html('Some Content')

        assert isinstance(result, BeautifulSoup)


class TestSanitizeHref:

    def test_handles_missing_url_data(self):
        href = '/some/path'
        host_url = 'https://google.com/some/other/path'

        result = utils.sanitize_href(host_url, href)

        assert result == 'https://google.com/some/path'

    def test_handles_double_slash(self):
        href = '//some/path'
        host_url = 'http://google.com/some/other/path'

        result = utils.sanitize_href(host_url, href)

        assert result == 'http://google.com/some/path'

    def test_invalid_url_raises_exception(self):
        href = 'asdfasdfasdfasdfasdfas'
        host_url = 'http://google.com/some/other/path'

        with pytest.raises(ValueError) as exc:
            utils.sanitize_href(host_url, href)

            assert exc.msg == f'{href} is not a valid url.'
