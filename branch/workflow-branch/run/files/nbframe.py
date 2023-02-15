from pathlib import Path
from pandas import Series, DataFrame, Index
from dask import dataframe, distributed
from toolz.curried import first, map
from dataclasses import dataclass, field
import nbformat, functools, asyncio


@functools.lru_cache
def get_client():
    return distributed.Client(asynchronous=False)


class meta:
    O = "object"
    ANY = None, O
    NB = dict(
        (("cells", O), ("metadata", O), ("nbformat", int), ("nbformat_minor", int))
    )
    CELL = dict(
        (
            ("cell_type", str),
            ("execution_count", int),
            ("id", str),
            ("metadata", O),
            ("outputs", O),
            ("source", str),
            ("cell_ct", int),
            ("attachments", O),
        )
    )
    OUTPUT = dict(
        (
            ("data", O),
            ("metadata", O),
            ("ename", str),
            ("evalue", str),
            ("text", str),
            ("execution_count", int),
            ("output_type", str),
            ("output_ct", int),
        )
    )
    DISPLAY = dict((("type", str), ("value", str)))
    new_nb = Series(index=map(first, NB), dtype="O")
    new_cell = Series(index=map(first, CELL), dtype="O")
    new_output = Series(index=map(first, OUTPUT), dtype="O")
    new_display = Series(index=map(first, DISPLAY), dtype="O")


def get_path_stats(path: Path) -> Series:
    stat = path.stat()
    return Series(
        dict(
            suffix=path.suffix,
            created_at=stat.st_ctime,
            modified_at=stat.st_mtime,
            size=stat.st_size,
        )
    )


@dataclass
class Finder:
    dir: Path = Path.cwd()
    include: str = "*.ipynb\n*.md\n*.py"
    exclude: str = ".ipynb_checkpoints"

    def get_index(self):
        return Index(iter_files(self.dir, self.include, self.exclude), name="path")

    def get_files(self):
        return self.get_index().to_series().apply(get_path_stats)

    def to_frame(self, updated_from=None):
        df = self.get_files()
        if len(df):
            if updated_from is not None:
                return df[df.modified_at.ne(updated_from.modified_at)]
        return df

    def to_dask(self):
        df = self.to_frame()
        return dataframe.from_pandas(df, npartitions=len(df))


def get_cell(data):
    out = dict.fromkeys(meta.CELL)
    out.update(data)
    return Series(out)


def enumerate_cells(cells):
    if isinstance(cells, list):
        for i, cell in enumerate(cells):
            cell.update(cell_ct=i)
    return cells


def get_markdown_file(md):
    return nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell(md)])


def get_py_file(py):
    return nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(py)])


def get_ipynb_file(ipynb):
    return nbformat.v4.reads(ipynb)


def load_document(s: Series):
    loader = LOADERS.get(s.suffix)
    document = dict.fromkeys(meta.NB)
    if loader:
        document.update(loader(Path(s.name).read_text()))
    return Series(document)
    

@dataclass
class Documents:
    """the contents of a file system cast in the shape of notebooks."""

    finder: Finder = field(default_factory=Finder)
    df: dataframe.DataFrame = field(default=None, repr=False)
    articles: dataframe.DataFrame = field(default=None, repr=False)

    def __post_init__(self):
        self.df = self.finder.to_dask()

    def get_documents(self):
        df = self.df
        if any(df.columns.map(set(meta.NB).__contains__)):
            df = df.drop(columns=list(meta.NB))
        self.df = df.join(df.apply(load_document, meta=meta.NB, axis=1))
        return self

    def get_articles(self, df=None):
        df = self.df.cells.apply(enumerate_cells, meta=("cells", "O"))
        self.articles = df.explode().apply(get_cell, meta=meta.CELL).persist()
        return self

    def load(self):
        return self.get_documents().get_articles()


LOADERS = {".ipynb": get_ipynb_file, ".py": get_py_file, ".md": get_markdown_file}


def iter_files(dir=None, include="*.md\n*.ipynb", exclude=".nox\n.ipynb_checkpoints\n"):
    import pathspec, pathlib

    exclude_spec = (
        pathspec.PathSpec.from_lines(pathspec.GitIgnorePattern, exclude.splitlines())
        if isinstance(exclude, str)
        else exclude
    )
    include_spec = (
        pathspec.PathSpec.from_lines(pathspec.GitIgnorePattern, include.splitlines())
        if isinstance(include, str)
        else include
    )
    dir = pathlib.Path(dir or pathlib.Path.cwd())
    for f in dir.iterdir():
        if f.is_dir():
            if not exclude_spec.match_file(f):
                yield from iter_files(f, include_spec, exclude_spec)
        if f.is_file():
            if include_spec.match_file(f):
                if not exclude_spec.match_file(f):
                    yield f
