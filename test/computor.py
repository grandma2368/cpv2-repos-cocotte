from colorama import Fore, Back, Style
from math import sin, cos, tan, pi
from os import system

from function import Function
from variable import Variable

from complex import Complex
from matrix import Matrix

from parser import Parser
from simplifier import Simplifier
# from evaluator import Evaluator
import evaluator
from solver import Solver
from exceptions import ParserException, ComputorException

class Computor:
	instance = None
	imag = Complex(0.0, 1.0)
	pi = pi		# Computor.pi = math.pi

	def __init__(self):
		if Computor.instance is None:
			Computor.instance = self
			self.__parser = Parser()
			self.__simplifier = Simplifier()
			self.__evaluator = evaluator.Evaluator()
			self.__solver = Solver()
			self.__vars = {}
			self.__funcs = {}
			self.__local_vars = []		# list of tuple (name, value), to be used as stack
		else:
			raise ComputorException('Computor.instance already instantiated')

	# TOP LEVEL OPERATIONS ------------------------------------

	def process_statement(self, statement):
		try:
			if '@SOLVE' in statement:
				self.__solver.solve(statement)
			else:
				result = self.__parser.parse(statement)
				if result is not None:
					print(result)
		except OverflowError as e:
			print(Style.BRIGHT + Fore.RED + 'OverflowError: ' + Style.RESET_ALL + Fore.RESET + str(e))
		except RecursionError as e:
			print(Style.BRIGHT + Fore.RED + 'RecursionError: ' + Style.RESET_ALL + Fore.RESET + str(e))
		except ParserException as e:
			print(Style.BRIGHT + Fore.RED + 'ParserException: ' + Style.RESET_ALL + Fore.RESET + str(e))
		except ComputorException as e:
			print(Style.BRIGHT + Fore.RED + 'ComputorException: ' + Style.RESET_ALL + Fore.RESET + str(e))
		finally:
			self.__local_vars.clear()

	def eval(self, expr):
		return self.__evaluator.eval(expr)

	def compact_str(self, value):
		if isinstance(value, Matrix):
			return value.get_compact_str()
		else:
			return str(value)

	def set_var(self, var_name, value):
		var_name_lc = var_name.lower()
		self.__vars[var_name_lc] = Variable(var_name, value)
		print(value)

	def get_var(self, var_name):
		var_name_lc = var_name.lower()
		# Search in stack of local variables
		for local_var in reversed(self.__local_vars):
			if local_var[0].lower() == var_name_lc:
				return local_var[1]
		# Search in dictionary of global variables
		if var_name_lc in self.__vars:
			return self.__vars[var_name_lc].value
		raise ComputorException('Variable \'' + Fore.BLUE + var_name + Fore.RESET + '\' is not defined')

	def resolve_var(self, var_name):
		var_name_lc = var_name.lower()
		# Search in stack of local variables
		# if found, return the variable name as string
		for local_var in reversed(self.__local_vars):
			if local_var[0].lower() == var_name_lc:
				return var_name
		# Search in dictionary of global variables
		# if found, return the variable's value
		if var_name_lc in self.__vars:
			return self.__vars[var_name_lc].value
		raise ComputorException('Variable \'' + Fore.BLUE + var_name + Fore.RESET + '\' is not defined')

	def set_func(self, func_name, local_vars, expr):
		func_name_lc = func_name.lower()
		function = Function(func_name, local_vars, expr)

		# push local variables on stack
		for var_name in function.local_vars:
			self.__local_vars.append((var_name, None))

		# simplify the function
		function.expr = self.__simplifier.simplify(function.expr)

		# pop local variables from stack
		for _ in self.__local_vars:
			self.__local_vars.pop()

		self.__funcs[func_name_lc] = function
		print(function)

	def get_func(self, func_name):
		func_name_lc = func_name.lower()
		if func_name_lc in self.__funcs:
			return (self.__funcs[func_name_lc])
		else:
			raise ComputorException('Function \'' + Fore.GREEN + func_name + Fore.RESET + '\' is not defined')

	def validate_func(self, func_name, num_args):
		func_name_lc = func_name.lower()
		# check name matches
		if func_name_lc in self.__funcs:
			function = self.__funcs[func_name_lc]
			# check number of args match
			if len(function.local_vars) == num_args:
				return
		raise ComputorException('No such function: ' + Fore.BLUE + func_name + Fore.RESET)

	def show_func(self, func_name, args):
		func_name = func_name.lower()
		# check if func_name matches
		if func_name in self.__funcs:
			function = self.__funcs[func_name]
			# check if args match
			if len(function.local_vars) == len(args) and \
				all([ x.lower() == y.lower() for x, y in zip(function.local_vars, args) ]):
				print(function)
				return
		raise ComputorException('No such function: ' + Fore.BLUE + func_name + '(' + ', '.join(args) + ')' + Fore.RESET)

	def eval_function(self, func_name, args):
		function = self.get_func(func_name)

		if len(function.local_vars) != len(args):
			raise ComputorException('Invalid parameters for ' + str(function))

		# push local variables on stack
		for var_name, value in zip(function.local_vars, args):
			self.__local_vars.append((var_name, value))

		# evaluate
		# result = self.__parser.parse(function.expr)
		result = self.__evaluator.eval(function.expr)

		# pop local variables from stack
		for _ in self.__local_vars:
			self.__local_vars.pop()

		return result

	def show_vars(self):
		print(Style.BRIGHT + '[VARIABLES]' + Style.RESET_ALL)
		for _, value in self.__vars.items():
			print(value)

	def show_funcs(self):
		print(Style.BRIGHT + '[FUNCTIONS]' + Style.RESET_ALL)
		for _, value in self.__funcs.items():
			print(value)

	def dance(self):
		dance_str = r'''(_＼ヽ
　 ＼＼ .Λ＿Λ.
　　 ＼(　ˇωˇ)　
　　　 >　⌒ヽ
　　　/ 　 へ＼
　　 /　　/　＼＼
　　 ﾚ　ノ　　 ヽ_つ
　　/　/
　 /　/|
　(　(ヽ
　|　|、＼
　| 丿 ＼ ⌒)
　| |　　) /
`ノ ) 　 Lﾉ
(_／'''
		print(dance_str)

	# Source: https://github.com/thiderman/doge
	def doge(self):
		system('doge')

	# OPERATORS ------------------------------------

	def add(self, a, b):
		if isinstance(a, float):
			if isinstance(b, float):
				return a + b
			elif isinstance(b, Complex):
				return Complex.add(Complex(a), b)
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Rational + Matrix')
		elif isinstance(a, Complex):
			if isinstance(b, float):
				return Complex.add(a, Complex(b))
			elif isinstance(b, Complex):
				return Complex.add(a, b)
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Complex + Matrix')
		elif isinstance(a, Matrix):
			if isinstance(b, float):
				raise ComputorException('Illegal operation: Matrix + Rational')
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Matrix + Complex')
			elif isinstance(b, Matrix):
				return Matrix.add(a, b)
		raise ComputorException('Computor.add(): something bad happened 🤷')

	def sub(self, a, b):
		if isinstance(a, float):
			if isinstance(b, float):
				return a - b
			elif isinstance(b, Complex):
				return Complex.sub(Complex(a), b)
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Rational - Matrix')
		elif isinstance(a, Complex):
			if isinstance(b, float):
				return Complex.sub(a, Complex(b))
			elif isinstance(b, Complex):
				return Complex.sub(a, b)
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Complex - Matrix')
		elif isinstance(a, Matrix):
			if isinstance(b, float):
				raise ComputorException('Illegal operation: Matrix - Rational')
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Matrix - Complex')
			elif isinstance(b, Matrix):
				return Matrix.sub(a, b)
		raise ComputorException('Computor.sub(): something bad happened 🤷')

	def mat_mul(self, a, b):
		if isinstance(a, Matrix) and isinstance(b, Matrix):
			return Matrix.mat_mul(a, b)
		else:
			raise ComputorException('**: both operands must be Matrix')

	def mat_mul(self, a, b):
		if isinstance(a, float):
			if isinstance(b, float):
				raise ComputorException('Illegal operation: Rational ** Rational')
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Rational ** Complex')
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Rational ** Matrix')
		elif isinstance(a, Complex):
			if isinstance(b, float):
				raise ComputorException('Illegal operation: Complex ** Rational')
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Complex ** Complex')
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Complex ** Matrix')
		elif isinstance(a, Matrix):
			if isinstance(b, float):
				raise ComputorException('Illegal operation: Matrix ** Rational')
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Matrix ** Complex')
			elif isinstance(b, Matrix):
				return Matrix.mat_mul(a, b)
		raise ComputorException('Computor.mat_mul(): something bad happened 🤷')

	def mul(self, a, b):
		if isinstance(a, float):
			if isinstance(b, float):
				return a * b
			elif isinstance(b, Complex):
				return Complex.mul(Complex(a), b)
			elif isinstance(b, Matrix):
				return Matrix.scalar_mul(a, b)
		elif isinstance(a, Complex):
			if isinstance(b, float):
				return Complex.mul(a, Complex(b))
			elif isinstance(b, Complex):
				return Complex.mul(a, b)
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Complex * Matrix')
		elif isinstance(a, Matrix):
			if isinstance(b, float):
				return Matrix.scalar_mul(b, a)
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Matrix * Complex')
			elif isinstance(b, Matrix):
				return Matrix.element_mul(a, b)
		raise ComputorException('Computor.mul(): something bad happened 🤷')

	def div(self, a, b):
		if isinstance(a, float):
			if isinstance(b, float):
				if b == 0:
					raise ComputorException('Division by zero')
				return a / b
			elif isinstance(b, Complex):
				return Complex.div(Complex(a), b)
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Rational / Matrix')
		elif isinstance(a, Complex):
			if isinstance(b, float):
				return Complex.div(a, Complex(b))
			elif isinstance(b, Complex):
				return Complex.div(a, b)
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Complex / Matrix')
		elif isinstance(a, Matrix):
			if isinstance(b, float):
				if b == 0:
					raise ComputorException('Division by zero')
				return Matrix.scalar_mul(1 / b, a)
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Matrix / Complex')
			elif isinstance(b, Matrix):
				return Matrix.mat_mul(a, b.get_inverse())
		raise ComputorException('Computor.div(): something bad happened 🤷')

	def mod(self, a, b):
		if isinstance(a, float):
			if isinstance(b, float):
				if not (a.is_integer() and b.is_integer()):
					raise ComputorException('Illegal operation: ' + str(a) + ' % ' + str(b))
				return a % b
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Rational % Complex')
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Rational % Matrix')
		elif isinstance(a, Complex):
			if isinstance(b, float):
				raise ComputorException('Illegal operation: Complex % Rational')
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Complex % Complex')
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Complex % Matrix')
		elif isinstance(a, Matrix):
			if isinstance(b, float):
				raise ComputorException('Illegal operation: Matrix % Rational')
			elif isinstance(b, Complex):
				raise ComputorException('Illegal operation: Matrix % Complex')
			elif isinstance(b, Matrix):
				raise ComputorException('Illegal operation: Matrix % Matrix')
		raise ComputorException('Computor.mul(): something bad happened 🤷')

	def pow(self, base, power):
		if not (isinstance(power, float) and power.is_integer() and int(power) >= 0):
			raise ComputorException('Exponent ' + Fore.RED + str(power) + Fore.RESET + ' must be a non-negative integer')
		power = int(power)
		if isinstance(base, float):
			return base ** power
		elif isinstance(base, Complex):
			return Complex.pow(base, power)
		elif isinstance(base, Matrix):
			return Matrix.pow(base, power)
		raise ComputorException('Computor.pow(): something bad happened 🤷')

	def neg(self, a):
		if isinstance(a, float):
			return -a
		elif isinstance(a, Complex):
			return Complex.neg(a)
		elif isinstance(a, Matrix):
			return Matrix.neg(a)
		raise ComputorException('Computor.neg(): something bad happened 🤷')

	# BUILT-IN FUNCTIONS ------------------------------------

	def inv(self, a):
		if isinstance(a, float):
			return self.div(1.0, a)
		elif isinstance(a, Complex):
			return self.div(1.0, a)
		elif isinstance(a, Matrix):
			return a.get_inverse()
		raise ComputorException('Computor.inv(): something bad happened 🤷')

	def transp(self, a):
		if isinstance(a, float):
			raise ComputorException('Illegal operation: transp(Rational)')
		elif isinstance(a, Complex):
			raise ComputorException('Illegal operation: transp(Complex)')
		elif isinstance(a, Matrix):
			return a.get_transpose()
		raise ComputorException('Computor.inv(): something bad happened 🤷')

	def sqrt(self, a):
		if isinstance(a, float):
			if a >= 0:
				return a ** 0.5
			else:
				return Complex(0, (-a) ** 0.5)
		elif isinstance(a, Complex):
			raise ComputorException('Illegal operation: sqrt(Complex)')
		elif isinstance(a, Matrix):
			raise ComputorException('Illegal operation: sqrt(Matrix)')
		raise ComputorException('Computor.sqrt(): something bad happened 🤷')

	def sin(self, radians):
		if isinstance(radians, float):
			return sin(radians)
		elif isinstance(radians, Complex):
			raise ComputorException('Illegal operation: sin(Complex)')
		elif isinstance(radians, Matrix):
			raise ComputorException('Illegal operation: sin(Matrix)')
		raise ComputorException('Computor.sin(): something bad happened 🤷')

	def cos(self, radians):
		if isinstance(radians, float):
			return cos(radians)
		elif isinstance(radians, Complex):
			raise ComputorException('Illegal operation: cos(Complex)')
		elif isinstance(radians, Matrix):
			raise ComputorException('Illegal operation: cos(Matrix)')
		raise ComputorException('Computor.cos(): something bad happened 🤷')

	def tan(self, radians):
		if isinstance(radians, float):
			return tan(radians)
		elif isinstance(radians, Complex):
			raise ComputorException('Illegal operation: tan(Complex)')
		elif isinstance(radians, Matrix):
			raise ComputorException('Illegal operation: tan(Matrix)')
		raise ComputorException('Computor.tan(): something bad happened 🤷')

	def deg(self, radians):
		if isinstance(radians, float):
			return radians * 180 / Computor.pi
		elif isinstance(radians, Complex):
			raise ComputorException('Illegal operation: deg(Complex)')
		elif isinstance(radians, Matrix):
			raise ComputorException('Illegal operation: deg(Matrix)')
		raise ComputorException('Computor.deg(): something bad happened 🤷')

	def rad(self, degrees):
		if isinstance(degrees, float):
			return degrees * Computor.pi / 180
		elif isinstance(degrees, Complex):
			raise ComputorException('Illegal operation: rad(Complex)')
		elif isinstance(degrees, Matrix):
			raise ComputorException('Illegal operation: rad(Matrix)')
		raise ComputorException('Computor.rad(): something bad happened 🤷')


