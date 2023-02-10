## mixing code fences and indented code

it is possible mix multiple flavors of code inputs with `midgy`.
this document demonstrates the implications of mixing
__indented code__, __code fences__, and __doctests__ inputs.

generally, it is suspected that an author or document will
choose one mode for code input and stick to it. what follows
are some of the outcomes of this choice.

*******************************************************

code fences are offset 4 spaces from indented code

````markdown
    print("indented code")
```python
print("fenced code")
```
````

````python
    print("indented code")
# ```python
print("fenced code")
# ```
````

the offset of four is defined because of the [indented code block commonmark specification].

*******************************************************


````markdown
    def an_indented_code_function():
```python
    print("encapsulated in the function")
```
```python
print("NOT encapsulated in the function")
```
````

````python
def an_indented_code_function():
    # ```python
    print("encapsulated in the function")
    # ```
# ```python
print("NOT encapsulated in the function")
# ```
````

because of the offset, the code fence needs to be indented to exist within the function defition.

[indented code block commonmark specification]: https://spec.commonmark.org/0.30/#indented-code-blocks