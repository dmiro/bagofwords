# bagofwords

[![Build Status](https://travis-ci.org/dmiro/bagofwords.svg)](https://travis-ci.org/dmiro/bagofwords)
[![Latest Version](http://badge.kloud51.com/pypi/v/bagofwords.svg)](https://pypi.python.org/pypi/bagofwords/)
[![Downloads](http://badge.kloud51.com/pypi/d/bagofwords.svg)](https://pypi.python.org/pypi/bagofwords/)
[![Supported Python versions](http://badge.kloud51.com/pypi/py_versions/bagofwords.svg)](https://pypi.python.org/pypi/bagofwords/)
[![Development Status](http://badge.kloud51.com/pypi/s/bagofwords.svg)](https://pypi.python.org/pypi/bagofwords/)
[![License](http://badge.kloud51.com/pypi/l/bagofwords.svg)](https://pypi.python.org/pypi/bagofwords/)


Introduction
------------

A Python module that allows you to create and manage a collection of occurrence counts of words without regard to grammar. The main purpose is provide a set of classes to manage several document classifieds by category in order to apply **Text Classification**.

You can make use via **API** or via **Command Line**. For example, you can generate your classified documents (*learn*) via Command Line and after via API classify an input document.

#### Third parties modules

Module uses thress third parties modules

* [stop_words](https://github.com/Alir3z4/python-stop-words)
* [pystemmer](https://github.com/snowballstem/pystemmer)
* [six](https://bitbucket.org/gutworth/six)

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


#### Methods

* `document_classifier(document, **classifieds)` Text classification based on an implementation of Naive Bayes


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

Example
-------

Previously you need to download a spam corpus  **enron-spam dataset**. For example you can download a compressed file that includes a directory with **1500 spam emails** and a directory with **4012 ham emails**.

```
 http://www.aueb.gr/users/ion/data/enron-spam/preprocessed/enron3.tar.gz
```

Now we will create the **spam** and **ham** classifiers 

```
$ bow create text spam
* filename: spam
* filter:
    type: DefaultDocument
    lang: english
    stemming: 1
* total words: 0
* total docs: 0
```

```
$ bow create text ham
* filename: ham
* filter:
    type: DefaultDocument
    lang: english
    stemming: 1
* total words: 0
* total docs: 0
```

It's time to learn

```
$ bow learn spam --dir enron3/spam

current
=======
* filename: spam
* filter:
    type: DefaultDocument
    lang: english
    stemming: 1
* total words: 0
* total docs: 0

updated
=======
* filename: spam
* filter:
    type: DefaultDocument
    lang: english
    stemming: 1
* total words: 223145
* total docs: 1500
* pos | word (top 50)                       | occurrence |       rate
  --- | ----------------------------------- | ---------- | ----------
    1 | "                                   |       2438 | 0.01092563
    2 | subject                             |       1662 | 0.00744807
    3 | compani                             |       1659 | 0.00743463
    4 | s                                   |       1499 | 0.00671761
    5 | will                                |       1194 | 0.00535078
    6 | com                                 |        978 | 0.00438280
    7 | statement                           |        935 | 0.00419010
    8 | secur                               |        908 | 0.00406910
    9 | inform                              |        880 | 0.00394362
   10 | e                                   |        802 | 0.00359408
   11 | can                                 |        798 | 0.00357615
   12 | http                                |        779 | 0.00349100
   13 | pleas                               |        743 | 0.00332967
   14 | invest                              |        740 | 0.00331623
   15 | de                                  |        739 | 0.00331175
   16 | o                                   |        733 | 0.00328486
   17 | 1                                   |        732 | 0.00328038
   18 | 2                                   |        709 | 0.00317731
   19 | stock                               |        700 | 0.00313697
   20 | price                               |        664 | 0.00297564
  ....
```

```
$ bow learn ham --dir enron3/ham

current
=======
* filename: ham
* filter:
    type: DefaultDocument
    lang: english
    stemming: 1
* total words: 0
* total docs: 0

updated
=======
* filename: ham
* filter:
    type: DefaultDocument
    lang: english
    stemming: 1
* total words: 1293023
* total docs: 4012
* pos | word (top 50)                       | occurrence |       rate
  --- | ----------------------------------- | ---------- | ----------
    1 | enron                               |      29805 | 0.02305063
    2 | s                                   |      22438 | 0.01735313
    3 | "                                   |      15712 | 0.01215137
    4 | compani                             |      12039 | 0.00931074
    5 | said                                |       9470 | 0.00732392
    6 | will                                |       8862 | 0.00685371
    7 | 2001                                |       8293 | 0.00641365
    8 | subject                             |       7167 | 0.00554282
    9 | 1                                   |       5887 | 0.00455290
   10 | trade                               |       5718 | 0.00442220
   11 | energi                              |       5599 | 0.00433016
   12 | market                              |       5498 | 0.00425205
   13 | new                                 |       5278 | 0.00408191
   14 | 2                                   |       4742 | 0.00366737
   15 | dynegi                              |       4651 | 0.00359700
   16 | stock                               |       4594 | 0.00355291
   17 | 10                                  |       4545 | 0.00351502
   18 | year                                |       4517 | 0.00349336
   19 | power                               |       4503 | 0.00348254
   20 | share                               |       4393 | 0.00339746
 ....
``````

Finally, we can classify a text file or url

```
$ bow classify spam ham --text "company"

* classifier                          |       rate
  ----------------------------------- | ----------
  ham                                 | 0.87888743
  spam                                | 0.12111257
```

```
$ bow classify spam ham --text "new lottery"

* classifier                          |       rate
  ----------------------------------- | ----------
  spam                                | 0.96633627
  ham                                 | 0.03366373
```

```
$ bow classify spam ham --text "Subject: a friendly professional online pharmacy focused on you !"

* classifier                          |       rate
  ----------------------------------- | ----------
  spam                                | 0.99671480
  ham                                 | 0.00328520
```

You should know that it is also possible to classify from python code

```
import bow

spam = bow.Document.load('spam')
ham = bow.Document.load('ham')
dc = bow.DefaultDocument()

dc.read_text("company")
result = bow.document_classifier(dc, spam=spam, ham=ham)

print result
```

Result

```
[('ham', 0.8788874288217258), ('spam', 0.12111257117827418)]
```


Others examples
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

