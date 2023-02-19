from set import Set
from estado import Estado
from simbolo import Simbolo
from transicion import Transicion
from automata import Automata
from afn import AFN
from postfix import Postfix
from arbol import Arbol
from graph import Graph

def main():
    expresion = ["ab*ab*", "0?(1?)?0*", "(a*|b*)c", "(b|b)*abb(a|b)*", "(a|ε)b(a+)c?", "(a|b)*a(a|b)(a|b)"]
    opcion = 0

    while True:
        print("\nExpresiones Regulares:")
        for i in range(len(expresion)):
            print(f"\t{i+1}. {expresion[i]}")

        opcion = int(input("\nIngrese el número de la expresión regular a evaluar: "))

        if opcion > 0 and opcion <= len(expresion):
            postfix_expr = Postfix(expresion[opcion-1])
            print("\nExpresión Regular (infix):",postfix_expr.regex)
            print("\nExpresión Regular (postfix):",postfix_expr.postfix)

            tree = Arbol(postfix_expr.postfix)
            #tree.print_tree(postfix_expr.postfix)

            afn = AFN(tree.root)
            Graph(afn, expresion[opcion-1])

            opcion = 0
        else:
            print("\nOpción inválida, intente de nuevo.")

if __name__ == "__main__":
    main()