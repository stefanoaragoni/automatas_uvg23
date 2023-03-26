from simbolo import Simbolo
import uuid
from graphviz import Digraph
from set import Set

'''
    Arbol de expresiones regulares generado a partir de una expresión regular en postfix.
        Cada nodo del árbol es una instancia de la clase Nodo.
            Cada nodo tiene un valor, y puede tener un hijo izquierdo y un hijo derecho.
            Si el nodo es una hoja, entonces no tiene hijos.
            Si el nodo es un operador, entonces tiene hijo(s). 
                Si el nodo es un operador unario, entonces tiene un hijo.
                    Si el nodo es un operador unario, entonces el hijo es el nodo izquierdo.
                Si el nodo es un operador binario, entonces tiene dos hijos.
                    Si el nodo es un operador binario, entonces el hijo izquierdo es el primer hijo.
                    Si el nodo es un operador binario, entonces el hijo derecho es el segundo hijo.
'''
class Arbol:
    # Constructor
    def __init__(self, regex, root=None):
        self.operators = ['|', '•', '*', '+', '?']
        self.operator_precedence = {'|': 1, '•': 2, '*': 3, '+': 3, '?': 3}
        self.regex = regex

        if root:
            self.root = root
        else:
            self.root = self.construct_tree()

    # Construye el árbol de expresiones regulares
    def construct_tree(self):
        stack = []
        compund = False
        compund_string = ''

        node = None

        # Recorre la expresión regular en postfix
        for char in self.regex:
            if char in self.operators:
                if char == '|':
                    right = stack.pop()
                    left = stack.pop()
                    node = Nodo('|', left, right)
                elif char == '•':
                    right = stack.pop()
                    left = stack.pop()
                    node = Nodo('•', left, right)
                elif char == '*':
                    child = stack.pop()
                    node = Nodo('*', child)
                elif char == '+':
                    child = stack.pop()
                    node = Nodo('•', child, Nodo('*' , child))
                elif char == '?':
                    child = stack.pop()
                    node = Nodo('|', child, Nodo('ε'))
                stack.append(node)

            elif char == "'":
                compund = not compund

                if compund == False and compund_string != '':
                    node = Nodo(compund_string)
                    stack.append(node)
                    compund_string = ''

            else:
                if compund:
                    compund_string += char

                else:
                    node = Nodo(char)
                    stack.append(node)
            
        # Retorna la raíz del árbol
        return stack.pop()

        
    def print_tree(self, regex):
        # Implementacion de Graphviz
        dot = Digraph()

        # Añade los nodos al grafo
        self.add_node(dot, self.root)

        dot.attr(label=regex)

        # Exporta el PDF
        dot.render('tree', view=True)

    def add_node(self, dot, node):
        # Añade nodo al grafo
        dot.node(str(node.id), node.valor)

        # Añadir hijos al grafo
        if node.izq is not None:
            self.add_node(dot, node.izq)
            dot.edge(str(node.id), str(node.izq.id))

        if node.der is not None:
            self.add_node(dot, node.der)
            dot.edge(str(node.id), str(node.der.id))

    def arbol_directo(self):
        arbol_nuevo = Nodo('•', self.root, Nodo('#'))
        return Arbol(self.regex, arbol_nuevo)

'''
    Clase Nodo almacena el valor de un nodo del árbol de expresiones regulares.
'''
class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.id = uuid.uuid4()  # Genera ID unico del Nodo.
        self.valor = valor
        self.izq = izq
        self.der = der

        ascii = 0

        # if valor is longer than 1, it is a compound character
        if len(valor) > 1:
            ascii = valor
        else:
            ascii = ord(valor)

        self.simbolo = Simbolo(ascii, valor)

        self.root = False
        self.analized = False

        self.nullable = False
        self.firstpos = Set()
        self.lastpos = Set()
        self.followpos = Set()

        if (valor != '|' and valor != '•' and valor != '*' and valor != '+' and valor != '?'):
            self.firstpos.AddItem(self.id)
            self.lastpos.AddItem(self.id)           
            

    def find_parent(self, root, node):
        # Si el nodo es la raiz, regresa None.
        if root == node:
            root.root = True
            return root

        # Revisa si el nodo esta en el hijo izquierdo de la raiz.
        if root.izq is not None:
            if root.izq == node:
                return root
            else:
                parent = self.find_parent(root.izq, node)
                if parent is not None:
                    return parent

        # Revisa si el nodo esta en el hijo derecho de la raiz.
        if root.der is not None:
            if root.der == node:
                return root
            else:
                parent = self.find_parent(root.der, node)
                if parent is not None:
                    return parent

        # Si no se encuentra el nodo, regresa None.
        return None

    def find_leftmost_leaf(self, root):
        # Si la raiz no tiene hijos, retorna la raiz.
        if root.izq is None and root.der is None:
            return root

        # Si la raiz tiene un hijo izquierdo, recursivamente recorre su subarbol izquierdo.
        if root.izq is not None:
            return self.find_leftmost_leaf(root.izq)
        
    def nullable_calc(self, node):
        if node.valor == 'ε':
            node.nullable = True
            return node.nullable
        
        elif node.valor == '|':
            izq = self.nullable_calc(node.izq)
            der = self.nullable_calc(node.der)
            node.nullable = izq or der
            return node.nullable
        
        elif node.valor == '•':
            izq = self.nullable_calc(node.izq)
            der = self.nullable_calc(node.der)
            node.nullable = izq and der
            return node.nullable
        
        elif node.valor == '*':
            node.nullable = True
            izq = self.nullable_calc(node.izq)
            return node.nullable
        
        else:
            node.nullable = False
            return node.nullable
    

    def firstpos_calc(self, node):
        if node.valor == '|':
            izq = self.firstpos_calc(node.izq)
            der = self.firstpos_calc(node.der)

            node.firstpos = izq.Union(der)
            return node.firstpos
        
        elif node.valor == '•':
            izq = self.firstpos_calc(node.izq)
            der = self.firstpos_calc(node.der)

            if node.izq.nullable:
                node.firstpos = izq.Union(der)
                return node.firstpos
            
            else:
                node.firstpos = izq
                return node.firstpos
        
        elif node.valor == '*':
            izq = self.firstpos_calc(node.izq)
            node.firstpos = izq
            return node.firstpos
        
        # epsilon or #
        elif node.valor == 'ε':
            node.firstpos = Set()
            return node.firstpos
        
        else:
            return node.firstpos
        
    def lastpos_calc(self, node):
        if node.valor == '|':
            izq = self.lastpos_calc(node.izq)
            der = self.lastpos_calc(node.der)

            node.lastpos = izq.Union(der)
            return node.lastpos
        
        elif node.valor == '•':
            izq = self.lastpos_calc(node.izq)
            der = self.lastpos_calc(node.der)

            if node.der.nullable:
                node.lastpos = der.Union(izq)
                return node.lastpos
            else:
                node.lastpos = der
                return node.lastpos
        
        elif node.valor == '*':
            izq = self.lastpos_calc(node.izq)

            node.lastpos = izq
            return node.lastpos
        
        elif node.valor == 'ε':
            node.lastpos = Set()
            return node.lastpos
        
        else:
            return node.lastpos
        
    def followpos_calc(self, root):
        if root.izq is not None:

            if root.valor == '•':
                self.followpos_calc(root.der)
                self.followpos_calc(root.izq)

                for position in root.izq.lastpos.Elementos:
                    nodo_temp = self.find_node_by_id(root, position)
                    nodo_temp.followpos = nodo_temp.followpos.Union(root.der.firstpos)
                    
            elif root.valor == '*':
                self.followpos_calc(root.izq)
                
                for position in root.lastpos.Elementos:
                    nodo_temp = self.find_node_by_id(root, position)
                    nodo_temp.followpos = nodo_temp.followpos.Union(root.firstpos)

            elif root.valor == '|':
                self.followpos_calc(root.der)
                self.followpos_calc(root.izq)
            
    def find_node_by_id(self, root, id):
        if root.id == id:
            return root

        if root.izq is not None:
            node = self.find_node_by_id(root.izq, id)
            if node is not None:
                return node

        if root.der is not None:
            node = self.find_node_by_id(root.der, id)
            if node is not None:
                return node

        return None


    def print_info_direct_tree(self, root, recursion = True):

        if recursion:
            print("Simbolo \t\t Followpos")
        
        recursion = False
        
        print(root.valor, "\t\t", root.followpos.Elementos)

        # Si la raiz tiene hijos
        if root.izq is not None and root.der is not None:
            self.print_info_direct_tree(root.izq, recursion)
            self.print_info_direct_tree(root.der, recursion)

        # Si la raiz tiene un hijo izquierdo, recursivamente recorre su subarbol izquierdo.
        elif root.izq is not None:
            self.print_info_direct_tree(root.izq, recursion)


