import pickle
import pandas as pd
import numpy as np
from simulacion import Simulacion
from prettytable import PrettyTable
from afd_directo import AFD_Directo
from yal_parser import YalParser

def parser():
	with open('./scanner/slr-1_parser.pkl', 'rb') as file:
		serialized_object = file.read()

	yalp = pickle.loads(serialized_object)

	namespace = {} 
	filename = 'slr-1.py' 
	with open(filename, 'r') as file: 
		code = file.read() 
	exec(code, namespace) 
	result = namespace['result']

	print('')
	print('-------- Tabla SLR(1) --------')
	print('')
	print(yalp.table)
	print('')

	m = 4     								# Cantidad de columnas
	n = 4                                   # Cantidad de tokens

	columns = ['STACK', 'SYMBOL', 'INPUT', 'ACTION']

	# array nxm
	data = [[''] * n for _ in range(1)]
	df = pd.DataFrame(data, columns=columns)

	input = []
	for token in result:
		for key in yalp.tokens:
			if token[2] == key[0]:
				if key[1] == 1:
					pass
				else:
					input.append(token[2])
					break

	input.append('$')

	# Inicializar Parsing
	stack = [0]
	input = input
	symbol = []
	a = input[0]

	while(True):
		s = stack[-1]

		if ("S" in yalp.table[a][s]):
			t = int(yalp.table[a][s].replace("S",""))

			new_row = {'STACK': stack.copy(), 'SYMBOL': symbol.copy(), 'INPUT': input[1:], 'ACTION': 'SHIFT'}
			df = df.append(new_row, ignore_index=True)

			symbol.append(a)
			stack.append(t)
			input = input[1:]
			a = input[0]
			print(df)

		


		

			


			




	print('')
	print('-------- Tabla Simulación --------')
	print('')
	print(df)


parser()