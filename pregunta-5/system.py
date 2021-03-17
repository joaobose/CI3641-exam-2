import expression as expr
import type as typ


class TypeSystem:
    def __init__(self):
        self.typ_parser = typ.TypeParser()
        self.exp_parser = expr.ExpParser()

        self.definitions = {}

    def define(self, name, string):
        self.definitions[name] = self.typ_parser.inter(string)

    def type_of(self, string):
        # exp = self.exp_parser.inter(string)
        return self.definitions[string]


s = TypeSystem()
s.define('x', 'T')
s.define('f', 't -> T')
s.define('g', '(a -> a) -> a')

print(s.type_of('x'))
print(s.type_of('f'))
print(s.type_of('g'))
