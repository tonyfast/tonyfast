from enum import Enum
from re import compile

__all__ = ("load",)
SHEBANG = compile("^#!\s*(?P<interpreter>\S+)\s*(?P<command>.*)")


FM = Enum("FM", {"yaml": "-", "toml": "+"})


def strip_and_classifiy(x):
    x = x.strip()
    return FM(x[0]), "".join(x.splitlines(True)[1:-1])


def load(x):
    """load front matter including the delimiters.

    --- and +++ reference yaml and toml front matter respectively."""
    kind, x = strip_and_classifiy(x)
    return {FM.toml: load_toml, FM.yaml: load_yaml}[kind](x)


def load_toml(x):
    from tomli import loads

    return loads(x)


def load_yaml(x):
    return _get_yaml_loader()(x)


def _get_yaml_loader():
    loader = getattr(_get_yaml_loader, "loader", None)
    if loader:
        return loader
    try:
        from ruamel.yaml import safe_load as load
    except ModuleNotFoundError:
        try:
            from yaml import safe_load as load
        except ModuleNotFoundError:
            from json import loads as load
    _get_yaml_loader.loader = load
    return load


def _shebang_lexer(state, startLine, endLine, silent):
    start = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    # our front matter allows for indents and can occur at positions
    # other than 0
    # this should filter out non-front matter
    if state.tokens:
        return False

    m = SHEBANG.match(state.src[start:maximum])
    if not m:
        return False

    parent = state.parentType
    line_max = state.lineMax

    # this will prevent lazy continuations from ever going past our end marker
    state.lineMax = startLine

    token = state.push("shebang", "", 0)
    token.hidden = True
    token.content = state.getLines(startLine, startLine + 1, 0, True)
    token.block = True

    state.parentType = parent
    state.lineMax = line_max
    state.line = startLine + 1
    token.map = [startLine, state.line]

    return True


def _front_matter_lexer(state, startLine, endLine, silent):
    auto_closed = False
    start = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]
    src_len = len(state.src)
    if state.tokens:
        if len(state.tokens) == 1:
            if state.tokens[0].type != "shebang":
                return False

    # our front matter allows for indents and can occur at positions
    # other than 0
    # this should filter out non-front matter

    if state.sCount[startLine]:
        return False

    if state.tokens:
        if len(state.tokens) > 1:
            return False
        if state.tokens[-1].type != "shebang":
            return False

    markup = None
    if state.srcCharCode[start] == ord("-"):
        markup = "-"
    elif state.srcCharCode[start] == ord("+"):
        markup = "+"
    else:
        return False

    if state.srcCharCode[start + 1 : maximum] != tuple(map(ord, (markup, markup))):
        return False

    # Search for the end of the block
    nextLine = startLine

    while True:
        nextLine += 1
        if nextLine >= endLine:
            return False

        start = state.bMarks[nextLine] + state.tShift[nextLine]
        maximum = state.eMarks[nextLine]

        if start < maximum and state.sCount[nextLine] < state.blkIndent:
            break

        if ord(markup) != state.srcCharCode[start]:
            continue

        if state.sCount[nextLine] - state.blkIndent >= 4:
            continue

        if state.srcCharCode[start + 1 : maximum] == tuple(map(ord, (markup, markup))):
            auto_closed = True
            nextLine += 1
            break

    parent = state.parentType
    line_max = state.lineMax
    state.parentType = "container"

    # this will prevent lazy continuations from ever going past our end marker
    state.lineMax = nextLine

    token = state.push("front_matter", "", 0)
    token.hidden = True
    token.markup = markup
    token.content = state.getLines(startLine, nextLine, 0, True)
    token.block = True

    state.parentType = parent
    state.lineMax = line_max
    state.line = nextLine
    token.map = [startLine, state.line]

    return True
