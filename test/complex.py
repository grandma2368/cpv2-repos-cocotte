from exceptions import ComputorException

class Complex:

	@staticmethod
	def add(a, b):
		return Complex(a.real + b.real, a.imag + b.imag)

	@staticmethod
	def sub(a, b):
		return Complex(a.real - b.real, a.imag - b.imag)

	# (a + bi) * (c + di) = (ac - bd, (ad + bc)i)
	@staticmethod
	def mul(a, b):
		return Complex(a.real * b.real - a.imag * b.imag, a.real * b.imag + a.imag * b.real)

	# (a + bi) / (c + di) = (a + bi) / (c + di) * (c - di) / (c - di)
	@staticmethod
	def div(a, b):
		if b.__is_zero():
			raise ComputorException('Division by zero')
		conjugate = b.__get_conjugate()
		numerator = Complex.mul(a, conjugate)
		denominator = Complex.mul(b, conjugate)
		assert denominator.imag == 0.0
		return Complex(numerator.real / denominator.real, numerator.imag / denominator.real)

	# Pre-condition: power is a non-negative integer
	@staticmethod
	def pow(base, power):
		product = Complex(1.0, 0.0)
		for _ in range(power):
			product = Complex.mul(product, base)
		return product

	@staticmethod
	def neg(a):
		return Complex(-a.real, -a.imag)

	def __init__(self, real, imag=0.0):
		self.real = real
		self.imag = imag

	def __str__(self):
		if self.real == 0.0:
			return str(self.imag) + "i"
		else:
			return str(self.real) + " + " + str(self.imag) + "i"

	def __is_zero(self):
		return self.real == 0.0 and self.imag == 0.0

	def __get_conjugate(self):
		return Complex(self.real, -self.imag)

