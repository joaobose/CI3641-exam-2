from lark import Lark, Transformer


class Exp:
    # Clase expresion base

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def kind(self):
        return self.__class__


class AtomExp(Exp):
    # Clase expresion atomica

    def __init__(self, token):
        self.token = token

    # La representacion es su token
    def __str__(self):
        return self.token


class FuncExp(Exp):
    # Clase expresion aplicacion funcional

    def __init__(self, fun, arg):
        self.fun = fun
        self.arg = arg

    # Representacion str
    def __str__(self):
        fun_str = f'({str(self.fun)})' if isinstance(
            self.fun, FuncExp) else str(self.fun)
        arg_str = f'({str(self.arg)})' if isinstance(
            self.arg, FuncExp) else str(self.arg)
        return f'{fun_str} {arg_str}'


class ExpTransformer(Transformer):
    # Transformer del parser

    def atom(self, t):
        token, = t
        return AtomExp(token)

    def func(self, val):
        fun, arg = val
        return FuncExp(fun, arg)


class ExpParser:
    # Parser de Lark (AMBIGUO)

    def __init__(self):
        self.parser = Lark(r"""
            ?expr: func
                | paren
                | ATOM -> atom

            ATOM: /\w+/

            func: (expr " ") expr
            ?paren: "(" expr ")"

            %import common.WS

            """, start='expr')

    def parse(self, string):
        return self.parser.parse(string)

    def transform(self, tree):
        return ExpTransformer().transform(tree)

    def inter(self, string):
        return self.transform(self.parse(string))
