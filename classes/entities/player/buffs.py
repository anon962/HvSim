from ...buff import Buff


class Regen(Buff):
	def on_tick(self):
		self.entity['hp']+= 0.2*self.entity['hp'].base

	def on_apply(self):
		self.on_tick()

	def on_expire(self):
		pass