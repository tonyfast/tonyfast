# line continuations

line continuations can connect markdown and python blocks separated by whitespace

*******************************************************

markdown blocks continue to code blocks when ending with line continuations, whitespace is captured

```markdown
a markdown paragraph can continues\

        
        .upper()
```

```python
"""a markdown paragraph can continues"""\
\
        \
.upper()
```

*******************************************************

code block continuations implicitly connect markdown blocks

```markdown
    foo =\

this is a string
```

```python
foo =\
\
"""this is a string""";
```

*******************************************************

continuations in the middle of markdown or code are translated explicitly

```markdown
a markdown paragraph can continues\
into this

    x = \
    42
```

```python
"""a markdown paragraph can continues\
into this"""

x = \
42
```
