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
    expresion = "(a|b)cbe((a|b)|z)qwerty"
    postfix_expr = Postfix(expresion)

    print("\nExpresión Regular (infix):",postfix_expr.regex)
    print("\nExpresión Regular (postfix):",postfix_expr.postfix)

    tree = Arbol(postfix_expr.postfix)
    tree.print_tree(postfix_expr.postfix)

    afn = AFN(tree.root)
    Graph(afn, expresion)


if __name__ == "__main__":
    main()