# bagofwords

[![Build Status](https://travis-ci.org/dmiro/bagofwords.svg)](https://travis-ci.org/dmiro/bagofwords)
[![Latest Version](https://pypip.in/version/bagofwords/badge.svg)](https://pypi.python.org/pypi/bagofwords/)
[![Downloads](https://pypip.in/download/bagofwords/badge.svg)](https://pypi.python.org/pypi/bagofwords/)
[![Supported Python versions](https://pypip.in/py_versions/bagofwords/badge.svg)](https://pypi.python.org/pypi/bagofwords/)
[![Development Status](https://pypip.in/status/bagofwords/badge.svg)](https://pypi.python.org/pypi/bagofwords/)
[![License](https://pypip.in/license/bagofwords/badge.svg)](https://pypi.python.org/pypi/bagofwords/)

Introduction
------------

A Python module that allows you to create and manage a collection of occurrence counts of words without regard to grammar. The main purpose is provide a set of classes to manage several document classifieds by category in order to apply **Text Classification**.

You can make use via **API** or via **Command Line**. For example, you can generate your classified documents (*learn*) via Command Line and after via API classify an input document.

#### Third parties modules

Module uses two third parties modules

* [stop_words](https://github.com/Alir3z4/python-stop-words)
* [pystemmer](https://github.com/snowballstem/pystemmer)

The first module is used in **stop_words filter**, the second module is used in **stemming filter**. If you don't use these two filters, you don't need install them.


Installation
------------

 Install it via `pip`

`$ [sudo] pip install bagofwords`

Or download zip and then install it by running

`$ [sudo] python setup.py install`

You can test it by running

`$ [sudo] python setup.py test`


Uninstallation
--------------

`$ [sudo] pip uninstall bagofwords`


Python API
----------

This module requires Python 2.7+ 

Module contains two main classes `DocumentClass` and `Document` and four secondary classes `BagOfWords`, `WordFilters`, `TextFilters` and `Tokenizer`


#### Main classes

* `DocumentClass` Implementing a bag of words collection where all the bags of words are the same category, as well as a bag of words with the entire collection of words. Each bag of words has an identifier otherwise it's assigned an calculated identifier. Retrieves the text of a file, folder, url or zip, and also allows save or retrieve
    the collection in json format.
* `Document` Implementing a bag of words where all words are of the same category. Retrieves the text of a file, folder, url or zip, and also allows save or retrieve the Document in json format.


#### Secondary classes

* `BagOfWords` Implementing a bag of words with their frequency of usages.
* `TextFilters` Filters for transforming a text. It's used in Tokenizer class. Including filters `upper` `lower` `invalid_chars` and `html_to_text`
* `WordFilters` Filters for transforming a set of words. It's used in Tokenizer class. Including filters `stemming` `stopwords` and `normalize`
* `Tokenizer` Allows to break a string into tokens (set of words). Optionally allows you to set filters before (TextFilters) and after (WordFilters) breaking the string into tokens.


#### Subclasses

* Tokenizer subclasses `DefaultTokenizer` `SimpleTokenizer` and `HtmlTokenizer` that implements the more common filters and overwriting **after_tokenizer** and **berofe_tokenizer** methods
* Document subclasses `DefaultDocument` `SimpleDocument` and `HtmlDocument` 
* DocumentClass subclasses `DefaultDocumentClass` `SimpleDocumentClass` and `HtmlDocumentClass`


Command Line Tool
-----------------

```
usage: bow [-h] [--version] {create,learn,show,classify} ...

Manage several document to apply text classification.

positional arguments:
  {create,learn,show,classify}
    create              create classifier
    learn               add words learned a classifier
    show                show classifier info
    classify            Naive Bayes text classification

optional arguments:
  -h, --help            show this help message and exit
  --version             show version and exit
```

**Create Command**
```
usage: bow create [-h] [--lang-filter LANG_FILTER]
                  [--stemming-filter STEMMING_FILTER]
                  {text,html} filename

positional arguments:
  {text,html}           filter type
  filename              file to be created where words learned are saved

optional arguments:
  -h, --help            show this help message and exit
  --lang-filter LANG_FILTER
                        language text where remove empty words
  --stemming-filter STEMMING_FILTER
                        number loops of lemmatizing
```

**Learn Command**
```
usage: bow learn [-h] [--file FILE [FILE ...]] [--dir DIR [DIR ...]]
                 [--url URL [URL ...]] [--zip ZIP [ZIP ...]] [--no-learn]
                 [--rewrite] [--list-top-words LIST_TOP_WORDS]
                 filename

positional arguments:
  filename              file to write words learned

optional arguments:
  -h, --help            show this help message and exit
  --file FILE [FILE ...]
                        filenames to learn
  --dir DIR [DIR ...]   directories to learn
  --url URL [URL ...]   url resources to learn
  --zip ZIP [ZIP ...]   zip filenames to learn
  --no-learn            not write to file the words learned
  --rewrite             overwrite the file
  --list-top-words LIST_TOP_WORDS
                        maximum number of words to list, 50 by default, -1
                        list all
```

**Show Command**
```
usage: bow show [-h] [--list-top-words LIST_TOP_WORDS] filename

positional arguments:
  filename              filename

optional arguments:
  -h, --help            show this help message and exit
  --list-top-words LIST_TOP_WORDS
                        maximum number of words to list, 50 by default, -1
                        list all
```

**Classify Command**
```
usage: bow classify [-h] [--file FILE] [--url URL] [--text TEXT]
                    classifiers [classifiers ...]

positional arguments:
  classifiers  classifiers

optional arguments:
  -h, --help   show this help message and exit
  --file FILE  file to classify
  --url URL    url resource to classify
  --text TEXT  text to classify
```

Examples
-------

**Join several bag of words**

```
from bow import BagOfWords

a = BagOfWords('car', 'chair', 'chicken')
b = BagOfWords({'chicken':2}, ['eye', 'ugly'])
c = BagOfWords('plane')

print a + b + c
print a - b - c
```

Result

```
{'eye': 1, 'car': 1, 'ugly': 1, 'plane': 1, 'chair': 1, 'chicken': 3}
{'car': 1, 'chair': 1}
```

**HTML document class**

```
from bow import HtmlDocumentClass

html_one = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <title>bag of words demo</title>
  <link rel="stylesheet" href="css/mycss.css">
  <script src="js/myjs.js"></script>
</head>
<body>
  <style> #demo {background: #c00; color: #fff; padding: 10px;}</style>
  <!--my comment section -->
  <h2>This is a demo</h2>
  <p id="demo">This a text example of my bag of words demo!</p>
  I hope this demo is useful for you
  <script type="text/javascript"> alert('But wait, it\'s a demo...');</script>
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
dclass(id_='doc1', text=html_one)
dclass(id_='doc2', text=html_two)
print 'docs \n', dclass.docs
print 'total \n', dclass
print 'rates \n', dclass.rates
```

Result

```
>>> 
docs 
{
 'doc2': {u'silly': 1, u'example': 1, u'another': 1}, 
 'doc1': {u'useful': 1, u'text': 1, u'bag': 2, u'words': 2, u'demo': 4, u'example': 1, u'hope': 1}
}
total 
{
 u'useful': 1, u'another': 1, u'text': 1, u'bag': 2, u'silly': 1, u'words': 2, 
 u'demo': 4, u'example': 2, u'hope': 1
}
rates 
{
 u'useful': 0.06666666666666667, u'another': 0.06666666666666667, u'text': 0.06666666666666667, 
 u'bag': 0.13333333333333333, u'silly': 0.06666666666666667, u'words': 0.13333333333333333, 
 u'demo': 0.26666666666666666, u'example': 0.13333333333333333, u'hope': 0.06666666666666667
}
>>>
```


License
-------
MIT License, see [LICENSE](https://github.com/dmiro/bagofwords/blob/master/LICENSE)

