# executable markdonw :fontawesome-brands-markdown: files

`midgy` runs markdown :fontawesome-brands-markdown: documents as python :fontawesome-brands-python:.

🤔 imagine being able to run your `README.md` as code. you could run the following command

```bash
midgy README.md
```

and all your :fontawesome-brands-markdown: is converted to valid :fontawesome-brands-python:, and off your go!

## 🔮 the future is markdown :fontawesome-brands-markdown:

markdown has emerged is a common file format for documentutation.
those just learning programming will bring rely on their language to
read and write code. `midgy`s approach to literate programming leaves space 
for both natural and programming languages to cooperate in a story.
it brings flexibility and freedom to the composition of news ideas.[^lp]

## ℹ️ about this documentation

this documentation describes:

* [__the midgy language__](language/README.md) specification describes how markdown is translated to python
* [__the midgy implementation__](midgy.md) describes the specifics of the python implementation.[^implementation]
* [__the midgy design__](design.md) describes the design constraints this work was developed under.



[literate programming]: http://www.literateprogramming.com/knuthweb.pdf
[^lp]: 
    freedom is a feature of literate programming more generally. in different literate programming circles like `orgmode`, `rmarkdown`, `quarto`, `jupyter` we notice a common thread of joy in composing programs. we find these features are by design when we reference the original [literate programming] paper:
[^implementation]:
    this specific implementation is written in python, but there is a little holding others back from porting this to other languages.