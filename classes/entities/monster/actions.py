from abc import abstractmethod
from utils.entity_utils import cooldown, action_time

class MonsterActions:
	@cooldown(0)
	@action_time(1)
	def attack(self, player):
		self.deal_damage(player)

	def skill_1(self, player):
		pass

	def skill_2(self, player):
		pass