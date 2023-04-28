import pickle
from simulacion import Simulacion
from prettytable import PrettyTable
from afd_directo import AFD_Directo


#-------- TOKENS
def tokens(regla, token):
	if regla.replace("'", "").replace('"', "") == 'espacioEnBlanco':
		return None
	if regla.replace("'", "").replace('"', "") == 'identificador':
		return "Identificador"
	if regla.replace("'", "").replace('"', "") == 'numero':
		return "Número"
	if regla.replace("'", "").replace('"', "") == '+':
		return "Operador de suma"
	if regla.replace("'", "").replace('"', "") == '-':
		return "Operador de menus"
	if regla.replace("'", "").replace('"', "") == '*':
		return "Operador de multiplicación"
	if regla.replace("'", "").replace('"', "") == '=':
		return "Operador de asignación"
	else:
		return 'Error: Token no definido!'


#-------- SIMULACION
def simulacion():
	with open(f'./scanner/slr-5.pkl', 'rb') as file:
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

	return resultado

simulacion()
