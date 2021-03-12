from functools import reduce


class Church:
    # Representacion interna de un numero de Church.
    # Esto para restringir las formas de construir un numero Church a solo zero y succ n.
    class __Representation:
        def __init__(self, fn):
            # Representamos un numero Church por una lambda function.
            # La forma de esta funcion sigue la defincion dada en el lambda calculo.
            self.__fn = fn

        # Definimos un getter para la funcion representativa.
        # No definimos setter para asegurar que su valor sea inmutable fuera de la representacion.
        @property
        def fn(self):
            return self.__fn

        # Sobrecargamos la llamada de un numero Church.
        # La llamada a un numero Church retorna su equivalente int.
        def __call__(self):
            return self.fn(lambda x: x + 1)(0)

        # Sobrecargamos la suma de numeros de Church.
        # Utilizamos la definicion de suma dada por el lambda calculo.
        def __add__(self, other):
            return self.__class__(lambda f: lambda x: self.fn(f)(other.fn(f)(x)))

        # Sobrecargamos la multiplicacion de numeros de Church.
        # Utilizamos la definicion de multiplicacion dada por el lambda calculo.
        def __mul__(self, other):
            return self.__class__(lambda f: lambda x: self.fn(other.fn(f))(x))

        # Sobrecargamos la representacion String de un numero Church.
        # Esto para llamar print con comodidad sobre numeros de Church.
        def __str__(self):
            return str(self())

    # Constructor cero (0)
    @classmethod
    def zero(cls):
        return cls.__Representation(lambda f: lambda x: x)

    # Contructor Succ Church
    @classmethod
    def succ(cls, n):
        return cls.__Representation(lambda f: lambda x: f(n.fn(f)(x)))

    # Contructor from_int
    # Este constructor no se encontraba en el enunciado.
    # Sin embargo, considero que es interesante.
    @classmethod
    def from_int(cls, n):
        return reduce(lambda x, _: Church.succ(x), range(n), Church.zero())

    # Restriccion de constructores
    def __new__(cls, *args, **kwargs):
        raise Exception(
            "Construcción inválida. Church debe construirse a partir de Church.zero, Church.succ ó Church.from_int")


zero = Church.zero()
one = Church.succ(zero)
two = Church.succ(one)
print(two)  # 2

three = one + two
print(three)  # 3
print((two + three) * three)  # 15

sixtynine = Church.from_int(69)
print(sixtynine)  # 69
print((sixtynine * two + sixtynine) * three)  # 621
