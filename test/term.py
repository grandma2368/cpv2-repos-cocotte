from colorama import Fore, Back, Style

class Term:

	def __init__(self, coef, degree):
		self.coef = coef
		self.degree = degree

	def __str__(self):
		buffer = ''

		if self.degree == 0:
			buffer += Fore.RED
		elif self.degree == 1:
			buffer += Fore.GREEN
		elif self.degree == 2:
			buffer += Fore.BLUE
		else:
			buffer += Fore.MAGENTA

		buffer += str(self.coef) + ' * X^' + str(self.degree)
		buffer += Fore.RESET
		return buffer

	#					X^0				X^1				X^2
	# coef = 0			''				''				''
	# coef = 1			1.0				X				X^2
	# coef = c			c				c * X			c * X^2		
	def get_super_reduced_str(self):
		if self.coef == 0:
			return ''

		buffer = ''
		if self.degree == 0:
			buffer += Fore.RED
		elif self.degree == 1:
			buffer += Fore.GREEN
		elif self.degree == 2:
			buffer += Fore.BLUE
		else:
			buffer += Fore.CYAN

		if self.coef == 1.0:
			if self.degree == 0:
				buffer += '1.0'
			elif self.degree == 1:
				buffer += 'X'
			else:
				buffer += 'X^2'
		else:
			if self.degree == 0:
				buffer += str(self.coef)
			elif self.degree == 1:
				buffer += str(self.coef) + ' * X'
			else:
				buffer += str(self.coef) + ' * X^2'

		buffer += Fore.RESET
		return buffer

