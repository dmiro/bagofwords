# -*- coding: utf-8 -*-
import unittest
import bow

class BagOfWordsTest(unittest.TestCase):

    def setUp(self):
        self.bow = bow.BagOfWords()

    def test_one_word(self):
        self.bow.add('David')
        self.bow.add('David')
        self.bow.add('David')
        self.assertEqual(self.bow.words, ['David'])
        self.assertEqual(len(self.bow), 1)
        self.assertEqual(self.bow.num, 3)
        self.assertEqual(self.bow.freq('David'), 3)
        self.assertEqual(dict(self.bow), {'David':3})

    def test_two_words(self):
        self.bow.add(u'David')
        self.bow.add(u'David')
        self.bow.add(u'Álex')
        self.assertEqual(self.bow.words, [u'Álex', u'David'])
        self.assertEqual(len(self.bow), 2)
        self.assertEqual(self.bow.num, 3)
        self.assertEqual(self.bow.freq('David'), 2)
        self.assertEqual(dict(self.bow), {u'Álex':1, 'David':2})

    def test_join(self):
        a = bow.BagOfWords()
        b = bow.BagOfWords()
        c = bow.BagOfWords()
        a.add(['car', 'chair', 'chicken'])
        b.add(['chicken', 'chicken', 'eye', 'ugly'])
        c.add('plane')
        total = a + b + c
        self.assertEqual(dict(total), {'car': 1, 'chair': 1, 'eye': 1, 'chicken': 3, 'plane': 1, 'ugly': 1})
        total.clear()
        total = total + ['car', 'chair', 'chicken'] + ['chicken', 'chicken', 'eye']
        total = 'ugly' + total
        total = total + 'plane'
        self.assertEqual(dict(total), {'eye': 1, 'car': 1, 'ugly': 1, 'plane': 1, 'chair': 1, 'chicken': 3})
              
    def test_clear(self):
        self.bow.add('item')
        self.bow.add('item')
        self.bow.clear()
        self.assertEqual(len(self.bow), 0)
        self.assertEqual(self.bow.num, 0)
        self.assertEqual(self.bow.freq('item'), 0)
        self.assertEqual(dict(self.bow), {})

    def test_item(self):
        self.bow.add(['item1', 'item2', 'item2', 'item3'])
        self.assertEqual(self.bow['item2'], 2)
        self.assertEqual(self.bow['item3'], 1)
        self.assertEqual(self.bow['item1'], 1)


if __name__ == '__main__':
    unittest.main()
