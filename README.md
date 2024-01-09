# ℹ️ about tonyfast

tonyfast is a freelance developer, designer, and scientist with significant experience in open source and science software. he is a [distinguished project jupyter contributor][distinguished] advocating for computational literacy, equity, and digital accessibility in scientific technologies.

* [📓 notebooks][Notebooks]
* [💀 deathbeds][deathbeds]
* [💻 github][Github]
* [💼 linkedin][Linkedin] 

## 🛠️ current projects

* [materialsgenomefoundation] strategic planning lead for an open materials science economy
* [nbconvert-a11y] né [notebooks for all] collaboration with [Space Telescope Science Institute] improving the accessibility of static notebooks through collaboration with designers and compensated disabled testers.
* [project jupyter accessibility working group], [jupyter triage], and [jupyter community calls]
* writing experiments with literate programs and computational essays on [my blog][notebooks].
* [`pidgy`][pidgy], [`midgy`][midgy], and [`importnb`][importnb] literate computing tools.


<details markdown>
<summary>➕ more</summary>

## 💿 events and media

* [writers workshop]
* [quirkshops]
* [open source directions]
* jupyter accessibility workshops [part 1] [part 2]
* [alt text events]
  * [scipy alt text scavenger hunt][scavenger hunt]
* [atlanta jupyter user group]
* [pydata atlanta]
* [deathbeds blog]
* [jupyter day triangle][jupyter triangle]
* jupyter days atlanta [2016] [2018]

## 📽️ presentations


* [ten pounds of 💩][xlbs]
* [reincarnation of the notebook][reincarnation]
* [calligrams]
* [powers often][powersoften]
* [ten things 'bout jupyter][ten]
* [notebookism]
* [the materials data scientist]

[alt text events]: https://github.com/isabela-pf/a11y-events/tree/main/workshop-resources/alt-text
[lifedeath]: #
[ten]: https://github.com/tonyfast/ten "ten things bout jupyter from 2018"
[notebookism]: https://github.com/tonyfast/notebookism-chicago  "a relation between journaling, physical, and digital notebooks from 2016"

## 👨‍🏭 organizations

* Materials Genome Foundation
* Quansight, LLC
* PyData Atlanta
* Bastille Networks
* Anaconda Inc
* Georgia Tech
* University of California Santa Barbara

</details>

<details markdown>
<summary>❓ about this repository</summary>

## the `tonyfast` distribution

this repository is one of github's special repositories for my personal profile.
i wanted to do more with than just a readme so i'm using it as a place to package my
computational essays or literate programs as a python distribution. 

currently this project features:

- [x] blogs, essays, notebooks and markdown re-used as python source code
- [x] a python project called `tonyfast` that uses [`hatch`][hatch] for most development tasks (see [`pyproject.toml`](pyproject.toml))

    ```
    pip install -e. # for development mode
    ```

- [x] github actions to deploy my content on github pages. the documentation is made of:

  - [x] [`mkdocs` documentation][notebooks] with my own notebook customizations. (see [`mkdocs.yml`](mkdocs.yml))
  - [x] a no-install, in-the-browser [`jupyterlite` demo][lite] so myself and others can try out the code themselves

- [ ] some things i'd like to do:
  
  - [ ] add cron for some posts
  - [ ] add tests for some posts
  - [ ] build a solid binder to run heavier demos that might not work in `jupyterlite`

</details>

[Linkedin]: https://www.linkedin.com/in/tonyfast/
[Github]: https://github.com/tonyfast
[Notebooks]: https://tonyfast.github.io/tonyfast/
[distinguished]: https://jupyter.org/governance/distinguished_contributors.html
[deathbeds]: https://github.com/deathbeds "experimental interactive computing tools orbitting project jupyter"
[notebooks for all]: https://github.com/Iota-School/notebooks-for-all/
[Space Telescope Science Institute]: https://www.stsci.edu/
[importnb]: https://github.com/deathbeds/importnb "imports notebooks and other documents formats with python's import."
[pidgy]: https://github.com/deathbeds/pidgy "weaves markdown to rich interactive jupyter displays"
[midgy]: https://github.com/deathbeds/midgy "tangles markdown to python source code"
[project jupyter accessibility working group]: https://github.com/jupyter/accessibility
[jupyter community calls]: https://discourse.jupyter.org/t/jupyter-community-calls/668
[scavenger hunt]: https://labs.quansight.org/blog/alt-text-scipy-2022
[part 1]: https://blog.jupyter.org/join-us-for-the-jupyter-accessibility-workshops-part-1-133e0e522d1b
[part 2]: https://blog.jupyter.org/join-us-for-the-jupyter-accessibility-workshops-part-2-aae1dbcdb9ac
[reincarnation]: https://github.com/deathbeds/reincarnation "how to bring life to notebooks after they've been authored"
[powersoften]: https://github.com/deathbeds/powersoften "a survey of the scales and perspectives of open source scientific computing"
[xlbs]: https://github.com/deathbeds/XlbsOSh_t
[open source directions]: https://www.youtube.com/@openteams6924/videos "bi weekly video series showcasing progress and roadmaps from popular open source projects"
[quirkshops]: https://www.youtube.com/@quansightquirkshops2781/streams "eccentric lifestyle conversations with open source experts and practioners"
[jupyter triage]: #
[2016]: https://jupyterday-atlanta-2016.github.io/
[2018]: https://atl-jugheads.github.io/jupyter-day-atlanta-ii/
[jupyter triangle]: https://renci.org/event/jupyter-day-in-the-triangle/
[pydata atlanta]: https://www.meetup.com/pydata-atlanta/?_cookie-check=St-JjKn1qVhJsUZ4
[atlanta jupyter user group]: https://twitter.com/jupyteratlanta
[deathbeds blog]: https://nbviewer.org/github/deathbeds/deathbeds.github.io/tree/master/
[writers workshop]: https://github.com/Quansight/writers-workshop/discussions "a cirriculum for learning to write literate programs in jupyter"
[the materials data scientist]: https://www.slideshare.net/tonyfast1/the-materials-data-scientist
[hatch]: https://hatch.pypa.io/
[lite]: https://tonyfast.github.io/tonyfast/run/lab/
[calligrams]: https://nbviewer.org/gist/tonyfast/a1c50b9e2ff6385492245859ca34b053 "a presentation on the text and form of data presentations"
[nbconvert-a11y]: https://github.com/deathbeds/nbconvert-a11y "accessibility templates, tests, and documentation about computational notebooks"
