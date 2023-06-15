import weakref
from .monster import Monster


class MonsterList:
	def __init__(self, sim, n):
		self.sim= weakref.proxy(sim)
		self.mobs= [Monster(sim=sim, name="test") for i in range(n)]

	def index(self, x):
		return self.mobs.index(x)

	def __iter__(self):
		for x in self.mobs:
			yield x

	def __getitem__(self, i):
		return self.mobs[i]