import math


class Arbol:
    # Representacion interna de Arbol.
    # Esto para restringir las formas de construir un Arbol a solo Rama y Hoja.
    class __Representation:
        def __init__(self, value, left=None, right=None):
            self.__value = value
            self.__left = left
            self.__right = right

        # Definimos getters sobre los atributos del arbol.

        @property
        def value(self):
            return self.__value

        @property
        def left(self):
            return self.__left

        @property
        def right(self):
            return self.__right

        # No definimos setters para asegurar que la estructura sea inmutable desde fuera de la representacion.

    # Constructor Hoja a
    @classmethod
    def Hoja(cls, value):
        return cls.__Representation(value)

    # Constructor Rama a (Arbol a) (Arbol a)
    @classmethod
    def Rama(cls, value, left, right):
        return cls.__Representation(value, left, right)

    # Funcion esDeBusqueda
    @staticmethod
    def is_BST(root):
        # Funcion auxiliar, recibe el min y max que deben respetar los valores del arbol.
        def validate(node, low=-math.inf, high=math.inf):
            if not node:
                return True

            # El valor del arbol debe estar entre min y max
            if node.value < low or node.value > high:
                return False

            # Los sub-arboles izquierdo y derecho deben ser validos:
            # - Para sub-arbol derecho:
            #   - Sus valores deben ser mayores o iguales que el valor del padre.
            #   - Sus valores deben ser menores o iguales que high para que los arboles ancestros
            #     cumplan con ser BST.
            # - Para sub-arbol izquierdo:
            #   - Sus valores deben ser menores o iguales que el valor del padre.
            #   - Sus valores deben ser mayores o iguales que low para que los arboles ancestros
            #     cumplan con ser BST.
            return (validate(node.right, node.value, high) and
                    validate(node.left, low, node.value))

        return validate(root)

    # Restriccion de constructores
    def __new__(cls, *args, **kwargs):
        raise Exception(
            "Construcción inválida. Arbol debe construirse a partir de Arbol.Rama ó Arbol.Hoja")


arbol = Arbol.Rama(
    6,
    Arbol.Rama(
        4,
        Arbol.Rama(
            2,
            # Arbol.Hoja(100),
            Arbol.Hoja(1),
            Arbol.Hoja(3)
        ),
        Arbol.Hoja(5)
    ),
    Arbol.Rama(
        9,
        Arbol.Rama(
            8,
            Arbol.Hoja(7),
            Arbol.Hoja(9)
        ),
        Arbol.Rama(
            10,
            Arbol.Hoja(9),
            Arbol.Hoja(11)
        )
    ),
)

print(Arbol.is_BST(arbol))
