# `midgy`

`midgy` transforms markdown to python modules and scripts.

### command line interface

```bash
midgy README.md     # run a readme file as python
midgy run README.md     # run a readme file as python
midgy -m README     # run a readme file as python
```   
   
      >>> from midgy.run import Markdown
      >>> with Markdown():
      ...   import README
      >>> print(README)
      <module 'README' from '...README.md'>
      

`midgy` is one half of `pidgy`, together they bring literate programming and computing afforandances to [python] and [`IPython`]. `midgy` is only concerned with the half of literate programming that translates a document to compiled code. `midgy` has a small api:

* `md_to_python` - a function that converts a markdown document to python
* `Python` - a class that parses a markdown document and renders python
* `midgy.run.Markdown` - is an `importnb` context manager that includes markdown documents when importing python modules.


## tangling literate programs

 literate programming is paradigm that treats code as literate, and vice versa; documents are evaluated on their literary and computational qualities. there are two actions defined in the framework of literate programming:

1. render
   : the act of translating the document into a programming language
   : `midgy` renders markdown to python
2. weave
   : the act of translating the document to a rendered format
   : `pidgy` weaves markdown to html, pdf, or md through the `jinja2` template system.

`midgy` focuses only on the `render` actions, and is extended in `pidgy` which implements the weave action.

### extending the lexical analysis of CommonMark markdown

`midgy` extends the commonmark spec to reflect some common conventions.

1. shebang
   : `midgy` documents are programs and may begin with a shebang.
2. front matter
   : can be included at the beginning of a document or after a shebang.
   : either toml, json or yaml can be used
3. doctest
   : a literate programming convention for including tests in python strings
4. code
   : our code blocks are modified to be aware of doctests and include lexical diagnostics of the content

### rendering tokenized CommonMark as Python

`midgy` translates markdown to python relative to indented code blocks. content between indented code blocks are wrapped a python block strings, and non-indented code blocks can be included in python programs. the translation from markdown to python is meant to require the fewest changes to have valid python code.

`midgy` goes to great lengths to generate a line-for-line translation of the markdown to python.
the line-for-line translation improves the error handling experience when using non-python documents as modules.

      from sys import argv
      print(argv)