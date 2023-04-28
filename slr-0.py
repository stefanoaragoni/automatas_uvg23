import pickle
from simulacion import Simulacion
from prettytable import PrettyTable
from afd_directo import AFD_Directo
#-------- HEADER
print("Lectura iniciada")
print("Lectura iniciada 2")
a = 55
print(a)


#-------- TOKENS
def tokens(regla, token):
	if regla.replace("'", "").replace('"', "") == 'ws':
		return "WHITESPACE"
	if regla.replace("'", "").replace('"', "") == 'id':
		print("Hola!")
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
	else:
		return 'Error: Token no definido!'


#-------- SIMULACION
def simulacion():
	with open(f'./scanner/slr-0.pkl', 'rb') as file:
		serialized_object = file.read()

	automata = pickle.loads(serialized_object)
	resultado = None

	with open('./yalex/prueba.txt', 'r') as archivo:
		contenido = archivo.read()

	resultado = Simulacion(automata, contenido, 'Yalex').resultado
	for res in resultado:
		res_token = tokens(res[0], res[1])
		res.append(res_token)

	table = PrettyTable()
	table.field_names = ["TOKEN", "VALUE","RESULT"]
	for res in resultado:
		table.add_row([res[0], res[1], res[2]])
	print(table)

	#-------- TRAILER
	print("Lectura finalizada")
	print("Stefano Aragoni")

	return resultado

simulacion()
