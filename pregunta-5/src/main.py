from .system import TypeSystem

system = TypeSystem()

while True:
    args = input("Introduzca su comando: ").split(" ", 1)

    command = args[0]

    if command == 'SALIR':
        break

    rest = args[1]

    try:
        if command == 'DEF':
            args = rest.split(" ", 1)
            nombre = args[0]
            tipo = args[1]
            system.define(nombre, tipo)
            continue

        if command == 'TIPO':
            print(system.type_of(rest))
            continue
    except Exception as error:
        print(error)
