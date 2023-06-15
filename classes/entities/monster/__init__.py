import utils
from classes.entities.entity import Entity
from .actions import MonsterActions
from .logic import MonsterLogic


class Monster(MonsterLogic, MonsterActions, Entity):
	def __init__(self, sim, name):
		self.config= utils.load_yaml(utils.MOB_CONFIG)[name]
		super().__init__(sim=sim, loger_name=__name__)

		self.append_tag("monster")

	def use(self, action_name, target=None):
		if target is None:
			target= self.sim.player
		return super().use(action_name=action_name, target=target)

	def index(self):
		return self.sim.mob_list.index(self)