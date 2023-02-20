"""render builds the machinery to translate markdown documents to code."""

from dataclasses import dataclass, field
from functools import partial
from io import StringIO
from re import compile

__all__ = ()

DOCTEST_CHAR, CONTINUATION_CHAR, COLON_CHAR, QUOTES_CHARS = 62, 92, 58, {39, 34}
BLOCK, FENCE, PYCON = "code_block", "fence", "pycon"
ESCAPE = {x: "\\" + x for x in "'\""}
ESCAPE_PATTERN = compile("[" + "".join(ESCAPE) + "]")
escape = partial(ESCAPE_PATTERN.sub, lambda m: ESCAPE.get(m.group(0)))
SP, QUOTES = chr(32), (chr(34) * 3, chr(39) * 3)


# the Renderer is special markdown renderer designed to produce
# line for line transformations of markdown to the converted code.
# not all languages require this, but for python it matters.
@dataclass
class Renderer:
    """the base render system for markdown to code.

    * tokenize & render markdown as code
    * line-for-line rendering
    * use indented code as fiducial markers for translation
    * augment the commonmark spec with shebang, doctest, code, and front_matter tokens
    * a reusable base class that underlies the python translation
    """

    parser: object = None
    cell_hr_length: int = 9
    include_code: bool = True # the nuclear option
    include_code_fences: set = field(default_factory=set)
    include_indented_code: bool = True
    include_doctest: bool = False
    config_key: str = "py"
    env: dict = None

    def __post_init__(self):
        self.parser = self.get_parser()

    @classmethod
    def code_from_string(cls, body, **kwargs):
        """render a string"""
        return cls(**kwargs).render(body)

    def get_block(self, env, stop=None):
        """iterate through the lines in a buffer"""
        if stop is None:
            yield from env["source"]
        else:
            while env["last_line"] < stop:
                yield self.readline(env)

    def get_cells(self, tokens, *, env=None, include_hr=True):
        """walk cells separated by mega-hrs"""
        block = []
        for token in tokens:
            if token.type == "hr":
                if (len(token.markup) - token.markup.count(" ")) > self.cell_hr_length:
                    yield (list(block), token)
                    block.clear()
                    if include_hr:
                        block.append(token)
                    elif env is not None:
                        list(self.get_block(env, token))
            else:
                block.append(token)
        if block:
            yield block, None

    def get_front_matter(self, tokens):
        for token in tokens:
            if token.type == "shebang":
                continue
            if token.type == "front_matter":
                from .front_matter import load

                if "data" in token.meta:
                    return token.meta["data"]
                return token.meta.setdefault("data", load(token.content))
            return

    def get_initial_env(self, src, tokens):
        """initialize the parser environment indents"""
        env = dict(**self.env or dict(), source=StringIO(src), last_line=0, last_indent=0)
        for token in filter(self.is_code_block, tokens):  # iterate through the tokens
            env["min_indent"] = min(env.get("min_indent", 9999), token.meta["min_indent"])
        env.setdefault("min_indent", 0)
        return env

    def get_parser(self):
        from markdown_it import MarkdownIt

        parser = MarkdownIt("gfm-like", options_update=dict(inline_definitions=True, langPrefix=""))
        return self.set_parser_defaults(parser)

    def get_updated_env(self, token, env, **kwargs):
        """update the state of the environment"""
        left = token.content.rstrip()
        env.update(
            continued=left.endswith("\\"),
            colon_block=left.endswith(":"),
            quoted_block=left.endswith(QUOTES),
        )
        env.update(kwargs)

    def is_code_block(self, token):
        """is the token a code block entry"""
        if self.include_code:
            if token.type == BLOCK:
                if token.meta["is_doctest"]:
                    return self.include_doctest
                return self.include_indented_code
            elif token.type == FENCE:
                if token.info in self.include_code_fences:
                    return True
                if token.info == PYCON:
                    return self.include_doctest
        return False

    def non_code(self, env, next=None):
        yield from self.get_block(env, next.map[0] if next else None)
        if next:
            env.update(last_indent=next.meta.get("last_indent", 0))

    def parse(self, src, env=None):
        return self.parser.parse(src, env)

    def parse_cells(self, body, *, include_hr=True):
        yield from (x[0] for x in self.get_cells(self.parse(body), include_hr=include_hr))

    def print(self, iter, io):
        return print(*iter, file=io, sep="", end="")

    def readline(self, env):
        try:
            return env["source"].readline()
        finally:
            env["last_line"] += 1

    def render(self, src):
        return self.render_tokens(self.parse(src), src=src)

    def render_cells(self, src, *, include_hr=True):
        # cells allow different parsers in a single pass
        tokens = self.parse(src)
        self = self.renderer_from_tokens(tokens)
        prior = self.get_initial_env(src, tokens)
        prior_token = None
        source = prior.pop("source")

        for block, next_token in self.get_cells(tokens, env=prior, include_hr=include_hr):
            env = self.get_initial_env(src, block)
            env["source"], env["last_line"] = source, prior["last_line"]
            prior_token and block.insert(0, prior_token)
            yield self.render_tokens(block, env=env, stop=next_token)
            prior, prior_token = env, next_token

    def render_token(self, token, env):
        if token:
            method = getattr(self, token.type, None)
            if method:
                yield from method(token, env) or ()

    def render_tokens(self, tokens, env=None, src=None, stop=None, target=None):
        """render parsed markdown tokens"""
        if target is None:
            target = StringIO()
        self = self.renderer_from_tokens(tokens)
        if env is None:
            env = self.get_initial_env(src, tokens)
        for token in tokens:
            if self.is_code_block(token):
                env["next_code"] = token
            self.print(self.render_token(token, env), target)
        # handle anything left in the buffer
        self.print(self.non_code(env, stop), target)
        return target.getvalue()  # return the value of the target, a format string.

    def renderer_from_tokens(self, tokens):
        front_matter = self.get_front_matter(tokens)
        if front_matter:
            # front matter can reconfigure the parser and make a new one
            config = {k: getattr(self, k) for k in self.__dataclass_fields__}
            config.update(front_matter.get(self.config_key, {}))
            if config:
                return type(self)(**config)
        return self

    def set_parser_defaults(self, parser):
        # our tangling system adds extra conventions to commonmark:
        ## extend indented code to recognize doctest syntax in-line
        ## replace the indented code lexer to recognize doctests and append metadata.
        ## recognize shebang lines at the beginning of a document.
        ## recognize front-matter at the beginning of document of following shebangs
        from mdit_py_plugins import deflist, footnote
        from .front_matter import _front_matter_lexer, _shebang_lexer
        from .lexers import code_fence_lexer, doctest_lexer, code_lexer

        parser.block.ruler.before("code", "doctest", doctest_lexer)
        parser.block.ruler.disable("code")
        # our indented code captures doctests in indented blocks
        parser.block.ruler.after("doctest", "code", code_lexer)
        parser.disable(FENCE)
        # our code fence captures indent information
        parser.block.ruler.after("code", FENCE, code_fence_lexer)
        # shebang because this markdown is code
        parser.block.ruler.before("table", "shebang", _shebang_lexer)
        parser.block.ruler.before("table", "front_matter", _front_matter_lexer)
        parser.use(footnote.footnote_plugin).use(deflist.deflist_plugin)
        parser.disable("footnote_tail")
        return parser
