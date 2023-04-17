import pickle
from prettytable import PrettyTable
from afd_directo import AFD_Directo
#-------- HEADER
print("Lectura iniciada")
print("Lectura iniciada 2")
a = 55
print(a)
def tokens(token, regla):
	if regla.replace("'", "").replace('"', "") == 'ws':
		return "WHITESPACE"
	if regla.replace("'", "").replace('"', "") == 'id':
		return "ID" if token != "abc" else "ID:ABC"
	if regla.replace("'", "").replace('"', "") == '+':
		return "PLUS"
	if regla.replace("'", "").replace('"', "") == '*':
		return "TIMES"
	if regla.replace("'", "").replace('"', "") == '(':
		return "LPAREN"
	if regla.replace("'", "").replace('"', "") == ')':
		return "RPAREN"
	if regla.replace("'", "").replace('"', "") == '*)':
		return "STARTCOMMENT"

#-------- SIMULACION
with open(f'./scanner/slr-0.pkl', 'rb') as file:
	serialized_object = file.read()

automata = pickle.loads(serialized_object)
resultado = None

def simularAFD(estado, cadena):

	global automata
	global resultado

	if len(cadena) != 0:
		for transicion in automata.transiciones:
			if transicion.estado_origen == estado and transicion.el_simbolo.id.replace("'", "") == str(ord(cadena[0])):
				simularAFD(transicion.estado_destino, cadena[1:])
	if len(cadena) == 0:
		resultado = estado
		return

def simularAFD_Yalex(estado, cadena):

	global automata
	global resultado
	current_state = estado
	last_result = None
	char_set = []
	resultado2 = []
	result_token = None

	for i, char in enumerate(cadena):

		simularAFD(current_state, char)

		while True:
			if resultado:
				current_state = resultado
				char_set.append(char)
				resultado = None
				last_result = True

				if i == len(cadena) - 1:
					token = ''.join(char_set)
					temp_token = (current_state.token.id).replace("'", "").replace('"', "'").replace("#", "")
					result_token = tokens(token, temp_token)
					resultado2.append([result_token, token])

				break

			elif last_result and resultado == None:
				token = ''.join(char_set)
				temp_token = (current_state.token.id).replace("'", "").replace('"', "'").replace("#", "")
				result_token = tokens(token, temp_token)
				resultado2.append([result_token, token])

				current_state = estado
				char_set = []
				last_result = False

				simularAFD(current_state, char)

			else:
				resultado2.append(["Error Lexico", char])
				break

	return resultado2

with open('./yalex/prueba.txt', 'r') as archivo:
	contenido = archivo.read()

resultado2 = simularAFD_Yalex(automata.estado_inicial, contenido)

table = PrettyTable()
table.field_names = ["TOKEN", "VALUE"]
for res in resultado2:
	table.add_row([res[0], res[1]])
print(table)
#-------- TRAILER
print("Lectura finalizada")
print("Stefano Aragoni")
