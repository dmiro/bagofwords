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
            if word in self._bow:
                self._bow[word] = operation(self._bow[word])
            else:
                self._bow[word] = operation(0)
            if self._bow[word] < 1:
                del self._bow[word]

##    http://stackoverflow.com/questions/10664856/make-dictionary-with-duplicate-keys-in-python
##    def _calc2(self, operation, other):
##        if isinstance(other, BagOfWords):
##            result = copy.deepcopy (self) 
##            for word, value in other._bow.items():
##                if word in result._bow:
##                    result._bow[word] = operation(self._bow[word], value)
##                else:
##                    result._bow[word] = operation(0, value)
##                if result._bow[word] < 1:
##                    del result._bow[word]
##            return result
##        else:
##            result = copy.deepcopy(self)
##            result._calc(result, other)
##            return result
    
    def add(self, words):
        """Add word or word list to bag of words
        :param values: word or word list to add
        :return:nothing"""
        self._calc(lambda x: x+1, words)

    def delete(self, words):
        """Del word or word list from bag of words
        :param values: word or word list to add
        :return:nothing"""
        self._calc(lambda x: x-1, words)

    def freq(self, word):
        """Returning the frequency of a word
        :param word: word to query
        :return: frequency"""
        if word in self._bow:
            return self._bow[word]
        else:
            return 0

    def __add__(self, other):
        """ Overloading of "+" operator to join BagOfWord+BagOfWord, BagOfWords+str or BagOfWords+[]
        :param other: BagOfWords
        :return: BagOfWords"""
        if isinstance(other, BagOfWords):
            result = copy.deepcopy (self) 
            for key in other._bow:
                if key in result._bow:
                    result._bow[key] += other._bow[key]
                else:
                    result._bow[key] = other._bow[key] 
            return result
        else:
            result = copy.deepcopy(self)
            result.add(other)
            return result
      
    def __radd__(self, other):
        return self.__add__(other)

    def __iter__(self):
        return self._bow.iteritems()

    def __getitem__(self, offset):
        return self._bow.__getitem__(offset)

    def __len__(self):
        return self._bow.__len__()
        
    def __repr__(self):
        return self._bow.__repr__()

    def clear(self):
        """Clear word list"""
        self._bow.clear()

    def iteritems(self):
        """Return an iterator over the word dictionary’s (word, frequency) pairs"""
        return self._bow.iteritems()
            
    @property
    def num(self):
        """Total number of words"""
        total = 0
        for key, value in self._bow.iteritems():
            total += value
        return total

    @property
    def words(self):
        """Word list contained in the object"""
        return self._bow.keys()







