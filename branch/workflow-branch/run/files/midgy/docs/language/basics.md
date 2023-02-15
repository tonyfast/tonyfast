## basic markdown to python translations

there are 3 flavors of literate programming available in `midgy`. 
we can interleave non-code with code found as: 
1. indented code blocks
2. code fences with specific `info` content
3. indented doctests when the `include_doctest` flag is enabled

-------------------------------------------------------

## tangling code with indented code blocks

the primary flavor of `midgy` literate programming uses indented code blocks.
content in between indented code blocks is treated as python blocks strings.
the samples below show some general interactions between non-code and indented code blocks.
 
*******************************************************

single markdown lines are single python strings

```markdown
a single line line of markdown is a python string.
```

```python
"""a single line line of markdown is a python string.""";
```

the semi-colon is appended to trailing block strings to suppress their output.

*******************************************************

a block of markdown lines are python block strings

```markdown
a paragraph with a list following:
* list item 1
* list item 2
```

```python
"""a paragraph with a list following:
* list item 1
* list item 2""";
```

*******************************************************

0-3 indents are treated as non-code and represented as strings

```markdown
   an indented markdown line
```

```python
"""   an indented markdown line""";
```

*******************************************************

at least 4 indents are raw python code

```markdown
    print("hello world")
```

```python
print("hello world")
```

*******************************************************

more than 4 indents are raw python code

```markdown
          print("hello world")
```

```python
print("hello world")
```

-------------------------------------------------------

## mixing code and non-code blocks

we are only concerned with block level markdown tokens when transpiling to python. through this lens a document is a collection of code and non-code blocks. 

*******************************************************

code before markdown requires a dedent and zero or more newlines

```markdown
    x = "code before markdown"
a markdown paragraph after code
```

```python
x = "code before markdown"
"""a markdown paragraph after code""";
```

*******************************************************

code after markdown requires at least one new line

```markdown
a markdown paragraph before code

    x = "code after markdown"
```

```python
"""a markdown paragraph before code"""

x = "code after markdown"
```

*******************************************************

triple double-quotes indicate explicit strings with whitespace included
    
```markdown
    """

a markdown paragraph
with lines

    """
```

```python
"""

a markdown paragraph
with lines

"""
```

*******************************************************

triple single-quotes indicate explicit strings with whitespace included
    
```markdown
    '''

a markdown paragraph
with lines

    '''
```

```python
'''

a markdown paragraph
with lines

'''
```
*******************************************************

markdown following a colon block (function) is indented and is the docstring
    
```markdown
        def f():

the docstring of the function f

        print(f())
```

```python
def f():

    """the docstring of the function f"""

print(f())
```

*******************************************************

markdown following a colon block (function) aligns to trailing code and is the docstring
    
```markdown
        def f():
the docstring of the function f

                        return 42
```

```python
def f():
                """the docstring of the function f"""

                return 42
```


*******************************************************

line continuations connect code to lines to markdown lines

```markdown
            foo =\

line continuations assign this string to `foo`
```

```python
foo =\
\
"""line continuations assign this string to `foo`""";
```


*******************************************************

line continuations remove whitespace when using explicit quotes

```markdown
            foo = """\


line continuations remove the whitespace\

            """.split()
```

```python
foo = """\
\
\
"""line continuations remove the whitespace"""\
\
""".split()
```

*******************************************************

markdown can be used as parameters in a function call.

```markdown
    requests.get(
https://api.github.com

    )
```

```python
requests.get(
"""https://api.github.com"""

)
```

*******************************************************

as parameters, markdown blocks can be manipulated with python

```markdown
    urls = [url.lstrip("*").lstrip() for url in 
* https://api.github.com
* https://google.com

        .splitlines()]
```

```python
urls = [url.lstrip("*").lstrip() for url in 
"""* https://api.github.com
* https://google.com"""

    .splitlines()]
```

*******************************************************

by default doctests are not included in code.

```markdown
>>> this is a blockquote
... with a trailing paragraph
and is not a doctest

    >>> assert 'this is a doctest\
    ... because it is indented'
```

```python
""">>> this is a blockquote
... with a trailing paragraph
and is not a doctest

    >>> assert \'this is a doctest\
    ... because it is indented\'""";
```
