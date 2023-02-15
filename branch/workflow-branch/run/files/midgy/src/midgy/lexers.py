from re import compile

BLOCK, FENCE, PYCON = "code_block", "fence", "pycon"
DOCTEST_CHARS = 62, 62, 62, 32  # >>>S
ELLIPSIS_CHARS = (ord("."),) * 3 + (32,)
MAGIC_CHARS = (37, 37)  # %%
MAGIC = compile("^\s*%{2}\S+")


def code_lexer(state, start, end, silent=False):
    """a code lexer that tracks indents in the token and is aware of doctests"""
    is_magic, min_indent = None, 9999
    if state.sCount[start] - state.blkIndent >= 4:
        first_indent, last_indent, next, last_line = 0, 0, start, start
        while next < end:
            if state.isEmpty(next):
                next += 1
                continue
            if state.sCount[next] - state.blkIndent >= 4:
                begin = state.bMarks[next] + state.tShift[next]
                if is_magic is None:
                    is_magic = state.srcCharCode[begin : begin + 2] == MAGIC_CHARS
                if not is_magic and state.srcCharCode[begin : begin + 4] == DOCTEST_CHARS:
                    break
                if not first_indent:
                    first_indent = state.sCount[next]
                min_indent = min(min_indent, state.sCount[next])
                last_indent, last_line = state.sCount[next], next
                next += 1
            else:
                break
        state.line = last_line + 1
        token = state.push(BLOCK, "code", 0)
        token.content = state.getLines(start, state.line, 4 + state.blkIndent, True)
        token.map = [start, state.line]
        token.meta.update(
            first_indent=first_indent,
            last_indent=last_indent,
            min_indent=min_indent,
            is_magic=is_magic,
            is_doctest=False,
        )
        return True
    return False


def doctest_lexer(state, startLine, end, silent=False):
    """a markdown-it-py plugin for doctests

    doctest are a literate programming convention in python that we
    include in the pidgy grammar. this avoids a mixing python and doctest
    code together.

    the doctest blocks:
    * extend the indented code blocks
    * do not conflict with blockquotes
    * are implicit code fences with the `pycon` info
    * can be replaced with explicit code blocks.
    """
    start = state.bMarks[startLine] + state.tShift[startLine]

    if (state.sCount[startLine] - state.blkIndent) < 4:
        return False

    if state.srcCharCode[start : start + 4] == DOCTEST_CHARS:
        lead, extra, output, closed = startLine, startLine + 1, startLine + 1, False
        indent, next, magic = state.sCount[startLine], startLine + 1, None
        while next < end:
            if state.isEmpty(next):
                break
            if state.sCount[next] < indent:
                break
            begin = state.bMarks[next] + state.tShift[next]
            if state.srcCharCode[begin : begin + 4] == DOCTEST_CHARS:
                break
            next += 1
            if (not closed) and state.srcCharCode[begin : begin + 4] == ELLIPSIS_CHARS:
                extra = next
            else:
                closed = True
                output = next
        state.line = next
        token = state.push(BLOCK, "code", 0)
        token.content = state.getLines(startLine, next, 0, True)
        token.map = [startLine, state.line]
        token.meta.update(
            first_indent=indent,
            last_indent=indent,
            min_indent=indent,
            is_magic=bool(MAGIC.match(token.content.lstrip().lstrip(">").lstrip())),
            is_doctest=True,
            input=[lead, extra],
            output=[extra, output] if extra < output else None,
        )
        return True
    return False


def code_fence_lexer(state, *args, **kwargs):
    from markdown_it.rules_block.fence import fence

    result = fence(state, *args, **kwargs)
    if result:
        token = state.tokens[-1]
        first_indent, last_indent = None, 0
        extent = range(token.map[0] + 1, token.map[1] - 1)
        for next in extent:
            if first_indent is None:
                first_indent = state.sCount[next]
            last_indent = state.sCount[next]
        min_indent = min([state.sCount[i] for i in extent if not state.isEmpty(i)] or [0])

        token.meta.update(
            first_indent=first_indent or 0,
            last_indent=last_indent,
            min_indent=min_indent,
            is_magic_info=bool(MAGIC.match(token.info)),
            is_magic=bool(MAGIC.match(token.content)),
            is_doctest=token.info == PYCON,
        )
    return result
