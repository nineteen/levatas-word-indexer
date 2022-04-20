from unittest.mock import Mock

import pytest

from levatas_indexer import indexer


class TestTokenizer:
    @pytest.fixture(scope='function')
    def tokenizer(self):
        return indexer.Tokenizer()

    def test_add_word_processor_adds_processor(self, tokenizer):
        mock = Mock()

        assert tokenizer._processors == {'word': [], 'document': []}

        tokenizer.add_word_processor(mock)

        assert tokenizer._processors == {'word': [mock], 'document': []}

    def test_add_word_processor_maintains_order(self, tokenizer):
        mock1 = Mock()
        mock2 = Mock()

        assert tokenizer._processors['word'] == []

        tokenizer.add_word_processor(mock1)
        tokenizer.add_word_processor(mock2)

        assert tokenizer._processors['word'] == [mock1, mock2]

    def test_add_document_processor_adds_processor(self, tokenizer):
        mock = Mock()

        assert tokenizer._processors == {'word': [], 'document': []}

        tokenizer.add_document_processor(mock)

        assert tokenizer._processors == {'word': [], 'document': [mock]}

    def test_add_document_processor_maintains_order(self, tokenizer):
        mock1 = Mock()
        mock2 = Mock()

        assert tokenizer._processors['document'] == []

        tokenizer.add_document_processor(mock1)
        tokenizer.add_document_processor(mock2)

        assert tokenizer._processors['document'] == [mock1, mock2]

    def test__process_calls_the_correct_processors(self, tokenizer):
        mock_word = Mock()
        mock_document = Mock()

        tokenizer.add_word_processor(mock_word)
        tokenizer.add_document_processor(mock_document)

        mock_word.assert_not_called()
        mock_document.assert_not_called()

        tokenizer._process('word', '')

        mock_word.assert_called()
        mock_document.assert_not_called()

    def test_tokenize_calls_processors(self, tokenizer):
        mock_word = Mock(return_values=['A', 'nice', 'clean', 'document'])
        mock_document = Mock(return_value='A nice clean document')

        tokenizer.add_word_processor(mock_word)
        tokenizer.add_document_processor(mock_document)

        mock_word.assert_not_called()
        mock_document.assert_not_called()

        tokenizer.tokenize('')

        mock_word.assert_called()
        mock_document.assert_called()

    def test_tokenize_splits_on_delimiter(self, tokenizer):
        result = tokenizer.tokenize('one  two three four\tfive')

        assert result == ['one', 'two', 'three', 'four\tfive']


class TestNLTKTokenizer:
    @pytest.fixture(scope='function')
    def nltk_tokenizer(self):
        return indexer.NLTKTokenizer()

    def test_it_calls_the_nltk_word_tokenize(self,
                                              nltk_tokenizer,
                                              monkeypatch):
        mock = Mock(return_value=[])
        monkeypatch.setattr('nltk.word_tokenize', mock)

        mock.assert_not_called()

        nltk_tokenizer.tokenize('')

        mock.assert_called()

    def test_tokenize_calls_processors(self, nltk_tokenizer):
        mock_word = Mock(return_values=['A', 'nice', 'clean', 'document'])
        mock_document = Mock(return_value='A nice clean document')

        nltk_tokenizer.add_word_processor(mock_word)
        nltk_tokenizer.add_document_processor(mock_document)

        mock_word.assert_not_called()
        mock_document.assert_not_called()

        nltk_tokenizer.tokenize('')

        mock_word.assert_called()
        mock_document.assert_called()


class TestWordIndexer:

    @pytest.fixture(scope='function')
    def word_indexer(self):
        return indexer.WordIndexer(Mock())

    def test_index_property_returns_copy(self, word_indexer):
        index = word_indexer.index
        index['testing'] = 'asldkfjasdl'

        assert 'testing' not in word_indexer._words

    def test_index_text_counts_words(self, word_indexer):
        words = ['one', 'two', 'two', 'three', 'four', 'two', 'three']
        word_indexer.tokenizer.tokenize = Mock(return_value=words)
        word_indexer.index_text('')

        index = word_indexer.index

        assert index['one'] == 1
        assert index['two'] == 3
        assert index['three'] == 2
        assert index['four'] == 1
        assert 'five' not in index

    def test_index_text_persists_across_calls(self, word_indexer):
        words = ['one', 'two', 'two', 'three', 'four', 'two', 'three']
        word_indexer.tokenizer.tokenize = Mock(return_value=words)
        word_indexer.index_text('')
        word_indexer.index_text('')

        index = word_indexer.index

        assert index['one'] == 2
        assert index['two'] == 6
        assert index['three'] == 4
        assert index['four'] == 2
        assert 'five' not in index

    def test_count_returns_correct_count(self, word_indexer):
        word_indexer._words['one'] = 99
        word_indexer._words['two'] = 35

        assert word_indexer.count('one') == 99
        assert word_indexer.count('two') == 35
        assert word_indexer.count('three') == 0
