import utils
from classes.entities.entity import Entity
from .actions import PlayerActions
from .logic import PlayerLogic


class Player(PlayerLogic, PlayerActions, Entity):
	def __init__(self, sim, loadout=None, style=None):
		loadout= loadout if loadout else "default"
		self.config= utils.load_yaml(utils.PLAYER_CONFIG)[loadout]
		super().__init__(sim=sim, loger_name=__name__)

		if style is None:
			style= ["imperil"]

		self.style= style
		self.append_tag("player")