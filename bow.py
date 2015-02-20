# -*- coding: utf-8 -*-
__author__ = 'dmiro'
import copy

class BagOfWords(object):

    def __init__(self):
        self._bow = {}

    def _calc(self, operation, words):
        if isinstance(words, basestring):
            words = [words]
        for word in words:
            n = 1
            if isinstance(words, dict):
                n = words[word]
            if word in self._bow:
                self._bow[word] = operation(self._bow[word], n)
            else:
                self._bow[word] = operation(0, n)
            if self._bow[word] < 1:
                del self._bow[word]
                
    def add(self, words):
        """Add word or word list to bag of words
        :param values: word or word list to add
        :return:nothing"""
        self._calc(lambda x,y: x+y, words)

    def delete(self, words):
        """Del word or word list from bag of words
        :param values: word or word list to add
        :return:nothing"""
        self._calc(lambda x,y: x-y, words)

    def freq(self, word):
        """Returning the frequency of a word
        :param word: word to query
        :return: frequency"""
        if word in self._bow:
            return self._bow[word]
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









