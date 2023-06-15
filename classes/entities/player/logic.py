from .buffs import *

class PlayerLogic:
	def do_battle(self):
		mob_list= self.sim.mob_list
		alive= [x for x in mob_list if x.alive()]

		if "regen" not in self.buffs and "regen" not in self.cooldowns:
			return self.use("regen")

		return self.use("attack", alive[0])

