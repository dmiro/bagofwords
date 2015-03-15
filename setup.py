from setuptools import setup, find_packages

PROJECT = "bagofwords"
  
setup(
    name=PROJECT,
    version=__import__("bow").__version__,
    author = "David Miro <lite.3engine@gmail.com>",
    description = "A Python module that allows you to create and manage a collection of \
    occurrence counts of words without regard to grammar. The main purpose is provide a set \
    of classes to manage several document classifieds by category in order to apply text \
    classification.",
    long_description=open('README.md').read(),
    license=open('LICENSE').read(),
    url='https://github.com/dmiro/bagofwords',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    py_modules=['bow'],
##    entry_points = {
##        'console_scripts': ['client = client:main']
##        },
    install_requires=[
        'stop-words',
        'PyStemmer'
        ],
    test_suite = 'test',
    platforms=['Any'],
    zip_safe=False
    )
