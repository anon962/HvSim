import weakref


class BuffList:
	def __init__(self, sim):
		self.sim= weakref.proxy(sim)
		self.buffs= []

	def __getitem__(self, item):
		for x in self.buffs:
			if x.name.lower() == item.lower():
				return x
		raise IndexError()

	def __iter__(self):
		yield from self.buffs

	def add(self, item):
		return self.buffs.append(item)

	def remove(self, item):
		return self.buffs.remove(item)

	def __contains__(self, item):
		return item.lower() in [x.name.lower() for x in self.buffs]

	def clear_expired(self):
		self.buffs= [x for x in self.buffs if not x.expired()]