from lark import Lark, Transformer, v_args
from colorama import Fore, Back, Style

from matrix import Matrix
from file_to_string import file_to_string
import computor

class Evaluator:

	@v_args(inline=True)	# Affects the signatures of the methods
	class MyTransformer(Transformer):

		def __init__(self):
			pass

		# OPERATORS ------------------------------------

		def add(self, a, b):
			return computor.Computor.instance.add(a, b)

		def sub(self, a, b):
			return computor.Computor.instance.sub(a, b)

		def mat_mul(self, a, b):
			return computor.Computor.instance.mat_mul(a, b)

		def mul(self, a, b):
			return computor.Computor.instance.mul(a, b)

		def div(self, a, b):
			return computor.Computor.instance.div(a, b)

		def mod(self, a, b):
			return computor.Computor.instance.mod(a, b)

		def pow(self, base, power):
			return computor.Computor.instance.pow(base, power)

		def neg(self, a):
			return computor.Computor.instance.neg(a)

		# PARSE FOR VALUE ------------------------------------

		def parse_number(self, token):
			return float(token.value)

		def parse_neg_number(self, token):
			return -float(token.value)

		def get_var_value(self, var_name):
			return computor.Computor.instance.get_var(var_name)

		def parse_number_imag(self, number_token=None):
			if number_token is None:
				return computor.Computor.imag
			else:
				number = float(number_token.value)
				return computor.Computor.instance.mul(number, computor.Computor.imag)

		def pi(self):
			return computor.Computor.pi

		def eval_func(self, func_name, *args):
			return computor.Computor.instance.eval_function(func_name, args)				

		# BUILT-IN FUNCTIONS ------------------------------------

		def eval_built_in(self, func, arg):
			return func(arg)

		def inv(self):
			return computor.Computor.instance.inv

		def transp(self):
			return computor.Computor.instance.transp

		def sqrt(self):
			return computor.Computor.instance.sqrt

		def sin(self):
			return computor.Computor.instance.sin

		def cos(self):
			return computor.Computor.instance.cos

		def tan(self):
			return computor.Computor.instance.tan

		def deg(self):
			return computor.Computor.instance.deg

		def rad(self):
			return computor.Computor.instance.rad

		# MATRIX CONSTRUCTION ------------------------------------

		def get_matrix(self, *rows):
			return Matrix(rows)

		def get_mat_rows(self, *elements):
			return elements

	def __init__(self):
		grammar = file_to_string('grammars/evaluator.lark')
		self.__lark_parser = Lark(grammar, parser='lalr', transformer=Evaluator.MyTransformer())

	def eval(self, statement):
		return self.__lark_parser.parse(statement)

