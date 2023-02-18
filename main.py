from set import Set
from estado import Estado
from simbolo import Simbolo
from transicion import Transicion
from automata import Automata
from afn import AFN
from postfix import Postfix
from arbol import Arbol

def main():
    expresion = "ab*ab?"
    postfix_expr = Postfix(expresion)

    print("\nExpresión Regular (infix):",postfix_expr.regex)
    print("\nExpresión Regular (postfix):",postfix_expr.postfix)

    tree = Arbol(postfix_expr.postfix)
    tree.print_tree(tree.root, '')

    afn = AFN(tree.root)

    

if __name__ == "__main__":
    main()