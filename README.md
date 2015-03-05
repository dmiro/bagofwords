# bagofwords

Introduction
------------

A python module that allows you to create and manage a collection of occurrence counts of words without regard to grammar.

Key features:

* Bag of words
* Filters
* Tokenizer
* DocumentClass


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
print 'docs:\n'
print dclass.docs()
print 'total:\n'
print dclass.total()
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

