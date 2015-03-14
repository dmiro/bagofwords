# bagofwords

Introduction
------------

A Python module that allows you to create and manage a collection of occurrence counts of words without regard to grammar. The main purpose is provide a set of classes to manage several document classifieds by category in order to apply **text classification**.

You can make use via **API** or via **Command Line**. For example, you can generate your classified documents (*learn*) via Command Line and after via API classify an input document.

##### Third parties modules

Module uses two third parties modules:

* [stop_words] (https://github.com/Alir3z4/python-stop-words)
* [pystemmer] (https://github.com/snowballstem/pystemmer)

The first module is used in **stop_words filter**, the second module is used in **stemming filter**. If you don't use these two filters, you don't need install them.

Installation
------------

```
 $ [sudo] pip install .... soon!
```

Uninstallation
--------------

```
 $ [sudo] pip uninstall .... soon!
```


Python API
----------

This module requires Python 2.7+ 

Module contains two main classes `DocumentClass` and `Document` and four secondary classes `BagOfWords`, `WordFilters`, `TextFilters` and `Tokenizer`

##### Main classes

* `DocumentClass` Implementing a bag of words collection where all the bags of words are the same category, as well as a bag of words with the entire collection of words. Each bag of words has an identifier otherwise it's assigned an calculated identifier. Retrieves the text of a file, folder, url or zip, and also allows save or retrieve
    the collection in json format.
* `Document` Implementing a bag of words where all words are of the same category. Retrieves the text of a file, folder, url or zip, and also allows save or retrieve the Document in json format.

##### Secondary classes

* `BagOfWords` Implementing a bag of words with their frequency of usages.
* `TextFilters` Filters for transforming a text. It's used in Tokenizer class. Including filters `upper` `lower` `invalid_chars` and `html_to_text`
* `WordFilters` Filters for transforming a set of words. It's used in Tokenizer class. Including filters `stemming` `stopwords` and `normalize`
* `Tokenizer` Allows to break a string into tokens (set of words). Optionally allows you to set filters before (TextFilters) and after (WordFilters) breaking the string into tokens.


##### Examples

1. Join several bag of words

```
from bow import BagOfWords

a = BagOfWords('car', 'chair', 'chicken')
b = BagOfWords({'chicken':2}, ['eye', 'ugly'])
c = BagOfWords('plane')

print a + b + c
print a - b - c
```

**Result**

```
{'eye': 1, 'car': 1, 'ugly': 1, 'plane': 1, 'chair': 1, 'chicken': 3}
{'car': 1, 'chair': 1}
```

2. HTML document class

```
from bow import HtmlDocumentClass

html_one = '''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset=utf-8>
	<title>bag of words demo</title>
	<link rel="stylesheet" href="css/mycss.css">
	<script src="js/myjs.js"></script>
</head>
<body>
	<style>
	  #demo {
		background: #c00;
		color: #fff;
		padding: 10px;
	  }
	</style>
	<!--my comment section -->
	<h2>This is a demo</h2>
	<p id="demo">This a text example of my bag of words demo!</p>
	I hope this demo is useful for you
	</article>
	<script type="text/javascript">
	  alert('But wait, it\'s a demo...');
	</script>
</body>
</html>
'''

html_two = '''
<!DOCTYPE html>
<html lang="en">
<head> </head>
<body> Another silly example. </body>
</html>
'''

dclass = HtmlDocumentClass(lang='english', stemming=0)
dclass(id_='html_one', text=html_one)
dclass(id_='html_two', text=html_two)
print 'docs >>\n', dclass.docs
print 'total >>\n', dclass
print 'rates >>\n', dclass.rates()
```

**Result**

```
>>> 
docs >>
{'html_one': {u'useful': 1, u'text': 1, u'bag': 2, u'words': 2, u'demo': 4, u'example': 1, u'hope': 1}, 'html_two': {u'silly': 1, u'example': 1, u'another': 1}}
total >>
{u'useful': 1, u'another': 1, u'text': 1, u'bag': 2, u'silly': 1, u'words': 2, u'demo': 4, u'example': 2, u'hope': 1}
rates >>
{u'useful': 0.06666666666666667, u'another': 0.06666666666666667, u'text': 0.06666666666666667, u'bag': 0.13333333333333333, u'silly': 0.06666666666666667, u'words': 0.13333333333333333, u'demo': 0.26666666666666666, u'example': 0.13333333333333333, u'hope': 0.06666666666666667}
>>>
```


Command Line Tool
-----------------


Example
*******

```
soon!
```

Testing
-------
The module uses ```unittest```

Then run test as normal.

```
soon!
```

License
-------
MIT License, see [LICENSE](https://github.com/dmiro/bagofwords/blob/master/LICENSE)

