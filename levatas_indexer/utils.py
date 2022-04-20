"""Useful functions that have no other home.

Note: Generally stay away from adding  to the this file if there is an
existing module that is a better fit.  If you do add to this file avoid
importing from other internal modules. These utilites are inteded to be
used throughout the application, and importing from other internal modules
is likely to create circular references.
"""
from typing import Iterator, List
import logging
import urllib.parse

from bs4 import BeautifulSoup  # type: ignore
import requests
import validators  # type: ignore


def fetch_page(url: str) -> str:
    """Fetch a webpage from a url

    :param url: The url used to fetch the page
    :type url: str
    :return: The page that was fetched
    :rtype: str
    """
    logging.debug('Fetching page for url: %s', url)
    response = requests.get(url)

    if response.status_code != 200:
        logging.warning('Failed to fetch page (url: %s, status: %d).', url, response.status_code)
        return ''

    return response.text


def parse_html(html_doc: str) -> BeautifulSoup:
    """Parse an xml document with BeautifulSoup

    :param html_doc: The document to parse.
    :type html_doc: str
    :return: The parsed document
    :rtype: :class:`bs4.BeautifulSoup`
    """
    return BeautifulSoup(html_doc, 'html.parser')


def get_links(soup: BeautifulSoup, unique: bool = True) -> List[str]:
    """Extract hyperlinks from an html document

    :param soup: The parsed html document to search
    :type soup: :class:`bs4.BeautifulSoup`
    :param unique: Whether or not to remove duplicate links (default=True).
    :type unique: bool, optional
    :return: A list of urls
    :rtype: List[str]
    """
    links = []
    for link in soup.find_all('a'):
        url = link.get('href', '').strip()
        links.append(url)

    if unique:
        return list(set(links))

    return links


def sanitize_href(host_url: str, href: str) -> str:
    """Sanitize values from an href

    :param host_url: The url for the page the href is embedded
    :type host_url: str
    :param href: The raw value from the href attribute
    :type href: str
    :return: A sanitized URL
    :rtype: str
    """
    if href.startswith('//'):
        host_parsed = urllib.parse.urlparse(host_url)
        url = f'{host_parsed.scheme}://{host_parsed.netloc}{href[1:]}'

    elif href.startswith('/'):
        host_parsed = urllib.parse.urlparse(host_url)
        url = f'{host_parsed.scheme}://{host_parsed.netloc}{href}'

    else:
        url = href

    if not validators.url(url):
        raise ValueError(f'{url} is not a valid url')

    return url


def fetch_documents(url: str, visted: set, depth: int = 1) -> Iterator[str]:
    """A generator that recursively fetches web pages by URL

    Recursivel fetch documents based on a root url and any hyperlinks
    imbedded in the page. How deep to fetch documents is controlled by the
    depth parameter.  For example a depth of 1 will fetch the page specified
    by the url, and the pages of any embedded hyperlinks.

    NOTE: More effort should be spent on checking if a url has already been
    visted. For example this method will retrieve the html documents for both
    https://google.com and https://google.com/.  Another consideration might
    be made for handling http redirects, or identical paths with different
    query params.

    :param url: The root url to fetch
    :type url: str
    :param visted: A set for tracking urls that have already been visted
    :type visted: set
    :param depth: How keep to recursively fetch documents.
    :type depth: int
    :return: An iterator to iterate of the text of the web pages
    :rtype: Iterator[str]
    """

    text = fetch_page(url)
    visted.add(url)

    yield text

    if depth > 0:
        soup = parse_html(text)
        links = get_links(soup)

        for link in links:
            try:
                link = sanitize_href(url, link)

            except ValueError:
                logging.warning('Failed to sanitize URL (skipping %s)', link)
                continue

            if link in visted:
                continue

            new_depth = depth -1
            yield from fetch_documents(link, visted, depth=new_depth)
