from lark import Lark, Transformer


def return_copy(f):
    # Decorador para retonar un deep copy del objeto retonado por f
    # Este docorador supone que f retona un objeto de tipo Type

    def k(*args):
        return f(*args).copy()
    return k


class TypeEcuationTerm:
    # Representa la ecuacion de tipos left = right

    def __init__(self, left, right):
        self.left = left
        self.right = right

    # Retorna la version normalizada de la ecuacion
    def norm(self):
        if self.left is not VariableType:
            return TypeEcuationTerm(self.right, self.left)
        return self

    # Representacion string
    def __str__(self):
        return f'{str(self.left)} = {str(self.right)}'

    # Hash - para trabajar con el tipo set
    def __hash__(self):
        return hash(str(self))

    # Igualdad de ecuaciones
    def __eq__(self, other):
        return str(self) == str(other)


class Type:
    # Clase tipo base

    # La igualda esta dada por la representacion str
    def __eq__(self, other):
        return str(self) == str(other)

    # Definimos la propiedad kind para poder utilizar
    # el operardor is, ie: x is ConstType
    @property
    def kind(self):
        return self.__class__


class ConstType(Type):
    # Clase tipo constante

    def __init__(self, token):
        self.token = token

    # La representacion es su token
    def __str__(self):
        return self.token

    # No se puede unificar un tipo constante
    def unify(self, other):
        raise Exception(
            f'Error: no se puede unificar {str(other)} con una constante.')

    # Copy
    def copy(self):
        return ConstType(self.token)

    # No se puede sustituir dentro de una constante
    def replacing_var(self, var, value):
        raise Exception(
            f'Error: No se pueden reemplazar valores dentro de una constante.')


class VariableType(Type):
    # Tipo valiable

    def __init__(self, token):
        self.token = token

    # La representacion str es su token
    def __str__(self):
        return self.token

    # No se puede unificar un tipo variable sin tener contexto
    def unify(self, other):
        raise Exception(
            f'Error: no se puede unificar {str(other)} con una variable sin contexto.')

    # Copy
    def copy(self):
        return VariableType(self.token)

    # sustitucion textual
    @return_copy
    def replacing_var(self, var, value):
        if self == var:
            return value
        return self


class FuncType(Type):
    # Tipo funcion

    # Tiene el tipo del dominio (domain) y el tipo del rango (target)
    def __init__(self, domain, target):
        self.domain = domain
        self.target = target

    # Representacion str
    def __str__(self):
        domain_str = f'({str(self.domain)})' if self.domain.kind is FuncType else str(
            self.domain)
        target_str = f'{str(self.target)}'
        return f'{domain_str} -> {target_str}'

    # Unificacion sobre una aplicacion
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

            # Ecuacion inicial
            equations = {TypeEcuationTerm(self.domain, other)}
            change = True

            while change:
                # Removemos ecuaciones de la forma X = X
                new_eq = {eq for eq in equations if eq.left != eq.right}

                # Reducimos las ecuaciones de funciones a sub-ecuaciones
                fun_eq = {
                    eq for eq in new_eq if eq.left.kind is FuncType and eq.right.kind is FuncType}
                new_eq = new_eq - fun_eq

                for k in fun_eq:
                    domain_eq = TypeEcuationTerm(
                        k.right.domain, k.left.domain).norm()
                    target_eq = TypeEcuationTerm(
                        k.right.target, k.left.target).norm()
                    new_eq.add(domain_eq)
                    new_eq.add(target_eq)

                # Condicion de cambio
                change = not (new_eq == equations)
                equations = new_eq

            # Buscamos inconsistencias -> Const = Const
            if len({eq for eq in equations if eq.left.kind is ConstType and eq.right.kind is ConstType}) > 0:
                raise Exception(
                    f'Error: no se puede unificar {str(self.domain)} con {str(other)}.')

            # Buscamos inconsistencias
            for eq1 in equations:
                for eq2 in equations:
                    # Circular -> a = b and b = a
                    if eq1.left == eq2.right and eq1.right == eq2.left:
                        raise Exception(
                            f'Error: no se puede unificar {str(self.domain)} con {str(other)}. Referencia circular')

                    # Contradiction -> a = b and a = c
                    if eq1.left == eq2.left and eq1.right != eq2.right:
                        raise Exception(
                            f'Error: no se puede unificar {str(self.domain)} con {str(other)}. Contradiccion')

            # Para este punto, todas las ecuaciones son de la forma
            #   var = t
            # con t.kind is not VariableType and var.kind is VariableType

            # Reemplazamos las ecuaciones resultantes
            result = self.target
            for eq in equations:
                result = result.replacing_var(eq.left, eq.right)

            return result

    # Deep copy
    def copy(self):
        return FuncType(self.domain.copy(), self.target.copy())

    # Sustitucion textual
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
    # Transformer del parser

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
    # Parser de Lark

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


# --------------- parse
to_parse = "a -> a -> a"
transformed = TypeParser().inter(to_parse)
print(to_parse)  # a -> a -> a

# --------------- unificacion

# ----- domain constant
constant_constant = "Int -> Bool"
constant_constant_t = TypeParser().inter(constant_constant)

correct_constant = "Int"
correct_constant_t = TypeParser().inter(correct_constant)

print(constant_constant_t.unify(correct_constant_t))  # Bool

# # must fail
# wrong_constant = "Bool"
# wrong_constant_t = TypeParser().inter(wrong_constant)
# print(constant_constant_t.unify(wrong_constant_t))

# ----- domain variable and target constant
var_constant = "a -> String"
var_constant_t = TypeParser().inter(var_constant)

whatever = "a -> a"
whatever_t = TypeParser().inter(whatever)

print(var_constant_t.unify(whatever_t))  # String

# ----- domain variable and target variable
var_var = "a -> a"
var_var_t = TypeParser().inter(var_var)

whatever = "a -> a"
whatever_t = TypeParser().inter(whatever)

print(var_var_t.unify(whatever_t))  # a -> a

# ----- domain variable and target function
var_fun = "a -> b -> a -> b -> a"
var_fun_t = TypeParser().inter(var_fun)
whatever = "Bool"
whatever_t = TypeParser().inter(whatever)

print(var_fun_t.unify(whatever_t))  # b -> Bool -> b -> Bool

# ----- domain function and target function
fun_fun = "(b -> T) -> (b -> T)"
fun_fun_t = TypeParser().inter(fun_fun)
whatever = "E -> c"
whatever_t = TypeParser().inter(whatever)

print(fun_fun_t.unify(whatever_t))  # E -> T
