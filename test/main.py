from colorama import Fore, Back, Style
from sys import argv
from os import path, getenv
import readline

from computor import Computor

def terminate_with_usage():
	print(Style.BRIGHT + 'usage: ' + Style.RESET_ALL)
	print ('python3 ' + Fore.BLUE + 'main.py ' + Fore.RESET + '-h \t\t\t (usage)')
	print ('python3 ' + Fore.BLUE + 'main.py ' + Fore.RESET + '\t\t\t (interactive mode)')
	print ('python3 ' + Fore.BLUE + 'main.py ' + Fore.RESET + 'statement' + '\t\t (process one statement)')
	print ('python3 ' + Fore.BLUE + 'main.py ' + Fore.RESET + '-f ' + Fore.CYAN + 'filename' + Fore.RESET +
		'\t\t (process all statements in file)')

	print('\nexport ' + Fore.BLUE + 'COMPUTOR_PROMPT' + Fore.RESET + '=' + \
		Fore.GREEN + 'value' + Fore.RESET + ' to set prompt in interactive mode')

	print(Style.BRIGHT + '\n[Built-in Commands]' + Style.RESET_ALL)
	print(Fore.BLUE + '@VARS' + Fore.RESET + '\t\t List all variables')
	print(Fore.BLUE + '@FUNCS' + Fore.RESET + '\t\t List all functions')
	print(Fore.BLUE + '@DANCE' + Fore.RESET + '\t\t ¯\\_(ツ)_/¯')
	print(Fore.BLUE + '@DOGE' + Fore.RESET + '\t\t ¯\\_(ツ)_/¯')

	print(Style.BRIGHT + '\n[Built-in Constants]' + Style.RESET_ALL)
	print(Fore.BLUE + 'i' + Fore.RESET + '\t\t imaginary number')
	print(Fore.BLUE + 'pi' + Fore.RESET + '\t\t natural number')

	print(Style.BRIGHT + '\n[Built-in Functions]' + Style.RESET_ALL)
	print(Fore.BLUE + 'inv(x)' + Fore.RESET + '\t\t multicative inverse')
	print(Fore.BLUE + 'transp(x)' + Fore.RESET + '\t matrix transpose')
	print(Fore.BLUE + 'sqrt(x)' + Fore.RESET + '\t\t square root')
	print(Fore.BLUE + 'sin(radians)' + Fore.RESET + '\t sine')
	print(Fore.BLUE + 'cos(radians)' + Fore.RESET + '\t cosine')
	print(Fore.BLUE + 'tan(radians)' + Fore.RESET + '\t tangent')
	print(Fore.BLUE + 'deg(radians)' + Fore.RESET + '\t convert radians to degrees')
	print(Fore.BLUE + 'rad(degrees)' + Fore.RESET + '\t convert degrees to radians')
	quit()

def interactive_loop(computor):
	prompt = getenv('COMPUTOR_PROMPT')
	if prompt is None or prompt == '':
		prompt = '🍔 Enter statement: '
	while True:
		print()
		statement = input(prompt)
		if statement.strip().upper() == 'EXIT':
			break
		if statement == '' or statement[0] == '#':
			continue
		computor.process_statement(statement)

def process_file(computor, filename):
	base_path = path.dirname(__file__)
	file_path = path.join(base_path, filename)
	with open(file_path, 'r') as file:
		for line in file:
			statement = line.strip()
			if statement == '' or statement[0] == '#':
				print(Fore.MAGENTA + statement + Fore.RESET)
			else:
				computor.process_statement(statement)

def main():
	try:
		computor = Computor()
		# Interactive mode
		if len(argv) == 1:
			interactive_loop(computor)
		# Usage mode
		elif argv[1] == '-h':
			terminate_with_usage()
		# File-processing mode
		elif argv[1] == '-f':
			if len(argv) != 3:
				terminate_with_usage()
			filename = argv[2]
			process_file(computor, filename)
		# Single statement-processing mode
		elif len(argv) == 2:
			statement = argv[1]
			computor.process_statement(statement)
		# Nope mode
		else:
			terminate_with_usage()
	except IOError as e:
		print(Style.BRIGHT + Fore.RED + 'I/O Error: ' + Style.RESET_ALL + Fore.RESET + str(e))

if __name__ == '__main__':
	main()

