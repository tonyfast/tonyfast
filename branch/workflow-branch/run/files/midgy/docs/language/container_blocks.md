## transpiling in container blocks

blocks and lists make up [commonmark's container blocks](https://spec.commonmark.org/0.30/#container-blocks).

lists are probably one of the most confusing syntactic features of midgy.

 
*******************************************************

lists are strings

```markdown
* list item 1
* list item 2
```
        
```python
"""* list item 1
* list item 2""";
```


*******************************************************

indented code requires and extra indents

```markdown
* list item 1

        code block
* list item 2
    
    list paragraph
```
        
```python
"""* list item 1"""

code block
"""* list item 2
    
    list paragraph""";
```


*******************************************************

each level requires and extra code indent

```markdown
* list item 1

        code block
    * nested list item 1

            code block
    * nested list item 2
        
        list paragraph
```
        
```python
"""* list item 1"""

code block
"""    * nested list item 1"""

    code block
    """    * nested list item 2
        
        list paragraph""";
```


