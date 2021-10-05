from lark import Lark, Transformer, v_args
from lark.exceptions import LarkError
from colorama import Fore, Back, Style

from exceptions import ParserException
from file_to_string import file_to_string
import computor

class Parser:

	@v_args(inline=True)	# Affects the signatures of the methods
	class MyTransformer(Transformer):

		def __init__(self):
			pass

		# TOP LEVEL STATEMENTS ------------------------------------

		def eval_expr(self, expr, _=None):
			return computor.Computor.instance.eval(expr)

		def show_func(self, func_name, *args):
			if '?' in args[-1]:
				args = args[:-1]
			computor.Computor.instance.show_func(func_name, args)

		def define_var(self, var_name, expr):
			value = computor.Computor.instance.eval(expr)
			computor.Computor.instance.set_var(var_name, value)

		def define_func(self, func_name, *args):
			local_vars = args[0:-1]
			expr = args[-1]
			computor.Computor.instance.set_func(func_name, local_vars, expr)

		def show_vars(self):
			computor.Computor.instance.show_vars()

		def show_funcs(self):
			computor.Computor.instance.show_funcs()

		def dance(self):
			computor.Computor.instance.dance()

		def doge(self):
			computor.Computor.instance.doge()

		# OPERATORS ------------------------------------

		def add(self, a, b):
			return a + ' + ' + b

		def sub(self, a, b):
			return a + ' - ' + b

		def mat_mul(self, a, b):
			return a + ' ** ' + b

		def mul(self, a, b):
			return a + ' * ' + b

		def div(self, a, b):
			return a + ' / ' + b

		def mod(self, a, b):
			return a + ' % ' + b

		def pow(self, base, power):
			return base + '^' + power

		def neg(self, a):
			return '-' + a

		# PARSE FOR VALUE ------------------------------------

		def parse_number(self, token):
			return str(token.value)

		def parse_neg_number(self, token):
			return '-' + str(token.value)

		# [number] thing	-> 1 or 2 args
		def parse_number_mul_with_thing(self, *args):
			# case: thing
			if len(args) == 1:
				thing = args[0]
				return thing
			# case: number thing
			elif len(args) == 2:
				number = str(args[0].value)
				thing = args[1]
				return number + ' * ' + thing

		def imag(self):
			return 'i'

		def pi(self):
			return 'pi'

		def parentheses_expr(self, expr):
			return '(' + expr + ')'

		def eval_func(self, func_name, *args):
			return func_name + '(' + ','.join(args) + ')'

		# BUILT-IN FUNCTIONS ------------------------------------

		def eval_built_in(self, func_name, arg):
			return func_name + '(' + arg + ')'

		def inv(self):
			return 'inv'

		def transp(self):
			return 'transp'

		def sqrt(self):
			return 'sqrt'

		def sin(self):
			return 'sin'

		def cos(self):
			return 'cos'

		def tan(self):
			return 'tan'

		def deg(self):
			return 'deg'

		def rad(self):
			return 'rad'

		# MATRIX CONSTRUCTION ------------------------------------

		def get_matrix(self, *rows):
			return '[' + ';'.join(rows) + ']'

		def get_mat_rows(self, *elements):
			return '[' + ','.join(map(str, elements)) + ']'

		# NAME VALIDATION ------------------------------------			

		def parse_name(self, token):
			reserved = ['i', 'pi', 'inv', 'transp', 'sqrt', 'sin', 'cos', 'tan']
			name = token.value
			if name.lower() in reserved:
				raise ParserException('Cannot use \'' + Fore.BLUE + name + Fore.RESET + '\' as variable or function name')
			return name

	def __init__(self):
		grammar = file_to_string('grammars/parser.lark')
		self.__lark_parser = Lark(grammar, parser='lalr', transformer=Parser.MyTransformer())

	def parse(self, statement):
		try:
			statement = self.__preprocess(statement)
			return self.__lark_parser.parse(statement)
		except LarkError as e:
			raise ParserException(e)

	# Prepend 'def' in a function definition statement, to help LALR(1) parser distinguish this statement
	def __preprocess(self, statement):
		if '=' in statement and not '?' in statement:
			lhs = statement.split('=')[0]
			if '(' in lhs and ')' in lhs:
				statement = 'def ' + statement
		return statement

