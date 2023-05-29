import pickle
import pandas as pd
import numpy as np
from simulacion import Simulacion
from prettytable import PrettyTable
from afd_directo import AFD_Directo
from yal_parser import YalParser

def parser():
	with open('./scanner/slr-3_parser.pkl', 'rb') as file:
		serialized_object = file.read()

	yalp = pickle.loads(serialized_object)

	namespace = {} 
	filename = 'slr-3.py' 
	with open(filename, 'r') as file: 
		code = file.read() 
	exec(code, namespace) 
	result = namespace['result']

	print('')
	print('-------- Tabla SLR(1) --------')
	print('')
	print(yalp.table)

	print('')
	m = 4
	n = 4

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

		if ('S' in yalp.table[a][s]):
			t = int(yalp.table[a][s].replace('S',''))
			new_row = {'STACK': stack.copy(), 'SYMBOL': symbol.copy(), 'INPUT': input, 'ACTION': 'SHIFT'}
			df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
			stack.append(t)
			symbol.append(a)
			input = input[1:]
			a = input[0]

		elif ('R' in yalp.table[a][s]):
			t = int(yalp.table[a][s].replace('R',''))
			prod = yalp.productionsOriginal[t-1]
			A = prod[0]
			B = prod[1].split(' ')
			new_row = {'STACK': stack.copy(), 'SYMBOL': symbol.copy(), 'INPUT': input, 'ACTION': 'REDUCE'}
			df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
			for i in range(len(B)):
				if len(stack) > 0:
					stack.pop()
				if len(symbol) > 0:
					symbol.pop()

			t_temp = stack[-1]
			symbol.append(A)
			goto = yalp.table[A][t_temp]
			goto = int(goto.replace('S',''))
			stack.append(goto)

		elif ('ACCEPT' in yalp.table[a][s]):
			new_row = {'STACK': stack.copy(), 'SYMBOL': symbol.copy(), 'INPUT': input, 'ACTION': 'ACCEPT'}
			df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
			break

		else:
			print('')
			print('-------- ERROR --------')
			print('')
			if len(symbol) > 0:
				print('Error Sintáctico: No se esperaba el token ', a,'después de ', symbol[-1])
			else:
				print('Error Sintáctico: No se esperaba el token ', a, 'en la posición 0')
			print('')
			exit()

	print('')
	print('-------- Tabla de Parsing --------')
	print('')
	print(df)

parser()