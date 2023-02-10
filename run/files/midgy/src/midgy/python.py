"""the Python class that translates markdown to python code"""
from dataclasses import dataclass, field
from io import StringIO
from copy import copy
from functools import partial
from .render import Renderer, escape, FENCE, SP, QUOTES
from .lexers import MAGIC
from typing import Tuple
DEFAULT_FENCE_LANGS = "python", "ipython"

@dataclass
class Python(Renderer):
    """a line-for-line markdown to python translator"""

    # include markdown as docstrings of functions and classes
    include_docstring: bool = True
    # include docstring as a code block
    include_doctest: bool = False
    # include front matter as a code block
    include_front_matter: bool = True
    # include markdown in that code as strings, (False) uses comments
    include_markdown: bool = True
    # code fence languages that indicate a code block
    include_code_fences: Tuple[str] = field(default_factory=partial(copy, DEFAULT_FENCE_LANGS))
    include_magic: bool = True

    front_matter_loader = '__import__("midgy").front_matter.load'
    QUOTE = QUOTES[0]

    def code_block(self, token, env):
        if token.meta["is_doctest"]:
            if self.include_doctest:
                yield from self.code_block_doctest(token, env)
        elif self.include_indented_code:
            yield from self.non_code(env, token)
            yield from self.code_block_body(self.get_block(env, token.map[1]), token, env)
            self.get_updated_env(token, env)

    def code_block_body(self, block, token, env):
        if token.meta["is_doctest"]:
            block = self.get_block_sans_doctest(block)
        if self.is_magic(token):
            block = self.code_block_magic(block, token.meta["min_indent"], env)
        yield from self.dedent_block(block, (not token.meta["is_magic"]) * env["min_indent"])

    def code_block_doctest(self, token, env):
        yield from self.non_code(env, token)
        yield from self.code_block_body(self.get_block(env, token.meta["input"][1]), token, env)
        if token.meta["output"]:
            block = self.get_block(env, token.meta["output"][1])
            block = self.dedent_block(block, token.meta["min_indent"])
            yield from self.comment(block, env)
        self.get_updated_env(token, env, colon_block=False, quoted_block=False, continued=False)

    def code_block_magic(self, block, indent, env, dedent=True):
        line = next(block)
        left = line.rstrip()
        # split magic name and arguments
        program, _, args = left.lstrip().lstrip("%").partition(" ")
        # add whitespace relative to the indents allowing for condition magics
        yield SP * self.get_computed_indent(env)
        # prefix the ipython run cell magic caller
        yield from ("get_ipython().run_cell_magic('", program, "', '")
        yield from (args, "',", line[len(left) :])
        if dedent:
            block = self.dedent_block(block, indent)
        # quote the block of the cell body
        yield from self.get_wrapped_lines(block, lead=self.QUOTE, trail=self.QUOTE + ")")

    def comment(self, block, env):
        yield from self.get_wrapped_lines(block, pre=SP * self.get_computed_indent(env) + "# ")

    def dedent_block(self, block, dedent):
        yield from (x[dedent:] for x in block)

    def fence(self, token, env):
        """the fence renderer is pluggable.

        if token_{token.info} exists then that method is called to render the token"""

        if token.info:
            method = getattr(self, f"fence_{token.info}", None)
            if method:
                return method(token, env)
            
            if token.meta["is_magic_info"]:
                return self._fence_info_magic(token, env)

    # def _flush_magic(self):

    def _fence_info_magic(self, token, env):
        """return a modified code fence that identifies as code"""

        yield from self.non_code(env, token)
        line = next(self.get_block(env, token.map[0]+1))
        left = line.rstrip()
        right = left.lstrip()
        markup = right[0]
        program, _, args = right.lstrip("`~").lstrip("%").partition(" ")
        yield from ("get_ipython().run_cell_magic('", program, "', '")
        yield from (args, "', # ", markup * 3 , line[len(left) :])

        block = self.get_block(env, token.map[1] - 1)
        block = self.dedent_block(block, token.meta["min_indent"])       
        yield from self.get_wrapped_lines(block, lead=self.QUOTE, trail=self.QUOTE + ")")

        self.get_updated_env(token, env)
        yield from self.comment(self.get_block(env, token.map[1]), env)

    def fence_python(self, token, env):
        """return a modified code fence that identifies as code"""
        if token.info in self.include_code_fences:
            yield from self.non_code(env, token)
            yield from self.comment(self.get_block(env, token.map[0] + 1), env)
            block = self.get_block(env, token.map[1] - 1)
            yield from self.code_block_body(block, token, env)
            self.get_updated_env(token, env)
            yield from self.comment(self.get_block(env, token.map[1]), env)

    fence_ipython = fence_python

    def front_matter(self, token, env):
        """comment, codify, or stringify blocks of front matter"""
        if self.include_front_matter:
            lead = f"locals().update({self.front_matter_loader}(" + self.QUOTE
            trail = self.QUOTE + "))"
            body = self.get_block(env, token.map[1])
            yield from self.get_wrapped_lines(body, lead=lead, trail=trail)
        else:
            yield from self.comment(self.get_block(env, token.map[1]), env)

    def get_block_sans_doctest(self, block):
        for line in block:
            right = line.lstrip()
            if right:
                line = line[: len(line) - len(right)] + right[4:]
            yield line

    def get_computed_indent(self, env):
        """compute the indent for the first line of a non-code block."""
        next = env.get("next_code")
        next_indent = next.meta["first_indent"] if next else 0
        spaces = prior_indent = env.get("last_indent", 0)
        if env.get("colon_block", False):  # inside a python block
            if next_indent > prior_indent:
                spaces = next_indent  # prefer greater trailing indent
            else:
                spaces += 4  # add post colon default spaces.
        min_indent = env.get("min_indent", 0)
        return max(spaces, min_indent) - min_indent

    def get_wrapped_lines(self, lines, lead="", pre="", trail="", continuation=""):
        """a utility function to manipulate a buffer of content line-by-line."""
        # can do this better with buffers
        ws, any, continued = "", False, False
        for line in lines:
            LL = len(line.rstrip())
            if LL:
                continued = line[LL - 1] == "\\"
                LL -= 1 * continued
                if any:
                    yield ws
                else:
                    for i, l in enumerate(StringIO(ws)):
                        yield from (pre, l[:-1], continuation, l[-1])
                yield from (pre, lead, line[:LL])
                lead, any, ws = "", True, line[LL:]
            else:
                ws += line
        if any:
            yield trail
        if continued:
            for i, line in enumerate(StringIO(ws)):
                yield from (i and pre or "", line[:-1], i and "\\" or "", line[-1])
        else:
            yield ws

    def is_magic(self, token):
        if self.include_magic and token.meta["is_magic"]:
            return True
        return token.type == FENCE and token.info == "ipython"

    def non_code(self, env, next=None):
        block = super().non_code(env, next)
        if self.include_markdown:
            lead = trail = "" if env.get("quoted_block", False) else self.QUOTE
            lead = SP * self.get_computed_indent(env) + lead
            trail += "" if next else ";"
            continued = env.get("continued") and "\\" or ""
            yield from self.get_wrapped_lines(
                map(escape, block), lead=lead, trail=trail, continuation=continued
            )
        else:
            yield from self.comment(block, env)

    def render(self, src):
        if MAGIC.match(src):
            from textwrap import dedent

            return "".join(self.code_block_magic(StringIO(dedent(src)), 0, {}))
        return super().render(src)

    def shebang(self, token, env):
        yield from self.get_block(env, token.map[1])
