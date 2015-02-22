# -*- coding: utf-8 -*-
import unittest
from bow import BagOfWords

class BagOfWordsTest(unittest.TestCase):

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
        self.bow.add('David')
        self.bow.delete('David')
        self.assertEqual(dict(self.bow), {})
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
        self.bow.add('David', u'Álex')
        self.bow.delete('David', u'Álex')
        self.assertEqual(dict(self.bow), {})
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
        total = a + b + c
        total = 'ugly' + total
        self.assertEqual(dict(total), {'car': 1, 'chair': 1, 'eye': 1, 'chicken': 3, 'plane': 1, 'ugly': 2})
        total = a + b + c
        total = 'ugly' + total
        total = total + 'plane'
        self.assertEqual(dict(total), {'car': 1, 'chair': 1, 'eye': 1, 'chicken': 3, 'plane': 2, 'ugly': 2})  
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
        total = b - c - a 
        total = 'eye' - total
        self.assertEqual(dict(total), {'chicken':1, 'ugly':1})
        total = b - c - a 
        total = 'eye' - total
        total = total - 'eye'
        self.assertEqual(dict(total), {'chicken':1, 'ugly':1})
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
        a.add('car')
        self.assertEqual(a == b, False)

    def test_has_key(self):
        self.bow.add('car', 'chair', 'chicken')
        self.assertEqual(self.bow.has_key('car'), True)
        self.assertEqual('car' in self.bow, True)

    def test_rate(self):
        self.bow.add(['a','a','a','b'])
        self.assertEqual(self.bow.rates(), {'a':0.75, 'b':0.25})
        self.assertEqual(self.bow.rate('a'), 0.75)
        self.assertEqual(self.bow.rate('b'), 0.25)
        self.assertEqual(self.bow.rate('c'), 0)
        self.bow.clear()
        self.assertEqual(self.bow.rate('a'), 0)

    def test_json(self):
        self.bow.add(['a','a','a','b'])
        self.assertEqual(self.bow.to_json(), '{\n "a": 3, \n "b": 1\n}')
        self.bow.clear()
        self.assertEqual(self.bow.to_json(), '{}')
        self.bow.from_json('{\n "a": 3, \n "b": 1\n}')
        self.assertEqual(dict(self.bow), {'a': 3, 'b': 1})
        self.bow.from_json('{}')
        self.assertEqual(dict(self.bow), {})
        
if __name__ == '__main__':
    unittest.main()
