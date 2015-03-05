# bagofwords

Introduction
------------

A python module that allows you to create and manage a collection of occurrence counts of words without regard to grammar.

Module contains two main classes ```DocumentClass``` and ```DocumentClassPool``` and four secondary classes ```BagOfWords```, ```WordFilters```, ```TextFilters``` and ```Tokenizer``` 

##### Main classes

* ```DocumentClass``` implementing a bag of words collection where all the bags of words are the same category. Retrieves the text of a file, folder, url or zip, and save or retrieve the collection in json format. This class uses secondary classes.
* ```DocumentClassPool``` soon

##### Secondary classes

* ```BagOfWords``` implementing a bag of words with their frequency of usages.
* ```TextFilters``` filters for transforming a text. It's used in Tokenizer class.
* ```WordFilters``` filters for transforming a set of words. It's used in Tokenizer class.
* ```Tokenizer``` allows to break a string into tokens (set of words). Optionally allows you to set filters before (TextFilters) and after (WordFilters) breaking the string into tokens.

##### Key features


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

Synopsis
********

soon!


Example
*******

```
from bow import DocumentClass

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
<head>
</head>
<body>
    Another silly example.
</body>
</html>
'''

class HtmlDocumentClass(DocumentClass):

    def __init__(self, category):
        DocumentClass.__init__(self, category)

    def before_tokenizer(self, textfilters, text):
        text = textfilters.html_to_text(text)
        text = textfilters.invalid_chars(text)
        text = textfilters.lower(text)
        return text

    def after_tokenizer(self, wordfilters, words):
        words = wordfilters.stopwords('english', words)
        words = wordfilters.normalize(words)
        return words
            
dclass = HtmlDocumentClass('demo')
dclass('html_one', html_one)
dclass('html_two', html_two)
print 'docs:'
print dclass.docs
print 'total:'
print dclass.total
```

Result

```
>>> ================================ RESTART ================================
>>> 
docs:
{'html_one': {u'useful': 1, u'text': 1, u'bag': 2, u'words': 2, u'demo': 4, 
u'example': 1, u'hope': 1}, 'html_two': {u'silly': 1, u'example': 1, u'another': 1}}
total:
{u'useful': 1, u'another': 1, u'text': 1, u'bag': 2, u'silly': 1, u'words': 
2, u'demo': 4, u'example': 2, u'hope': 1}
>>> 
```


Command Line Tool
-----------------

Synopsis
********

```
soon!
```

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

