'''
    Convierte una expresión regular infix a postfix
        Para esto, primero se agrega un punto de concatenacion
        Posteriormente, se convierte a infix eliminando los parentesis
        Finalmente, se convierte a postfix
'''
class Postfix:
    # Constructor
    def __init__(self, regex):
        self.operators = ['|', '.', '*', '+', '?']
        self.operator_precedence = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}
        self.regex = regex
        self.error = False

        self.verify_parenthesis()
        self.regex = self.add_concatenation()
        if not self.error:
            self.verify_regex()
            if not self.error:
                self.postfix = self.to_postfix()

    # Agrega paréntesis de cierre o apertura para balancear la expresión regular.
    def verify_parenthesis(self):
        self.regex = self.regex.replace(' ', '')

        num_open = self.regex.count('(')
        num_close = self.regex.count(')')
        if num_open > num_close:
            self.regex += ')' * (num_open - num_close)
            print("\nDeteccion Error: Se agregaron paréntesis de cierre para balancear la expresión regular.")
        elif num_close > num_open:
            self.regex = '(' * (num_close - num_open) + self.regex
            print("\nDeteccion Error: Se agregaron paréntesis de apertura para balancear la expresión regular.")

        stack = []
        for i, c in enumerate(self.regex):
            if c == '(':
                stack.append(i)
            elif c == ')':
                if len(stack) == 0:
                    print(f"\nDeteccion Error: Se encontro un parentesis de cierre sin su correspondiente apertura en la posición {i}.")
                    self.error = True
                    break
                stack.pop()

        if len(stack) > 0:
            for i in stack[::-1]:
                print(f"\nDeteccion Error: Se encontro un parentesis de apertura sin su correspondiente cierre en la posición {i}.")
                self.error = True
                break


    # Agrega un punto de concatenación entre caracteres
    def add_concatenation(self):
        new_regex = ''
        for i, char in enumerate(self.regex):
            new_regex += char
            if i+1 < len(self.regex):
                if (char not in ['(', '|'] and self.regex[i+1] not in [')', '|', '*', '+', '?']) or (char == ')' and self.regex[i+1] not in ['|', '*', '+', '?', ')']) or (char == '*' and self.regex[i+1] not in ['|', '*', '+', '?', ')']) or (char == '+' and self.regex[i+1] not in ['|', '*', '+', '?', ')']) or (char == '?' and self.regex[i+1] not in ['|', '*', '+', '?', ')']):
                    if self.regex[i+1] != ')' or char != '(':
                        new_regex += '.'
        return new_regex

    # Verifica que la expresión regular infix sea válida; si no lo es, lanza una excepción
    def verify_regex(self):
        if self.regex == '':
            print('La expresión regular no puede estar vacía.')
            self.error = True
            return
        if self.regex[0] in self.operators:
            print('La expresión regular infix no puede iniciar con un operador.')
            self.error = True
            return

        simbolos_binarios = ['|', '.']
        simbolos_unarios = ['*', '+', '?']
        for i, char in enumerate(self.regex):
            if i+1 < len(self.regex):
                if char == ')' and self.regex[i+1] == '(':
                    print('La expresión regular infix no puede tener dos expresiones seguidas sin operador.')
                    self.error = True
                    break
                
                if char in simbolos_binarios and self.regex[i+1] in simbolos_binarios:
                    print('La expresión regular infix no puede tener dos operadores seguidos como ".", "|".')
                    self.error = True
                    break
                
                if char in simbolos_binarios and self.regex[i+1] == ')':
                    print('La expresión regular infix no puede tener un operador seguido de un paréntesis de cierre.')
                    self.error = True
                    break

                if (char == '(' and self.regex[i+1] in simbolos_unarios) or (char == '(' and self.regex[i+1] in simbolos_binarios):
                    print('La expresión regular infix no puede tener un paréntesis de apertura seguido de un operador.')
                    self.error = True
                    break

                if (char == '(' and self.regex[i+1] == ')'):
                    print('La expresión regular infix no puede tener un paréntesis de apertura seguido de un paréntesis de cierre.')
                    self.error = True
                    break

                if char in simbolos_binarios and self.regex[i+1] in simbolos_unarios:
                    print('La expresión regular infix no puede tener un operador seguido de un operador unario como "*", "+", "?".')
                    self.error = True
                    break

        if self.regex[-1] in ['|', '.']:
            print('La expresión regular infix no puede terminar con un operador como ".", "|".')
            self.error = True
            
        if self.regex.count('(') != self.regex.count(')'):
            print('Los paréntesis de la expresión regular no están balanceados.')
            self.error = True

        if self.regex.count('[') > 1 or self.regex.count(']') > 1:
            print('La expresión regular no puede tener más de un conjunto de caracteres. Ejemplo: "[]" o "()", no ambos.')
            self.error = True

    # Basado en el algoritmo de Shunting-yard
    def to_postfix(self):
        output_queue = []
        operator_stack = []
        for char in self.regex:
            if char in self.operators:
                while operator_stack and operator_stack[-1] != '(' and self.operator_precedence[char] <= self.operator_precedence[operator_stack[-1]]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(char)
            elif char == '(':
                operator_stack.append('(')
            elif char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
            else:
                output_queue.append(char)
        while operator_stack:
            output_queue.append(operator_stack.pop())
        return ''.join(output_queue)
