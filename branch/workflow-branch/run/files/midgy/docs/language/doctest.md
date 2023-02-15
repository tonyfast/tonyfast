+++
py.include_doctest = true
py.include_indented_code = false
+++

# doctest


*******************************************************

`include_doctest` flag includes doctest inputs in code

```markdown
    >>> print("a doctest")
    a doctest
```

```python
print("a doctest")
# a doctest
```
*******************************************************

doctests can contain magics

```markdown
    >>> %%python
    ... print("a doctest")
    a doctest
```

```python
get_ipython().run_cell_magic('python', '',
"""print("a doctest")""")
# a doctest
```

*******************************************************

doctests can contain magics

```markdown
+++
py.include_indented_code = true
+++
    "normal code and doctest code are separated"

    >>> print("a doctest")
    a doctest
```

```python
locals().update(__import__("midgy").front_matter.load("""+++
py.include_indented_code = true
+++"""))
"normal code and doctest code are separated"

print("a doctest")
# a doctest
```

----------------------------------------------------------

## using explicit `doctest` for literate programming

it is possible to program in doctests.  


[pymarkdown]: https://github.com/mrocklin/pymarkdown