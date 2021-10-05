from lark import Lark, Transformer, v_args
from lark.exceptions import LarkError
from colorama import Fore, Back, Style

from function import Function
from term import Term
from file_to_string import file_to_string
from exceptions import ParserException, ComputorException
import computor

class Solver:

	@v_args(inline=True)	# Affects the signatures of the methods
	class MyTransformer(Transformer):

		def __init__(self, solver):
			self.__solver = solver

		def get_lhs_rhs(self, lhs, rhs):
			return lhs, rhs

		# build a term from var
		def build_term_var(self, var_name):
			value = computor.Computor.instance.get_var(var_name)
			if not isinstance(value, float):
				raise ComputorException('Variables must be rational')
			return [ Term(value, 0) ]

		# build terms from a function
		def build_terms_from_func_expr(self, func, _):
			return self.__solver.parse_func(func.expr)

		def add(self, a, b):
			return a + b

		def sub(self, a, b):
			b[0].coef = -b[0].coef
			return a + b

		def neg(self, terms):
			terms[0].coef *= -1
			return terms

		# coef only -> c * X^0
		def build_term_c_0(self, number_token):
			coef = float(number_token.value)
			return [ Term(coef, 0) ]

		def mul_number_thing(self, number_token, terms):
			number = float(number_token.value)
			terms[0].coef *= number
			return terms

		def build_term_deg(self, _, degree=None):
			if degree is None:
				return [ Term(1.0, 1) ]
			else:
				return [ Term(1.0, degree) ]

		def parse_degree(self, token):
			value = float(token.value)
			if value.is_integer():
				value = int(value)
				if 0 <= value <= 2:
					return value
			raise ParserException('Exponent ' + Fore.RED + str(value) + Fore.RESET + ' must be 0, 1, or 2')

		def parse_var(self, token):
			return token.value

		def parse_func(self, token):
			func_name = token.value
			function = computor.Computor.instance.get_func(func_name)
			if not (len(function.local_vars) == 1 and function.local_vars[0].upper() == 'X'):
				raise ComputorException('Invalid function: ' + str(function))
			return function


	def __init__(self):
		grammar = file_to_string('grammars/solver.lark')
		self.__lark_parser = Lark(grammar, parser='lalr', transformer=Solver.MyTransformer(self))
		self.__func_parser = Lark(grammar, parser='lalr', transformer=Solver.MyTransformer(self), start='expr')
		
	def parse_func(self, expr):
		return self.__func_parser.parse(expr)

	def solve(self, statement):
		lhs, rhs = self.__parse(statement)

		print(Style.BRIGHT + 'Given:' + Style.RESET_ALL)
		self.__print_equation(lhs, rhs)

		print(Style.BRIGHT + 'Group terms by degree:' + Style.RESET_ALL)
		self.__group_terms(lhs, rhs)
		self.__print_equation(lhs, rhs)

		print(Style.BRIGHT + 'Merge terms by degree:' + Style.RESET_ALL)
		lhs = self.__merge_terms(lhs)
		rhs = self.__merge_terms(rhs)
		self.__print_equation(lhs, rhs)

		print(Style.BRIGHT + 'Reduced form:' + Style.RESET_ALL)
		reduced_form = self.__get_reduced_form(lhs,rhs)
		self.__print_reduced_form(reduced_form)

		a = reduced_form[0].coef
		b = reduced_form[1].coef
		c = reduced_form[2].coef
		self.__solve_equation(a, b, c)

	def __parse(self, statement):
		try:
			lhs, rhs = self.__lark_parser.parse(statement)
			return lhs, rhs
		except LarkError as e:
			raise ParserException(e)

	def __group_terms(self, lhs, rhs):
		lhs.sort(key=lambda x: x.degree, reverse=True)
		rhs.sort(key=lambda x: x.degree, reverse=True)

	def __merge_terms(self, terms):
		merged_expr = [Term(0.0, 2), Term(0.0, 1), Term(0.0, 0)]
		for term in terms:
			if term.degree == 2:
				merged_expr[0].coef += term.coef
			if term.degree == 1:
				merged_expr[1].coef += term.coef
			if term.degree == 0:
				merged_expr[2].coef += term.coef
		return merged_expr

	def __get_reduced_form(self, lhs, rhs):
		lhs[0].coef -= rhs[0].coef
		lhs[1].coef -= rhs[1].coef
		lhs[2].coef -= rhs[2].coef
		return lhs

	def __print_equation(self, lhs, rhs):
		lhs_str = ' + '.join(map(str, lhs))
		rhs_str = ' + '.join(map(str, rhs))
		print(lhs_str + ' = ' + rhs_str)

	def __print_reduced_form(self, terms):
		reduced_str = ' + '.join(map(str, terms))
		print(reduced_str + ' = 0')

		# Print an even more reduced form
		super_reduced_form = [ term.get_super_reduced_str() for term in terms ]
		super_reduced_form = filter(lambda x: x != '', super_reduced_form)
		super_reduced_str = ' + '.join(map(str, super_reduced_form))
		if super_reduced_str == '':
			super_reduced_str = '0'
		print(super_reduced_str + ' = 0')

	def __solve_equation(self, a, b, c):
		if a == 0 and b == 0:
			print(Style.BRIGHT + 'Polynomial degree: 0' + Style.RESET_ALL)
			print(Style.BRIGHT + 'Solving equation with no X...' + Style.RESET_ALL)
			self.__solve_constant(a, b, c)
		elif a == 0:
			print(Style.BRIGHT + 'Polynomial degree: 1' + Style.RESET_ALL)
			print(Style.BRIGHT + 'Solving linear equation...' + Style.RESET_ALL)
			self.__solve_linear(a, b, c)
		else:
			print(Style.BRIGHT + 'Polynomial degree: 2' + Style.RESET_ALL)
			print(Style.BRIGHT + 'Solving quadratic equation...' + Style.RESET_ALL)
			self.__solve_quadratic(a, b, c)

	def __solve_constant(self, a, b, c):
		if c == 0:
			print(Style.BRIGHT + '    X =' + Style.RESET_ALL, 'All numbers!')
		else:
			print(Style.BRIGHT + '    X =' + Style.RESET_ALL, 'No solution!')

	def __solve_linear(self, a, b, c):
		x = -c / b
		print(Style.BRIGHT + '    X =' + Style.RESET_ALL, x)

	def __solve_quadratic(self, a, b, c):
		discriminant = b ** 2 - 4 * a * c
		print('Discriminant =', discriminant)

		# x0 = (-b + sqrt(discriminant)) / (2 * a)
		# x1 = (-b - sqrt(discriminant)) / (2 * a)
		x0 = computor.Computor.instance.div(computor.Computor.instance.add(-b, computor.Computor.instance.sqrt(discriminant)), 2 * a)
		x1 = computor.Computor.instance.div(computor.Computor.instance.sub(-b, computor.Computor.instance.sqrt(discriminant)), 2 * a)

		if discriminant < 0:
			print('  Discriminant < 0 : 2 complex solutions:')
			print(Style.BRIGHT + '    X0 =' + Style.RESET_ALL, x0)
			print(Style.BRIGHT + '    X1 =' + Style.RESET_ALL, x1)
		elif discriminant == 0:
			print('  Discriminant = 0 : 1 real solution:')
			print(Style.BRIGHT + '    X =' + Style.RESET_ALL, x0)
		else:
			print('  Discriminant > 0 : 2 real solutions:')
			print(Style.BRIGHT + '    X0 =' + Style.RESET_ALL, x0)
			print(Style.BRIGHT + '    X1 =' + Style.RESET_ALL, x1)














