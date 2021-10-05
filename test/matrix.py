from exceptions import ComputorException

class Matrix:

	@staticmethod
	def add(a, b):
		if a.shape != b.shape:
			raise ComputorException('Invalid Matrix shapes: M' + str(a.shape) + ' + M' + str(b.shape))
		data = []
		for i in range(a.shape[0]):
			data.append(list(map(lambda x, y: x + y, a.data[i], b.data[i])))
		return Matrix(data)

	@staticmethod
	def sub(a, b):
		if a.shape != b.shape:
			raise ComputorException('Invalid Matrix shapes: M' + str(a.shape) + ' - M' + str(b.shape))
		data = []
		for i in range(a.shape[0]):
			data.append(list(map(lambda x, y: x - y, a.data[i], b.data[i])))
		return Matrix(data)

	@staticmethod
	def mat_mul(a, b):
		if a.shape[1] != b.shape[0]:
			raise ComputorException('Invalid Matrix shapes: M' + str(a.shape) + ' ** M' + str(b.shape))
		data = []
		for i in range(a.shape[0]):
			data.append( [None] * b.shape[1] )
			for j in range(b.shape[1]):
				data[i][j] = sum([ a.data[i][k] * b.data[k][j] for k in range(a.shape[1]) ])
		return Matrix(data)

	@staticmethod
	def element_mul(a, b):
		if a.shape != b.shape:
			raise ComputorException('Invalid Matrix shapes: M' + str(a.shape) + ' * M' + str(b.shape))
		data = []
		for i in range(a.shape[0]):
			data.append(list(map(lambda x, y: x * y, a.data[i], b.data[i])))
		return Matrix(data)

	@staticmethod
	def scalar_mul(scalar, matrix):
		data = []
		for i in range(matrix.shape[0]):
			data.append(list(map(lambda x: scalar * x, matrix.data[i])))
		return Matrix(data)
	
	@staticmethod
	def div(a, b):
		b_inv = b.get_inverse()
		return Matrix.mat_mul(a, b_inv)

	# Pre-condition: power is a non-negative integer
	@staticmethod
	def pow(base, power):
		if base.shape[0] != base.shape[1]:
			raise ComputorException('Invalid Matrix shape: M' + str(base.shape) + ' ^ ' + str(power))
		product = Matrix.__identity(base.shape[0])
		for _ in range(power):
			product = Matrix.mat_mul(product, base)
		return product

	@staticmethod
	def neg(a):
		return Matrix.scalar_mul(-1, a)

	@staticmethod
	def __identity(width):
		data = []
		for i in range(width):
			data.append([ 1.0 if j == i else 0.0 for j in range(width) ])
		return Matrix(data)

	# data is tuple of tuples, or list of lists, where each element is a float
	# Precondition: grammar/parser guarantees at least 1 element in each container
	def __init__(self, data):
		rows = len(data)
		cols = len(data[0])
		self.shape = (rows, cols)
		self.data = data
		for row in self.data:
			if len(row) != cols:
				raise ComputorException('Invalid matrix shape')

	def __str__(self):
		row_strs = [ '[ ' + ' , '.join(map(str, row)) + ' ]' for row in self.data ]
		return '\n'.join(row_strs)

	def get_compact_str(self):
		row_strs = [ '[' + ','.join(map(str, row)) + ']' for row in self.data ]
		return '[' + ';'.join(row_strs) + ']'

	def get_transpose(self):
		data = list(map(list,zip(*self.data)))
		return Matrix(data)

	def get_inverse(self):
		# Check if it is square matrix
		if self.shape[0] != self.shape[1]:
			raise ComputorException('M' + str(self.shape) + ' is not invertible')
		
		# 1 x 1 Matrix
		if self.shape[0] == 1:
			if self.data[0][0] == 0:
				raise ComputorException('Matrix is singular')
			else:
				data = [[ 1 / self.data[0][0] ]]
				return Matrix(data)
		
		# Check determinant
		determinant = self.__get_determinant()
		if determinant == 0:
			raise ComputorException('Matrix is singular')
		
		# 2 x 2 Matrix
		# inv = 1/determinant * [[d, -b], [-c, a]]
		if self.shape[0] == 2:
			data = [[ 1 / determinant * self.data[1][1], -1 / determinant * self.data[0][1] ],
				[ -1 / determinant * self.data[1][0], 1 / determinant * self.data[0][0] ]]
			return Matrix(data)

		# 3 x 3 or Bigger Matrix
		cofactors = []
		for r in range(self.shape[0]):
			cofactor_row = []
			for c in range(self.shape[0]):
				minor = self.__get_minor(r, c)
				cofactor_row.append( ((-1)**(r+c)) * minor.__get_determinant() )
			cofactors.append(cofactor_row)
		inv = Matrix(cofactors).get_transpose()
		for r in range(inv.shape[0]):
			for c in range(inv.shape[0]):
				inv.data[r][c] /= determinant
		return inv

	def __get_minor(self, r, c):
		data = [ row[:c] + row[c+1:] for row in (self.data[:r] + self.data[r+1:]) ]
		return Matrix(data)
	
	def __get_determinant(self):
		# Base case: 2 x 2 Matrix
		# determinant = ad - bc
		if self.shape[0] == 2:
			return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
		# Recursive case:
		determinant = 0
		for c in range(self.shape[0]):
			minor = self.__get_minor(0, c)
			determinant += ((-1) ** c) * self.data[0][c] * minor.__get_determinant()
		return determinant

