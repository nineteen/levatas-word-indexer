"""Pure functions for processing text

This module provides text processors indended to be used with
:class:`levatas_indexer.indexer.Tokenizer`.  All functions defened here should
have the same function signature to ensure compatibility with the tokenizer.
"""
import string

from bs4 import BeautifulSoup  # type: ignore
from nltk.stem import PorterStemmer  # type: ignore

PORTER_STEMMER = PorterStemmer()


def strip_xml_from_doc(text: str) -> str:
    """Replace xml tags with whitespace

    :param text: The text to process
    :type text: str
    :return: The processed text
    :rtype: str
    """
    soup = BeautifulSoup(text, 'html.parser')

    return soup.get_text(separator=' ')


def cast_text_to_lower(text: str) -> str:
    """Convert text to lower case

    :param text: The text to process
    :type text: str
    :return: The processed text
    :rtype: str
    """
    return text.lower()


def remove_numeric_values(text: str) -> str:
    """Remove text if it is numeric

    Note: The method could probably be improved and won't catch all numbers.

    :param text: The text to process
    :type text: str
    :return: The processed text
    :rtype: str
    """
    sanitized = text.strip().replace('.', '').replace(',', '')

    if sanitized.isnumeric():
        return ''

    return text


def strip_whitespace(text: str) -> str:
    """Remove leading and trailing whitespace

    :param text: The text to process
    :type text: str
    :return: The processed text
    :rtype: str
    """
    return text.strip()


def strip_punctuation(text: str) -> str:
    """Remove leading and trailing punctuation

    :param text: The text to process
    :type text: str
    :return: The processed text
    :rtype: str
    """
    return text.strip(string.punctuation)


def stem_word(text: str) -> str:
    """Preform word stemming

    :param text: The text to process
    :type text: str
    :return: The processed text
    :rtype: str
    """
    return PORTER_STEMMER.stem(text)
