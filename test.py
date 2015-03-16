# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
import bow
from bow import BagOfWords, TextFilters, WordFilters, Tokenizer, SimpleTokenizer, DefaultTokenizer, DocumentClass, DefaultDocumentClass, DefaultDocument, SimpleDocument
import mock

class BagOfWordsTest(TestCase):

    def setUp(self):
        self.bow = BagOfWords()

    def test_add_one_word(self):
        self.bow.add('David')
        self.bow.add({'David':2})
        self.assertEqual(self.bow.words(), ['David'])
        self.assertEqual(len(self.bow), 1)
        self.assertEqual(self.bow.num(), 3)
        self.assertEqual(self.bow.freq('David'), 3)
        self.assertEqual(dict(self.bow), {'David':3})

    def test_add_two_words(self):
        self.bow.add(u'David', [u'David',u'Álex'])
        self.assertEqual(self.bow.words(), [u'Álex', u'David'])
        self.assertEqual(len(self.bow), 2)
        self.assertEqual(self.bow.num(), 3)
        self.assertEqual(self.bow.freq('David'), 2)
        self.assertEqual(dict(self.bow), {u'Álex':1, 'David':2})

    def test_del_one_word(self):
        self.bow.delete('David')
        self.assertEqual(dict(self.bow), {})
        #
        self.bow.add('David')
        self.bow.delete('David')
        self.assertEqual(dict(self.bow), {})
        #
        self.bow.add('David', 'David')
        self.bow.delete('David')
        self.assertEqual(self.bow.words(), ['David'])
        self.assertEqual(len(self.bow), 1)
        self.assertEqual(self.bow.num(), 1)
        self.assertEqual(self.bow.freq('David'), 1)
        self.assertEqual(dict(self.bow), {'David':1})

    def test_del_two_word(self):
        self.bow.delete('David', u'Álex')
        self.assertEqual(dict(self.bow), {})
        #
        self.bow.add('David', u'Álex')
        self.bow.delete('David', u'Álex')
        self.assertEqual(dict(self.bow), {})
        #
        self.bow.add({'David':2})
        self.bow.delete('David')
        self.bow.add(u'Álex')
        self.assertEqual(self.bow.words(), [u'Álex', 'David'])
        self.assertEqual(len(self.bow), 2)
        self.assertEqual(self.bow.num(), 2)
        self.assertEqual(self.bow.freq('David'), 1)
        self.assertEqual(dict(self.bow), {u'Álex':1, 'David':1})

    def test_join_add(self):
        a = BagOfWords('car', 'chair', 'chicken')
        b = BagOfWords({'chicken':2}, ['eye', 'ugly'])
        c = BagOfWords('plane')
        self.assertEqual(dict(a + b + c), {'car': 1, 'chair': 1, 'eye': 1, 'chicken': 3, 'plane': 1, 'ugly': 1})
        self.assertEqual(dict(c + b + a), {'car': 1, 'chair': 1, 'eye': 1, 'chicken': 3, 'plane': 1, 'ugly': 1})
        self.assertEqual(dict(b + c + a), {'car': 1, 'chair': 1, 'eye': 1, 'chicken': 3, 'plane': 1, 'ugly': 1})
        #
        total = a + b + c
        total = 'ugly' + total
        self.assertEqual(dict(total), {'car': 1, 'chair': 1, 'eye': 1, 'chicken': 3, 'plane': 1, 'ugly': 2})
        #
        total = a + b + c
        total = 'ugly' + total
        total = total + 'plane'
        self.assertEqual(dict(total), {'car': 1, 'chair': 1, 'eye': 1, 'chicken': 3, 'plane': 2, 'ugly': 2})
        #
        total = a + b + c
        total = total + ['car', 'chair', 'chicken'] + ['chicken', 'chicken', 'eye']
        self.assertEqual(dict(total), {'car': 2, 'chair': 2, 'eye': 2, 'chicken': 6, 'plane': 1, 'ugly': 1})

    def test_join_sub(self):
        a = BagOfWords('car', 'chair', 'chicken')
        b = BagOfWords({'chicken':2}, ['eye', 'ugly'])
        c = BagOfWords('plane')
        self.assertEqual(dict(a - b - c), {'car': 1, 'chair': 1})
        self.assertEqual(dict(c - b - a), {'plane': 1})
        self.assertEqual(dict(b - c - a), {'chicken':1, 'eye':1, 'ugly':1})
        #
        total = b - c - a
        total = 'eye' - total
        self.assertEqual(dict(total), {'chicken':1, 'ugly':1})
        #
        total = b - c - a
        total = 'eye' - total
        total = total - 'eye'
        self.assertEqual(dict(total), {'chicken':1, 'ugly':1})
        #
        total = b - c - a
        total = total - ['chicken', 'ugly']
        self.assertEqual(dict(total), {'eye':1})

    def test_clear(self):
        self.bow.add('item', 'item')
        self.bow.clear()
        self.assertEqual(len(self.bow), 0)
        self.assertEqual(self.bow.num(), 0)
        self.assertEqual(self.bow.freq('item'), 0)
        self.assertEqual(dict(self.bow), {})

    def test_item(self):
        self.bow.add('item1', 'item2', 'item2', 'item3')
        self.assertEqual(self.bow['item2'], 2)
        self.assertEqual(self.bow['item3'], 1)
        self.assertEqual(self.bow['item1'], 1)

    def test_copy(self):
        a = BagOfWords('car', 'chair', 'chicken')
        b = a.copy()
        self.assertEqual(a == b, True)

    def test_del(self):
        self.bow.add(['car', 'chair', 'chicken'])
        del self.bow['car']
        self.assertEqual(dict(self.bow), {'chair':1, 'chicken':1})

    def test_cmp(self):
        a = BagOfWords('car', 'chair', 'chicken')
        b = BagOfWords('car', 'chair', 'chicken')
        self.assertEqual(a == b, True)
        #
        a.add('car')
        self.assertEqual(a == b, False)

    def test_has_key(self):
        self.bow.add('car', 'chair', 'chicken')
        self.assertEqual(self.bow.has_key('car'), True)
        self.assertEqual('car' in self.bow, True)

    def test_rate(self):
        self.bow.add(['b','a','a','a'])
        self.assertEqual(self.bow.rates, {'a':0.75, 'b':0.25})
        self.assertEqual(self.bow.sorted_rates, [('a', 0.75), ('b', 0.25)])  
        self.assertEqual(self.bow.rate('a'), 0.75)
        self.assertEqual(self.bow.rate('b'), 0.25)
        self.assertEqual(self.bow.rate('c'), 0)
        #
        self.bow.clear()
        self.assertEqual(self.bow.rate('a'), 0)


class TokenizerTest(TestCase):

    def test_default_tokenizer(self):
        tokens = DefaultTokenizer()
        words = tokens('How do you convert a tuple to a list?');
        self.assertEqual(words, [u'convert', u'tupl', u'list'])
        #
        words = tokens.tokenizer('How do you convert a tuple to a list?');
        self.assertEqual(words, [u'convert', u'tupl', u'list'])
        #
        tokens = DefaultTokenizer(stemming=0)
        words = tokens('How do you convert a tuple to a list?');
        self.assertEqual(words, [u'convert', u'tuple', u'list'])
        #
        tokens = DefaultTokenizer(lang='', stemming=0)
        words = tokens('How do you convert a tuple to a list?');
        self.assertEqual(words, [u'how', u'do', u'you', u'convert', u'a', u'tuple', u'to', u'a', u'list'])
        #
        tokens = DefaultTokenizer(lang='spanish')
        words = tokens(u'Cómo convertir una tupla a lista?');
        self.assertEqual(words, [u'com', u'convert', u'tupl', u'list'])
        #
        tokens = DefaultTokenizer(lang='spanish', stemming=0)
        words = tokens(u'Cómo convertir una tupla a lista?');
        self.assertEqual(words, [u'como', u'convertir', u'tupla', u'lista'])
        #
        tokens = DefaultTokenizer(lang='', stemming=0)
        words = tokens(u'Cómo convertir una tupla a lista?');
        self.assertEqual(words, [u'como', u'convertir', u'una', u'tupla', u'a', u'lista'])

    def test_simple_tokenizer(self):
        tokens = SimpleTokenizer()
        words = tokens('How, do you convert - a tuple to a list?');
        self.assertEqual(words, [u'how', u'do', u'you', u'convert', u'a', u'tuple', u'to', u'a', u'list'])

    def test_tokenizer(self):

        class _MyTokenizer(Tokenizer):

            def __init__(self):
                 Tokenizer.__init__(self)

            def before_tokenizer(self, textfilters, text):
                text = textfilters.upper(text)
                return text

            def after_tokenizer(self, wordfilters, words):
                words = wordfilters.normalize(words)
                return words
        tokens = _MyTokenizer()
        words = tokens('How, do you convert - a tuple to a list?');
        self.assertEqual(words, [u'HOW,', u'DO', u'YOU', u'CONVERT', u'-', u'A', u'TUPLE', u'TO', u'A', u'LIST?'])
        #
        class _MyTokenizer(Tokenizer):

            def __init__(self):
                 Tokenizer.__init__(self)

            def before_tokenizer(self, textfilters, text):
                text = textfilters.html_to_text(text)
                text = textfilters.invalid_chars(text)
                text = textfilters.lower(text)
                return text

            def after_tokenizer(self, wordfilters, words):
                words = wordfilters.stopwords('english', words)
                words = wordfilters.normalize(words)
                return words
        tokens = _MyTokenizer()
        text = '''
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html>
                    <body>
                        <!--my comment -->
                        <script>my script</script>
                        <SCRIPT>another script</script>
                        <style>my style</style>
                        <h3>my project!!</h3> <br>
                        <b>Description</b>:<br/>
                        This small script is intended to allow conversion from HTML markup to plain text.
                    </body>
                </html>
                '''
        words = tokens(text)
        self.assertEqual(words, [u'project', u'description', u'small', u'script', u'intended', u'allow', u'conversion',
                                 u'html', u'markup', u'plain', u'text'])


class DocumentClassTest(TestCase):

    def test_default_document_class(self):
        dclass = DefaultDocumentClass()
        dclass('hello a beautiful world!', 'text one')
        dclass('hello the Moon!', 'text two')
        dclass('hello the world!', 'text one')
        self.assertEqual(dclass.docs, {'text two': {u'hello': 1, u'moon': 1}, 'text one': {u'world': 1, u'hello': 1}})
        self.assertEqual(dclass, {u'world': 1, u'hello': 2, u'moon': 1})
        self.assertEqual(dclass.numdocs, 2)

    def test_default_document(self):
        dclass = DefaultDocument()
        dclass('hello a beautiful world!')
        dclass('hello the Moon!')
        dclass('hello the world!')
        self.assertEqual(dclass, {u'world': 2, u'hello': 3, u'beauti': 1, u'moon': 1})
        self.assertEqual(dclass.numdocs, 3)

    def test_json(self):
        dclass = DefaultDocumentClass(lang='spanish')
        dclass.read_text('Hola mundo!', id_='1')
        dclass.read_text('Este es un bonito mundo', id_='2')
        json_ = dclass.to_json()
        dclass = DocumentClass.from_json(json_)
        self.assertEqual(dclass.__class__.__name__ , 'DefaultDocumentClass')
        self.assertEqual(dclass.docs, {u'2': {u'mund': 1, u'bonit': 1}, u'1': {u'mund': 1, u'hol': 1}})
        self.assertEqual(dclass, {u'mund': 2, u'hol': 1, u'bonit': 1})
        self.assertEqual(dclass.numdocs, 2)
        self.assertEqual(dclass.lang, 'spanish')
        self.assertEqual(dclass.stemming, 1)

class DocumentClassifierTest(TestCase):

    def test_simple(self):
        docnumbers = bow.SimpleDocument()
        docnumbers('one two three four')
        docnumbers('five six seven')
        docanimals = bow.SimpleDocument()
        docanimals('dog cat')
        docanimals('horse frog')
        docanimals('dog cat')
        docanimals('dog cat')
        docanimals('dog cat')
        docvehicles = bow.SimpleDocument()
        docvehicles('truck car')
        doc = bow.SimpleDocument()
        doc('I am a cat')
        result = bow.document_classifier(doc, numbers=docnumbers, animals=docanimals, vehicles=docvehicles)
        self.assertEqual(result, [('animals', 0.6785714285714286), ('numbers', 0.25), ('vehicles', 0.07142857142857142)])
        doc.clear()
        doc('one dog, one cat, three trucks')
        result = bow.document_classifier(doc, numbers=docnumbers, animals=docanimals, vehicles=docvehicles)
        self.assertEqual(result, [('numbers', 0.7302518458581976), ('animals', 0.2555881460503691), ('vehicles', 0.014160008091433189)])

    def test_save_document(self):
        m = mock.mock_open()
        with mock.patch('bow.open', m, create=True): 
            docnumbers = bow.SimpleDocument()
            docnumbers('one two three four')
            docnumbers('one two three')
            docnumbers.save('test.dat')
        #print m.mock_calls
        m.assert_called_once_with('test.dat','w')
        handle = m()
        data = '{"__module__": "bow", "numdocs": 2, "__class__": "SimpleDocument", "_bow": {"four": 1, "three": 2, "two": 2, "one": 2}}'
        handle.write.assert_called_once_with(data)

    def test_load_document(self):
        m = mock.mock_open()
        data = '{"__module__": "bow", "numdocs": 2, "__class__": "SimpleDocument", "_bow": {"four": 1, "three": 2, "two": 2, "one": 2}}'
        with mock.patch('bow.open', mock.mock_open(read_data=data), create=True) as m:
            docnumbers = SimpleDocument.load('test.dat')
        m.assert_called_once_with('test.dat','r')
        self.assertEqual(docnumbers, {u'four': 1, u'one': 2, u'three': 2, u'two': 2})
        
       
if __name__ == '__main__':
    unittest.main()
