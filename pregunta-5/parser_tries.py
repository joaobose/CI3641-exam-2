from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF
from arpeggio import RegExMatch as _
from arpeggio import ParserPython


def expr():
    return OneOrMore([atom, (function, "", argument)])


def function():
    return [("(", expr, ")"), atom]


def argument():
    return [("(", expr, ")"), atom]


def atom():
    return _(r'\w+')


def start():
    return expr


parser = ParserPython(start)
x = "f x y"
print(parser.parse(x))
