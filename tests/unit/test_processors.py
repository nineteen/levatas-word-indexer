from unittest.mock import Mock
import pytest

from levatas_indexer import processors


class TestStrimpXMLFromDoc:

    def test_xml_is_removed(self):
        doc = '<div class="content">Some Text</div>'

        result = processors.strip_xml_from_doc(doc)

        assert result == 'Some Text'

    def test_invalid_html(self):
        doc = '<div class="content">Some Text'
        result = processors.strip_xml_from_doc(doc)

        assert result == 'Some Text'

    def test_xml_is_replaced_by_whitespace(self):
        doc = '<div class="content">Some<strong>Text</strong></div>'
        result = processors.strip_xml_from_doc(doc)

        assert result == 'Some Text'


class TestCastTextToLower:

    @pytest.mark.parametrize('text,expected', [
        ('LDKSJlkfjslkdfakldsjLKJSD', 'ldksjlkfjslkdfakldsjlkjsd'),
        ('ŊŋŔŪ', 'ŋŋŕū'),
        ('asldkfjasldkf100', 'asldkfjasldkf100'),
        ('AAA100aaa200III', 'aaa100aaa200iii'),
        ('☀☁☈☋', '☀☁☈☋')
    ])
    def test_result_is_lower(self, text, expected):
        result = processors.cast_text_to_lower(text)

        assert result == expected


class TestRemoveNumericValues:
    @pytest.mark.parametrize('text,expected', [
        ('1', ''),
        ('9880083', ''),
        ('  123445', ''),
        ('1.0', ''),
        ('1.439054', ''),
        ('100,000', ''),
        ('123asdf34', '123asdf34')
    ])
    def test_result_is_not_numeric(self, text, expected):
        result = processors.remove_numeric_values(text)

        assert result == expected


class TestStripWhitespace:
    @pytest.mark.parametrize('text, expected', [
        ('     ', ''),
        ('\tsomething', 'something'),
        ('something\t', 'something'),
        ('\tsomething\t', 'something'),
        ('    test ', 'test')
    ])
    def test_leading_and_training_whitespace_is_removed(self, text, expected):
        result = processors.strip_whitespace(text)

        assert result == expected


class TestStemWord:
    def test_stem_method_is_called(self, monkeypatch):
        """This processor method uses the NLTK porter stemmer. Testing the
        functionality of this stemmer is beyond the scope of this project.
        Instead we will simple assert that the stemer is called.
        """
        mock_stem = Mock()
        monkeypatch.setattr(processors.PORTER_STEMMER, 'stem', mock_stem)

        mock_stem.assert_not_called()
        processors.stem_word('programming')
        mock_stem.assert_called()
