from setuptools import setup, find_packages

PROJECT = "bagofwords"

long_description = ''

try:
    import subprocess
    import pandoc

    process = subprocess.Popen(
        ['which pandoc'],
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    pandoc_path = process.communicate()[0]
    pandoc_path = pandoc_path.strip('\n')

    pandoc.core.PANDOC_PATH = pandoc_path

    doc = pandoc.Document()
    doc.markdown = open('README.md').read()

    long_description = doc.rst

except:
    pass

setup(
    name=PROJECT,
    version=__import__("bow").__version__,
    author = "David Miro <lite.3engine@gmail.com>",
    author_email = 'lite.3engine@gmail.com',
    description = "The main goal this Python module is to provide functions to apply Text Classification.",
    long_description=long_description,
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
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License'
        ],
    py_modules=['bow'],
    entry_points = {
        'console_scripts': ['bow = bow:main']
        },
    install_requires=[
        'stop-words',
        'PyStemmer',
        'six'
        ],
    test_suite = 'test',
    platforms=['Any'],
    zip_safe=False
    )
