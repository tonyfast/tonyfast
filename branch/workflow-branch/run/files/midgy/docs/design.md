# the `midgy` design

`midgy` is half of a literate programming implementation. 
literate programming a programming  paradigm proposed by donald knuth in 1984 that elevates authoring programming to the level of literature. as literate programmers we strive for literary and computational elegance because *surely no one wants to write an illiterate program*.

literate programming specifies multi-lingual documents that serve as both literate and programs. in this paper, two document translation are defined:

1. __tangle__: refers to translating the document to code. 
2. __weave__: refers to translating the document to a view (eg. html, pdf)

`midgy` only __tangles__ markdown to python; it is the complement to `pidgy` which adds opinions on weaving.

## design choices

extends
reverse
retrieve
obsolesce

every literate programming implementation needs to make choice of document & programming. 


the desire with `midgy` to allows authors to explore the new interface between code & non-code. a place that has little been explored

### markup language

`midgy` uses markdown because:
* it is inclusive of nearly all formal and programming languages
* markdown rarely fails. it violates expectation.
* it is a useful markdown with plain-text
* it commonly taught and widely adopted in software circles.
* CommonMark has version 1.0 and communities are adopting the convention.

### programming language

pascal was chosen for the original literate programming implementation because of its influence in education. a similar argument can be made for the choice of python in `midgy`. computer programming for everybody was a strong foundation for python that promotes programming as a mass literacy. 

another way to measure pythons impact is using the TIOBE scale. this scale measures popularity among programmers because ignores a large swath of folks who don't program.

## literacy


## design goals

* line-for-line transformations
* make pseudocode real code
* cooperate with documentation systems
* customizable
* minimize changes to generate valid python


## prior art

### jupyter notebooks

## choice of markup language and implementation

the __[tokenization]__ step reuses machinery from the [`markdown_it`] project. this library was chosen because amongst other markdown parsers (eg. [`mistune`], [`mistletoe`], [`python-markdown`]) it is the only one to return line numbers. 

[`markdown_it`] it is a port of the popular [markdown it javascript library]. it appears reliable for the `parser` and `tokens` because: 
* it is not innovating independently so we should expect a fairly stable api.
* the plugin interface makes it possible to extend the markdown parser in consistent ways as we do for the `code_lexer`, `doctest_lexer` and `front_matter` lexer.
* further, [`markdown_it`] has [strong adoption](https://pypistats.org/packages/markdown-it-py) specifically through documentation in `jupyter_book` and linting with `mdformat`. 


    

[tokenization]: https://en.wikipedia.org/wiki/Lexical_analysis#Tokenization
[`markdown_it`]: https://github.com/executablebooks/markdown-it-py
[markdown it javascript library]: https://github.com/markdown-it/markdown-it
[`mistune`]: https://pypi.org/project/mistune/
[`mistletoe`]: https://pypi.org/project/mistletoe/
[`python-markdown`]: https://pypi.org/project/markdown/
[`jupyter_book`]: https://pypi.org/project/jupyter-book/