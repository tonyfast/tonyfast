+++
py.include_doctest = true
+++


# `midgy` and magics

cell magics only built in to the language as they provide macro features for code.


*******************************************************

magics can be in indented code

```markdown
%%magic arguments
the body of the cell magic
is quoted and indents are maintained
```

```python
get_ipython().run_cell_magic('magic', 'arguments',
"""the body of the cell magic
is quoted and indents are maintained""")
```

*******************************************************

magics can be in code fences

````markdown
```ipython
%%magic arguments 
the body 
```
````

````python
# ```ipython
get_ipython().run_cell_magic('magic', 'arguments', 
"""the body""") 
# ```
````

*******************************************************

magics can be in doctests

````markdown
    >>> %%magic arguments 
    ... the body 
    some output
````

````python
get_ipython().run_cell_magic('magic', 'arguments', 
"""the body""") 
# some output
````

*******************************************************

magics can exist in the fence info

````markdown
```%%magic arguments 
the body 
```
````

````python
get_ipython().run_cell_magic('magic', 'arguments', # ``` 
"""the body""") 
# ```
````

this form is not friendly in native markdown mode