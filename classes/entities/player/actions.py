from utils.entity_utils import cooldown, action_time
from .buffs import *


class PlayerActions:
	@cooldown(0)
	@action_time(1)
	def attack(self, monster):
		self.deal_damage(monster)

	@cooldown(5)
	@action_time(1)
	def regen(self):
		self.buffs.add(Regen(self))