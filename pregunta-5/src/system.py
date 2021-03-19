from .expression import ExpParser, AtomExp, FuncExp
from .type import TypeParser


class TypeSystem:
    def __init__(self):
        self.typ_parser = TypeParser()
        self.exp_parser = ExpParser()

        self.definitions = {}

    # Define un tipo en el sistema
    def define(self, name, string):
        self.definitions[name] = self.typ_parser.inter(string)
        print(f'Se definio "{name}" con tipo {string}')

    # Obtiene el tipo de un Exp a partir de su str
    def type_of(self, string):
        exp = self.exp_parser.inter(string)
        return self.get_type(exp)

    # Obtiene el tipo de un Exp
    def get_type(self, exp):
        if exp.kind is AtomExp:
            if exp.token not in self.definitions:
                raise Exception(
                    f'ERROR: el nombre "{exp.token}" no esta definido.')
            return self.definitions[exp.token]

        if exp.kind is FuncExp:
            fun_type = self.get_type(exp.fun)
            arg_type = self.get_type(exp.arg)
            return fun_type.unify(arg_type)
