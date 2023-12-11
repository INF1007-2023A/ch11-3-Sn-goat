"""
Chapitre 11.2
"""


import numbers
import copy


class DimensionsTypeError(TypeError):
	pass

class DimensionsError(ValueError):
	pass

class IncompatibleOperandsError(DimensionsError):
	pass

class DataTypeError(TypeError):
	pass

class DataSizeError(ValueError):
	pass


class Matrix:
	"""
	Matrice numérique réelle stockée en tableau 1D en format rangée-major.

	:param height: La hauteur (nb de rangées)
	:param width: La largeur (nb de colonnes)
	:param data: Si une liste, alors les données elles-mêmes (`data` affectée, pas copiée). Si un nombre, alors la valeur de remplissage
	"""

	def __init__(self, height, width, data = 0.0):
		if not isinstance(height, numbers.Integral) or not isinstance(width, numbers.Integral):
			raise DimensionsTypeError("Height and width of Matrix argument must be int")
		if height <= 0 or width <= 0:
			raise DimensionsError(f"height={height} and width={width} are not > 0")
		self.__height = height
		self.__width = width
		
		if isinstance(data, list):
			if len(data) != len(self):
				raise DataSizeError(f"Data length is {len(data)}, must be {len(self)}")
			self.__data = data
		elif isinstance(data, numbers.Number):
			self.__data = [data for _ in range(len(self))]
		else:
			raise DataTypeError("Data argument must be number or list")

	@property
	def height(self):
		return self.__height

	@property
	def width(self):
		return self.__width

	@property
	def data(self):
		return self.__data

	# TODO: Accès à un élément en lecture
	def __getitem__(self, indexes):
		"""
		Indexation rangée-major

		:param indexes: Les index en `tuple` (rangée, colonne)
		"""

		self._check_indexes(indexes)
		index = indexes[0]*self.width + indexes[1]
		# TODO: Retourner la valeur
		return self.data[index]

	# TODO: Affectation à un élément
	def __setitem__(self, indexes, value):
		"""
		Indexation rangée-major

		:param indexes: Les index en `tuple` (rangée, colonne)
		"""
		self._check_indexes(indexes)
		# TODO: L'affectation
		index = indexes[0]*self.width + indexes[1]
		self.data[index] = value


	def __len__(self):
		"""
		Nombre total d'éléments
		"""
		return self.height * self.width

	# TODO: Représentation affichable (conversion pour print)
	def __str__(self):
		# TODO: Chaque rangée est sur une ligne, avec chaque élément séparé d'un espace.
		matrix = self.copy()
		n=0
		for i in range(len(self)):
			if (i % matrix.width) == 0:
				matrix.data.insert(i+n, "\n")
				n+=1

		data_matrix = " ".join(map(str, matrix.data))

		return data_matrix

	# TODO: Représentation officielle
	def __repr__(self):
		return f"Matrix({self.height}, {self.width}, {self.data})"

	# TODO: String formatée
	def __format__(self, format):
		# TODO: On veut pouvoir dir comment chaque élément doit être formaté en passant la spécification de formatage qu'on passerait à `format()`
		new_data = [f"{num:{format}}" for num in self.data]
		return str(Matrix(self.height, self.width, new_data))

	def clone(self):
		return Matrix(self.height, self.width, self.data)

	def copy(self):
		return Matrix(self.height, self.width, copy.deepcopy(self.data))

	def has_same_dimensions(self, other):
		if not isinstance(other, Matrix):
			raise TypeError(type(other))
		return (self.height, self.width) == (other.height, other.width)
	
	def _check_indexes(self, indexes):
		if not isinstance(indexes, tuple) and len(indexes) == 2:
			raise IndexError(f"{indexes} is not tuple of two elements")
		if indexes[0] >= self.height or indexes[1] >= self.width:
			raise IndexError(f"{indexes} is not within (height={self.height}, width={self.width})")

	def __pos__(self):
		return self.copy()

	# TODO: Négation
	def __neg__(self):
		new_data = list(map(lambda x: -x, self.data))
		return Matrix(self.height, self.width, new_data)

	# TODO: Addition
	def __add__(self, other):
		if isinstance(other, Matrix):

			if (self.width == other.width) and (self.height == other.height):
				new_data = list(map(lambda x,y : x + y, self.data, other.data))
			else:
				raise IncompatibleOperandsError(f"{other.height}, {other.width}")
		else:
			raise TypeError(type(other))
		# TODO: D'abord vérifier que les opérandes ont les mêmes dimensions. Sinon, on lève un IncompatibleOperandsError.
		# TODO: Retourner le résultat de l'addition
		return Matrix(self.height, self.width, new_data)
	
	# TODO: Soustraction (n'oubliez pas qu'on a déjà l'opérateur de négation et d'addition)
	def __sub__(self, other):
		return self + (-other)
	
	# TODO: Multiplication matricielle/scalaire
	def __mul__(self, other):
		if isinstance(other, Matrix):
			# TODO: D'abord vérifier que les opérandes on des dimensions compatibles. Sinon on lève un IncompatibleOperandsError.
			if self.width == other.height:
			# TODO: Multiplication matricielle.
				C = Matrix(self.height, other.width)
			# Pour i dans [0, hauteur_C[
				# Pour j dans [0, largeur_C[
					# Pour k dans [0, largeur_A[
						# C(i, j) = A(i, k) * B(k, j)
				for i in range(C.height):
					for j in range(C.width):
						for k in range(self.width):
							C[i,j] += self[i,k] * other[k,j]
				return C
							

		elif isinstance(other, numbers.Number):
			# TODO: Multiplication scalaire.
			new_data = list(map(lambda x: x * other, self.data))
			return Matrix(self.height, self.width, new_data)

		else:
			raise TypeError(type(other))

	# TODO: Multiplication scalaire avec le scalaire à gauche
	def __rmul__(self, other):
		if isinstance(other, numbers.Number):
			# TODO: Multiplication scalaire.
			new_data = list(map(lambda x: x * other, self.data))
			return Matrix(self.height, self.width, new_data)

		else:
			raise TypeError(type(other))

	def __abs__(self):
		return Matrix(self.height, self.width, [abs(e) for e in self.data])

	# TODO: Égalité entre deux matrices

	# TODO: Méthode de classe identity qui crée une matrice identité
