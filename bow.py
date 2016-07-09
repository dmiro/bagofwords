# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from six import text_type as str
from six import text_type as str
from six.moves import urllib
from six.moves.html_parser import HTMLParser
from zipfile import ZipFile
from json import JSONEncoder, JSONDecoder

import os
import copy
import uuid
import math
import inspect
import argparse
import unicodedata

__author__ = 'dmiro'
__version_info__ = (1, 0, 3)
__version__ = '.'.join(str(v) for v in __version_info__)



class BagOfWords(object):
    """Implementing a bag of words with their frequency of usages"""

    def __init__(self, *args):
        self._bow = {}
        self.add(*args)

    def __calc(self, operation, *args):
        for words in args:
            if isinstance(words, str):
                words = [words]
            for word in words:
                n = 1
                if isinstance(words, dict):
                    n = words[word]
                self._bow[word] = operation(self._bow.get(word, 0), n)
                if self._bow[word] < 1:
                    del self._bow[word]

    def add(self, *args):
        """Add set of word, word list or word dict to bag of words.
        :param args: set of word or word list to add
        :return:nothing
        """
        self.__calc(lambda x,y: x+y, *args)

    def delete(self, *args):
        """Delete set of word, word list or word dict to bag of words.
        :param args: set of word or word list to add
        :return:nothing
        """
        self.__calc(lambda x,y: x-y, *args)

    @property
    def rates(self):
        """Rate of occurrences
        :return: Dict
        """
        total = float(self.num())
        if total:
            return {k:v/total for k, v in list(self._bow.items())}
        else:
            return {}

    @property
    def sorted_rates(self):
        """Sorted rate of occurrences
        :return: list sorted from greater to lowest rate
        """
        total = float(self.num())
        if total:
            res = [(k,v/total) for k, v in list(self._bow.items())]
            return sorted(res, key=lambda t: t[1], reverse=True)
        else:
            return []

    def freq(self, word):
        """Frequency of a word.
        :param word: word to query
        :return: frequency
        """
        if word in self._bow:
            return self._bow[word]
        else:
            return 0

    def rate(self, word):
        """Rate of a word.
        :param word: word to query
        :return: rate
        """
        total = float(self.num())
        if total:
            return self.freq(word)/total
        else:
            return 0

    def __add__(self, other):
        """ Overloading of "+" operator to join BagOfWord+BagOfWord, BagOfWords+str or
        BagOfWords+list.
        :param other: BagOfWords, str or list
        :return: BagOfWords
        """
        result = self.copy()
        if isinstance(other, BagOfWords):
            result.add(dict(other))
        else:
            result.add(other)
        return result

    def __sub__(self, other):
        """ Overloading of "-" operator to join BagOfWord+BagOfWord, BagOfWords+str or
        BagOfWords+list.
        :param other: BagOfWords, str or list
        :return: BagOfWords
        """
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
        return list(self._bow.items())

    def __getitem__(self, offset):
        return self._bow.__getitem__(offset)

    def __len__(self):
        return self._bow.__len__()

    def __repr__(self):
        return self._bow.__repr__()

    def __delitem__(self, key):
        del self._bow[key]

    def __eq__(self, other):
        if isinstance(other, BagOfWords):
            return self._bow == other._bow
        else:
            return self._bow == other

    def __ne__(self, other):
        if isinstance(other, BagOfWords):
            return self._bow !=other._bow
        else:
            return self._bow != other


    def copy(self):
        return copy.deepcopy(self)

    def clear(self):
        """Clear word list."""
        self._bow.clear()

    def items(self):
        """Return an iterator over the word dictionary’s (word, frequency) pairs."""
        return list(self._bow.items())

    def keys(self):
        """Word list contained in the object."""
        return list(self._bow.keys())

    def words(self):
        """Word list contained in the object."""
        return list(self.keys())

    def items(self):
        return list(self._bow.items())

    def values(self):
        return list(self._bow.values())

    def num(self):
        """Total number of words."""
        return sum(self._bow.values())

    def __contains__(self, key):
        """Method key in y"""
        return key in self._bow

    def __call__(self, *args):
         self.add(self, *args)


class TextFilters(object):
    """Filters for transforming a text"""

    @staticmethod
    def upper(text):
        """Convert text to uppercase."""
        return text.upper()

    @staticmethod
    def lower(text):
        """Convert text to lowercase."""
        return text.lower()

    @staticmethod
    def invalid_chars(text):
        """Remove invalid chars from a text."""
        INVALID_CHARS = "/\¨º-~#@|¡!,·$%&()¿?'[^""`]+}{><;,:.=*^_"
        return ''.join([char for char in text if char not in INVALID_CHARS])

    @staticmethod
    def html_to_text(text):
        """Conversion from HTML markup to plain text."""
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
    """Filters for transforming a set of words"""

    @staticmethod
    def stemming(lang, stemming, words):
        """Lemmatize text.
        :param lang: lang text to lemmatize
        :param stemming: number loops of lemmatizing
        """
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
        """Remove stop words from a text.
        :param lang: language text where remove empty words
        """
        import stop_words
        try:
            stopwords = stop_words.get_stop_words(lang)
            return [word for word in words if word not in stopwords]
        except stop_words.StopWordError:
            return words

    @staticmethod
    def normalize(words):
        """Normalize chars from a text."""
        return [''.join((char for char in unicodedata.normalize('NFD', str(word)) if unicodedata.category(char) != 'Mn'))
                for word in words]


class Tokenizer(object):
    """Allows to break a string into tokens (set of words). Optionally allows you to set
    filters before (TextFilters) and after (WordFilters) breaking the string into tokens.
    """

    def __init__(self):
        object.__init__(self)

    def before_tokenizer(self, textfilters, text):
        """function to call before tokenizer text.
        :param textfilters: static class with helper methods to filter text
        :param text: The text will be split
        """
        return text

    def after_tokenizer(self, wordfilters, words):
        """function to call after tokenizer text.
        :param wordfilters: static class with helper methods to filter words
        :param words: split words
        """
        return words

    def tokenizer(self, text):
        """tokenize a text.
        :param text: text to tokenizer
        """
        text = self.before_tokenizer(TextFilters, text)
        words = text.split()
        words = self.after_tokenizer(WordFilters, words)
        return words

    def __call__(self, text):
        return self.tokenizer(text)


class Document(BagOfWords, Tokenizer):
    """Implementing a bag of words where all words are of the same category. Retrieves
    the text of a file, folder, url or zip, and also allows save or retrieve the Document
    in json format.
    """

    def __init__(self):
        Tokenizer.__init__(self)
        BagOfWords.__init__(self)
        self.numdocs = 0

    def _read(self, id_, text):
        self.numdocs += 1
        words = self.tokenizer(text)
        self.add(words)

    def clear(self):
        """Clear word list."""
        BagOfWords.clear(self)
        self.numdocs = 0

    def read_text(self, text):
        """The text is stored in a BagOfWords identified by Id.
        :param text: text to add a BagOfWords
        :return: nothing
        """
        self._read(None, text)

    def read_files(self, *filenames):
        """The contents of each file or files is stored in a BagOfWord identified by the
        filename.
        :param *filenames: filenames to add
        :return: nothing
        """
        for filename in filenames:
            text = open(filename, 'r').read()
            self._read(filename, text)

    def read_dir(self, *paths):
        """The contents of each file o files of a directory is stored in a BagOfWord
        identified by the filename.
        :param paths: directory or directories path to add files
        :return: nothing
        """
        for path in paths:
            fn = []
            for (_, _, filenames) in os.walk(path):
                fn.extend([os.path.join(path,f) for f in filenames])
                break
            self.read_files(*fn)

    def read_urls(self, *urls):
        """The contents of each url or urls is stored in a BagOfWord identified by the url.
        :param *urls: urls to add
        :return: nothing
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20140129 Firefox/24.0'}
        for url in urls:
            req = urllib.Request(url=url, headers=headers)
            text = urllib.request.urlopen(req).read()
            self._read(url, text)

    def read_zips(self, *zipfilenames):
        """The contents of each file o files of a zip file is stored in a BagOfWord
        identified by the filename.
        :param *zipfilenames: zip files to add
        :return: nothing
        """
        for zipfilename in zipfilenames:
            input_zip = ZipFile(zipfilename)
            for input_file in input_zip.infolist():
                if input_file.file_size > 0:
                    text = input_zip.read(input_file)
                    self._read(input_file.filename, text)

    def to_json(self):
        """Convert Document object to json string.
        :return: json string
        """
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

    @staticmethod
    def from_json(json_):
        """Convert json string to Document object.
        :param json_: json string
        :return: Document object
        """
        class _Decoder(JSONDecoder):

            def __init__(self):
                JSONDecoder.__init__(self, object_hook=self.dict_to_object)

            def dict_to_object(self, d):
                if '__class__' in d:
                    class_name = d.pop('__class__')
                    module_name = d.pop('__module__')
                    module = __import__(module_name)
                    class_ = getattr(module, class_name)
##                    if issubclass(class_, BagOfWords):
##                        obj = class_(d.pop('_bow'))
##                    else:
##                        obj = class_()
                    obj = class_()
                    for k, v in list(d.items()):
                        setattr(obj, k, v)
                    return obj
                return d

        return _Decoder().decode(json_)

    def save(self, filename):
        """Serialize Documentand save to a file in json format
        :filename: file to save
        :return: nothing
        """
        with open(filename, 'w') as f:
            json_ = self.to_json()
            f.write(json_)

    @staticmethod
    def load(filename):
        """Load and deserialize Document from file saved in json format
        :filename: file to load
        :return: nothing
        """
        with open(filename, 'r') as f:
            json_ = f.read()
            return Document.from_json(json_)

    def __call__(self, text):
        self.read_text(text)


class DocumentClass(Document):
    """Implementing a bag of words collection where all the bags of words are the same
    category, as well as a bag of words with the entire collection of words. Each bag
    of words has an identifier otherwise it's assigned an calculated identifier.
    Retrieves the text of a file, folder, url or zip, and also allows save or retrieve
    the collection in json format.
    """

    def __init__(self):
        Document.__init__(self)
        self.docs = {}

    def _read(self, id_, text):
        words = self.tokenizer(text)
        bow = BagOfWords(words)
        if not id_:
            id_ = uuid.uuid4().hex
        if id_ in self.docs:
            self.delete(dict(self.docs[id_]))
        else:
            self.numdocs += 1
        self.docs[id_] = bow
        self.add(words)

    def clear(self):
        """Clear word and docs list."""
        Document.clear(self)
        self.docs = {}

    def read_text(self, text, id_=None):
        """The text is stored in a BagOfWords identified by Id.
        :param text: text to add a BagOfWords
        :param id_: BagOfWord identifier. Optional. If not set then it's set an UUID4
        identifier.
        :return: nothing
        """
        self._read(id_, text)

    def __call__(self, text, id_=None):
        self._read(id_, text)


class DefaultTokenizer(Tokenizer):
    """Tokenizer subclass that implements the text filters 'lower', 'invalid_chars'
    and the word filters 'stopwords', 'stemming' and 'normalize'.
    """

    def __init__(self, lang='english', stemming=1):
         Tokenizer.__init__(self)
         self.lang = lang
         self.stemming = stemming

    def before_tokenizer(self, textfilters, text):
        text = textfilters.lower(text)
        text = textfilters.invalid_chars(text)
        return text

    def after_tokenizer(self, wordfilters, words):
        words = wordfilters.stopwords(self.lang, words)
        words = wordfilters.stemming(self.lang, self.stemming, words)
        words = wordfilters.normalize(words)
        return words


class SimpleTokenizer(Tokenizer):
    """Tokenizer subclass that implements the text filters 'lower', 'invalid_chars'
    and the word filter 'normalize'.
    """

    def __init__(self):
         Tokenizer.__init__(self)

    def before_tokenizer(self, textfilters, text):
        text = textfilters.lower(text)
        text = textfilters.invalid_chars(text)
        return text

    def after_tokenizer(self, wordfilters, words):
        words = wordfilters.normalize(words)
        return words


class HtmlTokenizer(DefaultTokenizer):
    """Tokenizer subclass that implements the text filters 'htm_to_text', 'lower',
    'invalid_chars' and the word filter 'normalize'.
    """

    def __init__(self, lang='english', stemming=1):
         DefaultTokenizer.__init__(self, lang, stemming)

    def before_tokenizer(self, textfilters, text):
        text = textfilters.html_to_text(text)
        text = DefaultTokenizer.before_tokenizer(self, textfilters, text)
        return text


class DefaultDocument(Document, DefaultTokenizer):
    """DefaultTokenizer and Document subclass"""

    def __init__(self, lang='english', stemming=1):
        Document.__init__(self)
        DefaultTokenizer.__init__(self, lang, stemming)


class SimpleDocument(Document, SimpleTokenizer):
    """SimpleTokenizer and Document subclass"""

    def __init__(self):
        Document.__init__(self)
        SimpleTokenizer.__init__(self)


class HtmlDocument(Document, HtmlTokenizer):
    """HtmlTokenizer and Document subclass"""

    def __init__(self, lang='english', stemming=1):
        Document.__init__(self)
        HtmlTokenizer.__init__(self, lang, stemming)


class DefaultDocumentClass(DocumentClass, DefaultTokenizer):
    """DefaultTokenizer and DocumentClass subclass"""

    def __init__(self, lang='english', stemming=1):
        DocumentClass.__init__(self)
        DefaultTokenizer.__init__(self, lang, stemming)


class SimpleDocumentClass(DocumentClass, SimpleTokenizer):
    """SimpleTokenizer and DocumentClass subclass"""

    def __init__(self):
        DocumentClass.__init__(self)
        SimpleTokenizer.__init__(self)


class HtmlDocumentClass(DocumentClass, HtmlTokenizer):
    """HtmlTokenizer and DocumentClass subclass"""

    def __init__(self, lang='english', stemming=1):
        DocumentClass.__init__(self)
        HtmlTokenizer.__init__(self, lang, stemming)


def document_classifier(document, **classifieds):
    """Text classification based on an implementation of Naive Bayes
    :param document: document class instance to classify.
    :param classifieds: dictionary with Document class instances have already been classified.
    :return: list sorted from highest to lowest probability.
    """
    # http://blog.yhathq.com/posts/naive-bayes-in-python.html
    res = {}
    total_docs = SimpleDocument()
    for classified in list(classifieds.values()):
        total_docs += classified
    for k_classified, classified in list(classifieds.items()):
        prior = float(classified.num()) / float(total_docs.num())
        log_prob = 0.0
        for word, value in list(document.items()):
            if word in total_docs:
                if classified.rate(word) > 0.0:
                    # log(probability) it requires fewer decimal places
                    log_prob += math.log(value * classified.rate(word) / total_docs.rate(word))
        # log space to regular space
        exp_prob = math.exp(log_prob + math.log(prior))
        res[k_classified] = exp_prob
    total = sum(res.values())
    res = [(k,v/total) for k, v in list(res.items())]
    return sorted(res, key=lambda t: t[1], reverse=True)


def _show_document(document, filename, verbose, top=50):
    print('* filename: %s' % filename)
    print('* filter:')
    print('    type: %s' % document.__class__.__name__)
    print('    lang: %s' % document.lang)
    print('    stemming: %s' % document.stemming)
    print('* total words: %d' % document.num())
    print('* total docs: %d' % document.numdocs)
    if verbose:
        if top:
            words = 'word (top %d)' % top
            rates = document.sorted_rates[0:top]
        else:
            words = 'word'
            rates = document.sorted_rates
        posadj = len(str(len(rates)))+1
        print('*','pos'.rjust(posadj),'|',words.ljust(35),'|','occurrence'.rjust(10),\
              '|','rate'.rjust(10))
        print(' ','-'*posadj,'|','-'*35,'|','-'*10,'|','-'*10)
        for word, rate in rates:
            print(' ',str(rates.index((word, rate))+1).rjust(posadj),'|',\
                  word.encode('utf-8').ljust(35),'|', str(document[word]).rjust(10),\
                  '|',('%.8f' % rate).rjust(10))


def _show(args):
    try:
        dc = Document.load(args.filename)
        _show_document(document=dc, filename=args.filename, verbose=True, top=args.list_top_words)
    except IOError:
        print('No such classifier: %s' % args.filename)


def _create(args):
    if args.filter == 'html':
        dc = HtmlDocument(lang=args.lang_filter, stemming=args.stemming_filter)
    else:
        dc = DefaultDocument(lang=args.lang_filter, stemming=args.stemming_filter)
    dc.save(args.filename)
    _show_document(document=dc, filename=args.filename, verbose=False)


def _learn(args):
    try:
        dc = Document.load(args.filename)
        if args.rewrite:
            dc.clear()
        print('\ncurrent')
        print('=======')
        _show_document(document=dc, filename=args.filename, verbose=False)
        print('\nupdated')
        print('=======')
        if args.url:
            dc.read_urls(*args.url)
        if args.dir:
            dc.read_dir(*args.dir)
        if args.file:
            dc.read_files(*args.file)
        if args.zip:
            dc.read_zips(*args.zip)
        if not args.no_learn:
            dc.save(args.filename)
        _show_document(document=dc, filename=args.filename, verbose=True, top=args.list_top_words)
    except IOError:
        print('No such classifier: %s' % args.filename)


def _classify(args):
    dclist = {}
    for filename in args.classifiers:
        dc = Document.load(filename)
        dclist[filename] = dc
    dc = list(dclist.values())[0].copy()
    dc.clear()
##    if args.filter == 'html':
##        dc = HtmlDocument(lang=args.lang_filter, stemming=args.stemming_filter)
##    else:
##        dc = DefaultDocument(lang=args.lang_filter, stemming=args.stemming_filter)
    if args.text:
        dc.read_text(args.text)
    elif args.url:
        dc.read_urls(args.url)
    elif args.file:
        dc.read_files(args.file)
    result = document_classifier(dc, **dclist)
    print('*','classifier'.ljust(35),'|','rate'.rjust(10))
    print(' ','-'*35,'|','-'*10)
    for classifier, rate in result:
        print(' ',classifier.encode('utf-8').ljust(35),'|',('%.8f' % rate).rjust(10))


def main():
    parser = argparse.ArgumentParser(description='Manage several document to apply text classification.',
                                     epilog="see https://github.com/dmiro/bagofwords for more info")
    parser.add_argument('--version', action='version', version=__version__,
                        help='show version and exit')
    subparsers = parser.add_subparsers(help='')
    # create command
    parser_create = subparsers.add_parser('create', help='create classifier')
    parser_create.add_argument('filter', choices=['text', 'html'], help='filter type')
    parser_create.add_argument('filename', help='file to be created where words learned are saved')
    parser_create.add_argument('--lang-filter', default='english', type=str,
                               help='language text where remove empty words')
    parser_create.add_argument('--stemming-filter', default=1, type=int,
                               help='number loops of lemmatizing')
    parser_create.set_defaults(func=_create)
    # learn command
    parser_learn = subparsers.add_parser('learn', help='add words learned a classifier')
    parser_learn.add_argument('filename', help='file to write words learned')
    parser_learn.add_argument('--file', nargs='+', help='filenames to learn')
    parser_learn.add_argument('--dir', nargs='+', help='directories to learn')
    parser_learn.add_argument('--url', nargs='+', help='url resources to learn')
    parser_learn.add_argument('--zip', nargs='+', help='zip filenames to learn')
    parser_learn.add_argument('--no-learn', action='store_true', default=False,
                              help='not write to file the words learned')
    parser_learn.add_argument('--rewrite', action='store_true', default=False,
                              help='overwrite the file')
    parser_learn.add_argument('--list-top-words', default=50, type=int,
                              help='maximum number of words to list, 50 by default, -1 list all')
    parser_learn.set_defaults(func=_learn)
    # show command
    parser_show = subparsers.add_parser('show', help='show classifier info')
    parser_show.add_argument('filename', help='filename')
    parser_show.add_argument('--list-top-words', default=50, type=int,
                             help='maximum number of words to list, 50 by default, -1 list all')
    parser_show.set_defaults(func=_show)
    # classify command
    parser_classify = subparsers.add_parser('classify', help='Naive Bayes text classification')
    parser_classify.add_argument('classifiers', nargs='+', help='classifiers')
    parser_classify.add_argument('--file', help='file to classify')
    parser_classify.add_argument('--url', help='url resource to classify')
    parser_classify.add_argument('--text',help='text to classify')
    parser_classify.set_defaults(func=_classify)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
	main()
