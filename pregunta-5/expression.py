from lark import Lark, Transformer


class Exp:
    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def kind(self):
        return self.__class__


class AtomExp(Exp):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token


class FuncExp(Exp):
    def __init__(self, fun, arg):
        self.fun = fun
        self.arg = arg

    def __str__(self):
        fun_str = f'({str(self.fun)})' if isinstance(
            self.fun, FuncExp) else str(self.fun)
        arg_str = f'({str(self.arg)})' if isinstance(
            self.arg, FuncExp) else str(self.arg)
        return f'{fun_str} {arg_str}'


class ExpTransformer(Transformer):
    def atom(self, t):
        token, = t
        return AtomExp(token)

    def func(self, val):
        fun, arg = val
        return FuncExp(fun, arg)


class ExpParser:
    def __init__(self):
        self.parser = Lark(r"""
            ?expr: func
                | paren
                | ATOM -> atom

            ATOM: /\w+/

            func: expr (" " expr)
            ?paren: "(" expr ")"

            %import common.WS

            """, start='expr')

    def parse(self, string):
        return self.parser.parse(string)

    def transform(self, tree):
        return ExpTransformer().transform(tree)

    def inter(self, string):
        return self.transform(self.parse(string))


x = "if (eq 0 n) 1 n"
transformed = ExpParser().inter(x)
print(transformed)
