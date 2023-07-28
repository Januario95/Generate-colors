class Fraction:
	def __init__(self, nume, deno):
		self.nume = nume
		self.deno = deno

	def __str__(self):
		return f'{self.nume}/{self.deno}'

	def __add__(self, other_func):
		new_nume = self.nume * other_func.deno + other_func.nume * self.deno
		new_demo = self.deno * other_func.deno
		return Fraction(new_nume, new_demo)

	def __mul__(self, other_func):
		new_nume = self.nume * other_func.nume
		new_demo = self.deno * other_func.deno
		return Fraction(new_nume, new_demo)

	def __sub__(self, other_func):
		new_nume = self.nume * other_func.deno - other_func.nume * self.deno
		new_demo = self.deno * other_func.deno
		return Fraction(new_nume, new_demo)

	def __truediv__(self, other_func):
		other_func = Fraction(other_func.deno, other_func.nume)
		return self.__mul__(other_func)










