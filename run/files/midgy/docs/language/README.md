# the `midgy` language tests


this directory contains the language specification for `midgy`.
the file


## tests structure

the markdown input is renderd and compared to the explicit markdown input.

````
*********************************************************
short paragraph description
```markdown
a block or markdown source
```

```python
a block of python source
```
````

    if __name__ == "__main__":
        from pathlib import Path
        HERE = Path(__file__).parent
        import pytest
        pytest.main(args=[str(HERE / "test_language.py")])