## front matter

`midgy` permits `yaml` and `toml` front matter.

*******************************************************

triple + indicates toml front matter

```markdown
+++
+++
```

```python
locals().update(__import__("midgy").front_matter.load("""+++
+++"""))
```

*******************************************************

triple - indicates yaml front matter
    
```markdown
---
---
```

```python
locals().update(__import__("midgy").front_matter.load("""---
---"""))
```



*******************************************************

only shebang tokens can precede front matter

```markdown
#!/usr/bin/env midgy
---
---
```

```python
#!/usr/bin/env midgy
locals().update(__import__("midgy").front_matter.load("""---
---"""))
```

*******************************************************

non-shebang tokens cancel front matter

```markdown
a short paragraph
---
---
```

```python
"""a short paragraph
---
---""";
```
*******************************************************

exclude front matter from parsing

```markdown
+++
[py]
include_front_matter = false
+++
```

```python
# +++
# [py]
# include_front_matter = false
# +++
```
