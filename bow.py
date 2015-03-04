# -*- coding: utf-8 -*-
__author__ = 'dmiro'
import os
import copy
import urllib2
import inspect
import unicodedata
from HTMLParser import HTMLParser
from zipfile import ZipFile
from json import JSONEncoder, JSONDecoder
import json

class BagOfWords(object):

    def __init__(self, *args):
        self._bow = {}
        self.add(*args)

    def __calc(self, operation, *args):
        for words in args:
            if isinstance(words, basestring):
                words = [words]
            for word in words:
                n = 1
                if isinstance(words, dict):
                    n = words[word]
                self._bow[word] = operation(self._bow.get(word, 0), n)
                if self._bow[word] < 1:
                    del self._bow[word]

    def add(self, *args):
        """Add set of word, word list or word dict to bag of words
        :param args: set of word or word list to add
        :return:nothing"""
        self.__calc(lambda x,y: x+y, *args)

    def delete(self, *args):
        """Delete set of word, word list or word dict to bag of words
        :param args: set of word or word list to add
        :return:nothing"""
        self.__calc(lambda x,y: x-y, *args)

    def rates(self):
        """Rate of occurrences"""
        total = float(self.num())
        if total:
            return {k:v/total for k, v in self._bow.iteritems()}
        else:
            return {}

    def freq(self, word):
        """Frequency of a word
        :param word: word to query
        :return: frequency"""
        if word in self._bow:
            return self._bow[word]
        else:
            return 0

    def rate(self, word):
        """Rate of a word
        :param word: word to query
        :return: rate"""
        total = float(self.num())
        if total:
            return self.freq(word)/total
        else:
            return 0

    def __add__(self, other):
        """ Overloading of "+" operator to join BagOfWord+BagOfWord, BagOfWords+str or BagOfWords+list
        :param other: BagOfWords, str or list
        :return: BagOfWords"""
        result = self.copy()
        if isinstance(other, BagOfWords):
            result.add(dict(other))
        else:
            result.add(other)
        return result

    def __sub__(self, other):
        """ Overloading of "-" operator to join BagOfWord+BagOfWord, BagOfWords+str or BagOfWords+list
        :param other: BagOfWords, str or list
        :return: BagOfWords"""
        result = self.copy()
        if isinstance(other, BagOfWords):
            result.delete(dict(other))
        else:
            result.delete(other)
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __iter__(self):
        return self._bow.iteritems()

    def __getitem__(self, offset):
        return self._bow.__getitem__(offset)

    def __len__(self):
        return self._bow.__len__()

    def __repr__(self):
        return self._bow.__repr__()

    def __delitem__(self, key):
        del self._bow[key]

    def __cmp__(self, other):
        if isinstance(other, BagOfWords):
            return cmp(self._bow, other._bow)
        else:
            return cmp(self._bow, other)

    def copy(self):
        return copy.deepcopy(self)

    def clear(self):
        """Clear word list"""
        self._bow.clear()

    def iteritems(self):
        """Return an iterator over the word dictionary’s (word, frequency) pairs"""
        return self._bow.iteritems()

    def keys(self):
        """Word list contained in the object"""
        return self._bow.keys()

    def words(self):
        """Word list contained in the object"""
        return self.keys()

    def items(self):
        return self._bow.items()

    def values(self):
        return self._bow.values()

    def num(self):
        """Total number of words"""
        return sum(self._bow.values())

    def has_key(self, key):
        return self._bow.has_key(key)

    def __contains__(self, key):
        """Method key in y"""
        return self.has_key(key)

    def __call__(self, *args):
         self.add(self, *args)

    def to_json(self):
        """Convert dict to json string
        :param other: BagOfWords, str or list
        :return: BagOfWords"""
        return json.dumps(self._bow, indent=1)

    def from_json(self, data):
        """Load dict from json string
        :param data: json string
        :return: nothing"""
        self._bow = json.loads(data)


class TextFilters(object):

    @staticmethod
    def upper(text):
        """Convert text to uppercase"""
        return text.upper()

    @staticmethod
    def lower(text):
        """Convert text to lowercase"""
        return text.lower()

    @staticmethod
    def invalid_chars(text):
        """Remove invalid chars from a text"""
        INVALID_CHARS = u"/\¨º-~#@|¡!,·$%&()¿?'[^""`]+}{><;,:.=*^_"
        return ''.join([char for char in text if char not in INVALID_CHARS])

    @staticmethod
    def html_to_text(text):
        """Conversion from HTML markup to plain text"""
        class _HTMLParser(HTMLParser):

            def __init__(self):
                HTMLParser.__init__(self)
                self.text = []

            def handle_data(self, data):
                append = True
                text = data.split()
                if text:
                    tag = self.get_starttag_text()
                    if tag:
                        tag = tag.lower()
                        append = not tag.startswith(('<script','<style'))
                    if append:
                        self.text.extend(text)
        parser = _HTMLParser()
        parser.feed(text)
        return ' '.join(parser.text)


class WordFilters(object):

    @staticmethod
    def stemming(lang, stemming, words):
        """Lemmatize text
        :param lang: lang text to lemmatize
        :param stemming: number loops of lemmatizing"""
        import Stemmer as stemmer
        try:
            stemmer = stemmer.Stemmer(lang)
            for i in range(stemming):
                words = stemmer.stemWords(words)
            return words
        except KeyError:
            return words

    @staticmethod
    def stopwords(lang, words):
        """Remove stop words from a text
        :param lang: language text where remove empty words"""
        import stop_words
        try:
            stopwords = stop_words.get_stop_words(lang)
            return [word for word in words if word not in stopwords]
        except stop_words.StopWordError:
            return words

    @staticmethod
    def normalize(words):
        """Normalize chars from a text"""
        return [''.join((char for char in unicodedata.normalize('NFD', unicode(word)) if unicodedata.category(char) != 'Mn'))
                for word in words]


class Tokenizer(object):

    def __init__(self):
        object.__init__(self)

    def before_tokenizer(self, textfilters, text):
        """function to call before tokenizer text
        :param textfilters: static class with helper methods to filter text
        :param text: The text will be split"""
        return text

    def after_tokenizer(self, wordfilters, words):
        """function to call after tokenizer text
        :param wordfilters: static class with helper methods to filter words
        :param words: split words"""
        return words

    def tokenizer(self, text):
        """tokenize a text
        :param text: text to tokenizer"""
        text = self.before_tokenizer(TextFilters, text)
        words = text.split()
        words = self.after_tokenizer(WordFilters, words)
        return words

    def __call__(self, text):
        return self.tokenizer(text)


class DocumentClass(Tokenizer):

    def __init__(self, category):
        Tokenizer.__init__(self)
        self._category = category
        self._docs = {}
        self._total = BagOfWords()

    def read_text(self, id, text):
        """The text is stored in a BagOfWords identified by id
        :param id: BagOfWord identifier
        :param text: text to add a BagOfWords
        :return: BagOfWords"""
        words = self.tokenizer(text)
        if id in self._docs:
            self._total -= self._docs[id]
        self._docs[id] = BagOfWords(words)
        self._total.add(words)
        return self._docs[id]

    def read_files(self, *filenames):
        """The contents of each file or files is stored in a BagOfWord identified by the filename
        :param *filenames: filenames to add
        :return: BagOfWord dict"""
        docs = {}
        for filename in filenames:
            text = open(filename, 'r').read()
            text = text.decode('utf-8')
            docs[filename] = self.read_text(filename, text)
        return docs

    def read_dir(self, path):
        """The contents of each file o files of a directory is stored in a BagOfWord identified by the filename
        :param path: directoy path to add files
        :return: BagOfWord dict"""
        fn = []
        for (_, _, filenames) in os.walk(path):
            fn.extend([os.path.join(path,f) for f in filenames])
            break
        return self.read_files(*fn)

    def read_urls(self, *urls):
        """The contents of each url or urls is stored in a BagOfWord identified by the url
        :param *urls: urls to add
        :return: BagOfWord dict"""
        docs = {}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20140129 Firefox/24.0'}
        for url in urls:
            req = urllib2.Request(url=url, headers=headers)
            text = urllib2.urlopen(req).read()
            text = text.decode('utf-8')
            docs[url] = self.read_text(url, text)
        return docs

    def read_zips(self, *zipfilenames):
        """The contents of each file o files of a zip file is stored in a BagOfWord identified by the filename
        :param *zipfilenames: zip files to add
        :return: BagOfWord dict"""
        docs = {}
        for zipfilename in zipfilenames:
            input_zip = ZipFile(zipfilename)
            for input_file in input_zip.infolist():
                if input_file.file_size > 0:
                    text = input_zip.read(input_file)
                    text = text.decode('utf-8')
                    docs[input_file.filename] = self.read_text(input_file.filename, text)
        return docs

    def __call__(self, id, text):
        return self.read_text(id, text)

    def docs(self):
        return self._docs

    def total(self):
        return self._total

    def category(self):
        return self._category

    def to_json(self):
        class _Encoder(JSONEncoder):

            def default(self, obj):
                if isinstance(obj, DocumentClass) or \
                   isinstance(obj, BagOfWords):
                    d = {'__class__': obj.__class__.__name__,
                         '__module__':obj.__module__}
                    d.update(obj.__dict__)
                    return d
                if not inspect.isfunction(obj):
                    return super(_Encoder, self).default(obj)

        return _Encoder().encode(self)

    def from_json(self, json_):
        class _Decoder(JSONDecoder):

            def __init__(self):
                JSONDecoder.__init__(self, object_hook = self.dict_to_object)

            def dict_to_object(self, d):
                if '__class__' in d:
                    class_name = d.pop('__class__')
                    module_name = d.pop('__module__')
                    module = __import__(module_name)
                    class_ = getattr(module, class_name)
                    if issubclass(class_, DocumentClass):
                        obj = class_(d.pop('_category'))
                    elif issubclass(class_, BagOfWords):
                        obj = class_(d.pop('_bow'))
                    else:
                        obj = class_()
                    for k, v in d.iteritems():
                        setattr(obj, k, v)
                    return obj
                return d

        return _Decoder().decode(json_)


class DefaultTokenizer(Tokenizer):

    def __init__(self, lang='english', stemming=1):
         Tokenizer.__init__(self)
         self._lang = lang
         self._stemming = stemming

    def before_tokenizer(self, textfilters, text):
        text = textfilters.lower(text)
        text = textfilters.invalid_chars(text)
        return text

    def after_tokenizer(self, wordfilters, words):
        words = wordfilters.stopwords(self._lang, words)
        words = wordfilters.stemming(self._lang, self._stemming, words)
        words = wordfilters.normalize(words)
        return words

class SimpleTokenizer(Tokenizer):

    def __init__(self):
         Tokenizer.__init__(self)

    def before_tokenizer(self, textfilters, text):
        text = textfilters.lower(text)
        text = textfilters.invalid_chars(text)
        return text

    def after_tokenizer(self, wordfilters, words):
        words = wordfilters.normalize(words)
        return words


class DefaultDocumentClass(DocumentClass, DefaultTokenizer):

    def __init__(self, category, lang='english', stemming=1):
        DocumentClass.__init__(self, category)
        DefaultTokenizer.__init__(self, lang, stemming)


class SimpleDocumentClass(DocumentClass, SimpleTokenizer):

    def __init__(self, category):
        DocumentClass.__init__(self, category)
        SimpleTokenizer.__init__(self)
