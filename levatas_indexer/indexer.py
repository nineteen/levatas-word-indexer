"""Abstractions for tokenizing and indexing

This module provides a customizable tokenizer for processesing text documents
and a basic indexer that counts the number of occurrences of a give word. You
may find the text processors in :module:`levatas_indexer.processors` useful
when configuring the :class:`levatas_indexer.indexer.Tokenizer`.

It also contains helper funtioncs for getting a pre-configured default indexer
and indexing web pages based on a root url.
"""
from collections.abc import Callable
from collections import defaultdict
from typing import List, Literal, TypedDict

import nltk  # type: ignore

from . import processors, utils


class ProcessorDict(TypedDict):
    """Type decloration for dictionary that holds processors"""
    word: List[Callable[[str], str]]
    document: List[Callable[[str], str]]


class Tokenizer:
    """Configurable class for processing text documents

    The intent is to add as many text processesors to an instance of this
    class as are needed. It currently supports two types of processors.

    Document processors act on the entire body of text, where as word
    processors act on indivdual words in the text.

    :param delimiter: The delimiter to use when spliting the text
    :type delimiter: str
    """
    def __init__(self, delimiter: str = ' '):
        """Constructor method

        :param delimiter: The delimiter to use when spliting the text
        :type delimiter: str
        """
        self.delimiter = delimiter
        self._processors: ProcessorDict = {
            'word': [],
            'document': []
        }

    def _process(self, type_: Literal['word', 'document'], document: str) -> str:
        """Iterate over the callbacks defined by type_ and invoke them on the
        given document

        :param type_: The type of the processors to run (word, document)
        :type type_: str
        :param document: The document to process
        :type document: str
        :return: The proccessed text
        :rtype: str
        """
        for processor in self._processors.get(type_, []):
            if document is None:
                return ''

            document = processor(document)

        return document

    def add_word_processor(self, callback: Callable[[str], str]) -> None:
        """Add a word processor to the tokenizer

        Word processors are functions that take in a string of text and return
        the processed text. The input text to the function will be a single
        word as defined by the class' delimiter attribute.

        :param callback: The text processor to add
        :type callback: Callable[[str], str]
        """
        self._processors['word'].append(callback)

    def add_document_processor(self, callback: Callable[[str], str]) -> None:
        """Add a document processor to the tokenizer

        Document processors are functions that take in a string of text and
        return the processed text.  The input text to the function will be the
        entire body of text.

        :param callback: The text processor to add
        :type callback: Callable[[str], str]
        """
        self._processors['document'].append(callback)

    def tokenize(self, document: str) -> List[str]:
        """Split a body of text into individual tokens

        :param document: The body of text to tokenize
        :type document: str
        :param
        """
        tokens = []
        document = self._process('document', document)

        for word in document.split(self.delimiter):
            word = self._process('word', word)

            if not word:
                continue

            tokens.append(word)

        return tokens


class NLTKTokenizer(Tokenizer):
    """Subclass of :class:`levatas_indexer.indexer.Tokenizer` that uses the
    natural languate toolkit to tokenzie the text instead of splitting
    """
    def tokenize(self, document: str) -> List[str]:
        """Split a body of text into individual tokens

        :param document: The body of text to tokenize
        :type document: str
        :param
        """
        tokens = []
        document = self._process('document', document)

        for word in nltk.word_tokenize(document):
            word = self._process('word', word)
            tokens.append(word)

        return tokens


class WordIndexer:
    """Simple indexer to count the number of occurance of each word

    :param tokenizer: A tokenizer for splitting the text
    :type tokenizer: :class:`levatas_indexer.indexer.Tokenizer`
    :param index: The running index for all documents processed
    :type index: dict
    """
    def __init__(self, tokenizer):
        """Constructor method

        :param tokenizer: An instance of a tokenizer to use
        :type tokenizer: :class:`levatas_indexer.indexer.Tokenizer`
        """
        self.tokenizer = tokenizer
        self._words = defaultdict(int)

    @property
    def index(self) -> dict:
        """Property for accessing a copy of the index

        This method casts the defaultdict back to a normal dict returning a
        copy so that changes made to the return value do not corrupt the index
        """
        return dict(self._words)

    def index_text(self, text: str) -> None:
        """Add a document to the running index

        :param text: A text document to index
        :type text: str
        """
        for word in self.tokenizer.tokenize(text):
            self._words[word] += 1

    def count(self, word: str) -> int:
        """Get the number of occurrences of the given word in the indexed
        documents

        :param word: The word to search for
        :type word: str
        :return: The number of occurrences of a given word
        :rtype: int
        """
        return self._words.get(word, 0)


def get_default_indexer() -> WordIndexer:
    """Retrieve and instance of a pre-configured word indexer

    :return: An instance of an indexer
    :rtype: :class:`levatas_indexer.indexer.WordIndexer`
    """
    tokenizer = NLTKTokenizer()
    tokenizer.add_document_processor(processors.strip_xml_from_doc)
    tokenizer.add_word_processor(processors.cast_text_to_lower)
    tokenizer.add_word_processor(processors.stem_word)

    return WordIndexer(tokenizer)


def index_html_documents(url: str, indexer: WordIndexer) -> dict:
    """Index HTML documents supplied by the given URL

    This will process the html document returned by the given url, as well as
    the html documents of any embedded hyperlinks up to one level deep.

    :param url: The root URL to use when retriving the xml documents
    :type url: str
    :param indexer: The indexer to use for indexing the documents
    :type indexer: :class:`levatas_indexer.indexer.WordIndexer`
    :return: A dictionary where the keys are words and the values are the
        number of occurence for the given word
    :rtype: dict
    """
    for document in utils.fetch_documents(url, set()):
        indexer.index_text(document)

    return indexer.index
