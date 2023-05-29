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

	print(yalp.table)

parser()