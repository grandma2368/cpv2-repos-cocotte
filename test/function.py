from colorama import Fore, Back, Style

from exceptions import ComputorException

class Function:

	def __init__(self, name, local_vars, expr):
		self.name = name
		self.local_vars = local_vars
		if len(self.local_vars) != len(set(self.local_vars)):
			raise ComputorException('Function local variables repeated')
		self.expr = expr

	def __str__(self):
		return Style.BRIGHT + Fore.BLUE + self.name + \
			'(' + ', '.join(self.local_vars) + ')' + Fore.RESET + Style.RESET_ALL +\
			' = ' + self.expr



