from lark import Lark, Transformer, v_args
from colorama import Fore, Back, Style

from matrix import Matrix
from file_to_string import file_to_string
import computor

class Simplifier:

	@v_args(inline=True)	# Affects the signatures of the methods
	class MyTransformer(Transformer):

		def __init__(self):
			pass

		# TOP LEVEL STATEMENTS ------------------------------------

		def expr_to_str(self, expr):
			if isinstance(expr, str):
				return expr
			else:
				return computor.Computor.instance.compact_str(expr)

		# OPERATORS ------------------------------------

		def add(self, a, b):
			if (not isinstance(a, str)) and (not isinstance(b, str)):
				return computor.Computor.instance.add(a, b)
			else:
				return computor.Computor.instance.compact_str(a) + ' + ' + computor.Computor.instance.compact_str(b)

		def sub(self, a, b):
			if (not isinstance(a, str)) and (not isinstance(b, str)):
				return computor.Computor.instance.sub(a, b)
			else:
				return computor.Computor.instance.compact_str(a) + ' - ' + computor.Computor.instance.compact_str(b)

		def mat_mul(self, a, b):
			if (not isinstance(a, str)) and (not isinstance(b, str)):
				return computor.Computor.instance.mat_mul(a, b)
			else:
				return computor.Computor.instance.compact_str(a) + ' ** ' + computor.Computor.instance.compact_str(b)

		def mul(self, a, b):
			if (not isinstance(a, str)) and (not isinstance(b, str)):
				return computor.Computor.instance.mul(a, b)
			else:
				return computor.Computor.instance.compact_str(a) + ' * ' + computor.Computor.instance.compact_str(b)

		def div(self, a, b):
			if (not isinstance(a, str)) and (not isinstance(b, str)):
				return computor.Computor.instance.div(a, b)
			else:
				return computor.Computor.instance.compact_str(a) + ' / ' + computor.Computor.instance.compact_str(b)

		def mod(self, a, b):
			if (not isinstance(a, str)) and (not isinstance(b, str)):
				return computor.Computor.instance.mod(a, b)
			else:
				return computor.Computor.instance.compact_str(a) + ' % ' + computor.Computor.instance.compact_str(b)

		def pow(self, base, power):
			if (not isinstance(base, str)) and (not isinstance(power, str)):
				return computor.Computor.instance.pow(base, power)
			else:
				return computor.Computor.instance.compact_str(base) + '^' + computor.Computor.instance.compact_str(power)

		def neg(self, a):
			if not isinstance(a, str):
				return computor.Computor.instance.neg(a)
			else:
				return '-' + computor.Computor.instance.compact_str(a)

		# PARSE FOR VALUE ------------------------------------

		def parse_number(self, token):
			return float(token.value)

		def parse_neg_number(self, token):
			return -float(token.value)

		def resolve_var(self, var_name):
			return computor.Computor.instance.resolve_var(var_name)

		def imag(self):
			return computor.Computor.imag

		def pi(self):
			return computor.Computor.pi

		def parentheses_expr(self, expr):
			if isinstance(expr, str):
				return '(' + expr + ')'
			else:
				return expr

		def eval_func(self, func_name, *args):
			# check if this func_name with this many args exists
			computor.Computor.instance.validate_func(func_name, len(args))
			# if any arg is string
			if any(map(lambda x: isinstance(x, str), args)):
				return func_name + '(' + ', '.join(map(lambda x: computor.Computor.instance.compact_str(x), args)) + ')'
			else:
				return computor.Computor.instance.eval_function(func_name, args)				

		# BUILT-IN FUNCTIONS ------------------------------------

		def eval_built_in(self, func_tuple, arg):
			func = func_tuple[0]
			func_str = func_tuple[1]
			if isinstance(arg, str):
				return func_str + '(' + arg + ')'
			else:
				return func(arg)

		def inv(self):
			return computor.Computor.instance.inv, 'inv'

		def transp(self):
			return computor.Computor.instance.transp, 'transp'

		def sqrt(self):
			return computor.Computor.instance.sqrt, 'sqrt'

		def sin(self):
			return computor.Computor.instance.sin, 'sin'

		def cos(self):
			return computor.Computor.instance.cos, 'cos'

		def tan(self):
			return computor.Computor.instance.tan, 'tan'

		def deg(self):
			return computor.Computor.instance.deg, 'deg'

		def rad(self):
			return computor.Computor.instance.rad, 'rad'

		# MATRIX CONSTRUCTION ------------------------------------

		def get_matrix(self, *rows):
			return Matrix(rows)

		def get_mat_rows(self, *elements):
			return elements

	def __init__(self):
		grammar = file_to_string('grammars/simplifier.lark')
		self.__lark_parser = Lark(grammar, parser='lalr', transformer=Simplifier.MyTransformer())

	def simplify(self, statement):
		return self.__lark_parser.parse(statement)

