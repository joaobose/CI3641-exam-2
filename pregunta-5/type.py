from lark import Lark, Transformer


def return_copy(f):
    def k(*args):
        return f(*args).copy()
    return k


class Type:
    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def kind(self):
        return self.__class__


class ConstType(Type):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def unify(self, other):
        raise Exception(
            f'Error: no se puede unificar {str(other)} con una constante.')

    def copy(self):
        return ConstType(self.token)

    def replacing_var(self, var, value):
        raise Exception(
            f'Error: No se pueden reemplazar valores dentro de una constante.')


class VariableType(Type):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.token

    def unify(self, other):
        raise Exception(
            f'Error: no se puede unificar {str(other)} con una variable sin contexto.')

    def copy(self):
        return VariableType(self.token)

    @return_copy
    def replacing_var(self, var, value):
        if self == var:
            return value
        return self


class FuncType(Type):
    def __init__(self, domain, target):
        self.domain = domain
        self.target = target

    def textual_subs(self, token, substituion):
        pass

    def __str__(self):
        domain_str = f'({str(self.domain)})' if self.domain.kind is FuncType else str(
            self.domain)
        target_str = f'({str(self.target)})' if self.target.kind is FuncType else str(
            self.target)
        # target_str = f'{str(self.target)}' # UNCOMMENT FOR CORRECT PRINT
        return f'{domain_str} -> {target_str}'

    @return_copy
    def unify(self, other):
        if self.domain.kind is ConstType:
            assert other == self.domain, f'Error: no se pudo unificar {str(self.domain)} con {str(other)}'
            return self.target

        if self.domain.kind is VariableType:
            if self.target.kind is ConstType:
                return self.target

            if self.target.kind is VariableType:
                return other

            if self.target.kind is FuncType:
                return self.target.replacing_var(self.domain, other)

        if self.domain.kind is FuncType:
            assert other.kind is FuncType
            ...

    def copy(self):
        return FuncType(self.domain.copy(), self.target.copy())

    def replacing_var(self, var, value):
        copy = self.copy()

        # replacing in domain
        if copy.domain.kind is not ConstType:
            copy.domain = copy.domain.replacing_var(var, value)

        # replacing in target
        if copy.target.kind is not ConstType:
            copy.target = copy.target.replacing_var(var, value)

        return copy


class TypeTransformer(Transformer):
    def const(self, t):
        token, = t
        return ConstType(token)

    def var(self, t):
        token, = t
        return VariableType(token)

    def func(self, val):
        domain, target = val
        return FuncType(domain, target)


class TypeParser:
    def __init__(self):
        self.parser = Lark(r"""
            ?type: func
                | paren
                | CONST -> const
                | VAR   -> var

            CONST : /([A-Z])\w*/
            VAR : /([a-z])\w*/

            func : type "->" type

            ?paren : "(" type ")"

            %import common.WS
            %ignore WS

            """, start='type', parser='lalr', lexer='contextual')

    def parse(self, string):
        return self.parser.parse(string)

    def transform(self, tree):
        return TypeTransformer().transform(tree)

    def inter(self, string):
        return self.transform(self.parse(string))


# # --------------- parse
# to_parse = "(a -> a) -> a"
# transformed = TypeParser().inter(to_parse)
# print(to_parse)

# --------------- unificacion

# # ----- domain constant
# constant_constant = "Int -> Bool"
# constant_constant_t = TypeParser().inter(constant_constant)

# correct_constant = "Int"
# correct_constant_t = TypeParser().inter(correct_constant)

# print(constant_constant_t.unify(correct_constant_t))

# # must fail
# wrong_constant = "Bool"
# wrong_constant_t = TypeParser().inter(wrong_constant)
# print(constant_constant_t.unify(wrong_constant_t))

# # ----- domain variable and target constant
# var_constant = "a -> String"
# var_constant_t = TypeParser().inter(var_constant)

# whatever = "a -> a"
# whatever_t = TypeParser().inter(whatever)

# print(var_constant_t.unify(whatever_t))

# # ----- domain variable and target variable
# var_var = "a -> a"
# var_var_t = TypeParser().inter(var_var)

# whatever = "a -> a"
# whatever_t = TypeParser().inter(whatever)

# print(var_var_t.unify(whatever_t))

# # ----- domain variable and target function
# var_fun = "a -> (b -> (a -> (b -> a)))"
# var_fun_t = TypeParser().inter(var_fun)
# whatever = "Bool"
# whatever_t = TypeParser().inter(whatever)

# print(var_fun_t.unify(whatever_t))

pepe = "Int -> Int -> Int -> Int"
pepe_t = TypeParser().inter(pepe)
print(pepe_t)
