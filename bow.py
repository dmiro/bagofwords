# -*- coding: utf-8 -*-
__author__ = 'dmiro'
import copy
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

    #def __setitem__(self, key, item): http://www.diveintopython.net/object_oriented_framework/userdict.html
        
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

##    def load_json(self, fn):
##        pass
##
##    def save_json(self, fn):
##        pass



