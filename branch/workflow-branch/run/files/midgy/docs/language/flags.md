# `midgy` python language flags

flags provide control over the markdown to python translation.
flags control the rendering of:
* front matter
* doctests
* indented code
* code fences
* docstring

*******************************************************

indented code can be ignored

```markdown
+++
py.include_indented_code = false
+++
    ignored
```

```python
locals().update(__import__("midgy").front_matter.load("""+++
py.include_indented_code = false
+++"""))
"""    ignored""";
```


*******************************************************

markdown code can be ignored

```markdown
+++
py.include_markdown = false
+++
ignored
```

```python
locals().update(__import__("midgy").front_matter.load("""+++
py.include_markdown = false
+++"""))
# ignored
```

*******************************************************

front matter code can be ignored

```markdown
+++
py.include_front_matter = false
+++
```

```python
# +++
# py.include_front_matter = false
# +++
```
