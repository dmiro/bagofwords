# -*- coding: utf-8 -*-
__author__ = 'dmiro'
import copy


class BagOfWords(object):

    def __init__(self):
        self._bow = {}

    def add(self, values):
        """Add word or word list to bag of words
        :param values: word or word list to add
        :return:nothing"""
        if isinstance(values, basestring):
            values = [values]
        for value in values:
            if value in self._bow:
                self._bow[value] += 1
            else:
                self._bow[value] = 1

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
            result = copy.deepcopy(self) 
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


        







