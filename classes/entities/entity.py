from ..logger import Logger
from ..buff_list import BuffList
from abc import ABC, abstractmethod
import weakref, random

class Entity(ABC, Logger):
	"""
	Interface for :class:`classes.Player` and :class:`classes.Monster`.

	Parameters
	----------
		sim: Simulator
			Simulator utilizing the entity.

	Attributes
	----------
	config: dict
		Dictionary loaded from config file containing default stat values.
	"""

	def __init__(self, sim, loger_name):
		self.sim= weakref.proxy(sim)
		self.cooldowns= {}
		self.buffs= BuffList(sim)
		self.stats= {}
		self.next_action_time= 0

		super().__init__(loger_name)

		self.reset()

	def reset(self) -> None:
		"""
		Reinitializes stats using config file.
		"""
		# set numerical stats
		for x,y in self.config['init'].items():
			self[x]= y

		# convert certain stats to [current, max, ratio] list
		for x in ['hp']:
			self[x]= VitalStat(entity=self, name="hp", max=self[x])

	def alive(self) -> bool:
		"""
		Checks if remaining HP is greater than zero.
		"""
		return self['hp'][0] > 0

	def use(self, action_name, target=None):
		"""Performs an action.

		Parameters
		----------
		target: Entity
			Target entity.
		action_name: str
			Name of action.

		Returns
		-------
		None
			Thingy

		"""
		# inits
		action= getattr(self, action_name)
		self.info(self.render_template("use_template", user=self, action=action_name, target=target))

		# do action
		if target:
			action(target)
		else:
			action()

	@abstractmethod
	def do_battle(self) -> dict:
		"""
		Select and perform an action. Implementations should increment :attr:`Entity.next_action_time`.

		:return: :class:`dict` containing action taken and action time. For example::

			{ action: "attack", action_time: 1.0 }
		"""
		...

	def deal_damage(self, target, mult=1):
		from classes.entities.player import Player

		# base damage
		damage= mult*self['attack']

		# accuracy roll
		if random.random() > self['accuracy']:
			self.info(self.render_template("target_miss", dealer=self, target=target))
			return

		# evasion roll
		if random.random() < target['evade']:
			self.info(self.render_template("target_evade", dealer=self, target=target))
			return

		# crit roll
		if random.random() < self['crit_chance']:
			self.info(self.render_template("target_crit", dealer=self, target=target))
			damage*= self['crit_mult']

		# apply mits
		damage*= 1-target['mitigation']

		# resist roll
		count= 0
		if isinstance(self, Player):
			eff_resist= target['resist'] * (1-self['counter_resist'])

			for i in range(3):
				if random.random() < eff_resist:
					count+= 1

		r_mult= [0, 0.5, 0.75, 0.9][count]
		if r_mult > 0:
			self.info(self.render_template("target_resist", dealer=self, target=target, mult=r_mult))

		damage*= 1-r_mult

		# done
		target['hp']-= damage
		return

	def natural_regen(self):
		for x in ['hp']:
			self[x]+= self[x + '_regen']
		return

	def __lt__(self, other):
		return self.next_action_time < other.next_action_time

	def __getitem__(self, stat_name):
		return self.stats[stat_name]

	def __setitem__(self, stat_name, value):
		if stat_name in self.stats and \
			isinstance(value, VitalStat) and \
			value.entity is None:
				self.stats[stat_name].current= value.current
		else:
			self.stats[stat_name]= value

	def __str__(self):
		from classes import Player, Monster

		if isinstance(self, Player):
			return f"Player"
		elif isinstance(self, Monster):
			return f"Monster {self.index()}"
		else:
			return "Entity"

class VitalStat:
	def __init__(self, name, max, entity=None, current=None, bonus=0):
		self.entity= entity
		self.name= name

		self.base= max
		self.bonus= bonus
		self.max= (1+bonus)*self.base if self.base else None
		self._current= self.max if current is None else current
		self.ratio= 1

	@property
	def current(self):
		return self._current

	@current.setter
	def current(self, value):
		if self._current - value != 0 and self.entity:
			self.entity.info(self.entity.render_template("vital_change", vital=self, value=value), tags=self.name)

		self._current= value
		self.ratio= self._current / self.max

		if self._current <= 0 and self.entity:
			self.entity.info(self.entity.render_template("death", SELF=self.entity))

	def __getitem__(self, i):
		if i == 0:
			return self._current
		elif i == 1:
			return self.max
		else:
			return self.ratio

	def __setitem__(self, i, value):
		if i == 0:
			self.current= value
		elif i == 1:
			self.max= value
		elif i == 2:
			self.ratio= value
		else:
			raise IndexError

	def __sub__(self, other):
		val= self._current
		if isinstance(other, (float,int)):
			val-= other
		else:
			val-= other._current

		return VitalStat(name=None, max=None, entity=None, current=int(val))

	def __add__(self, other):
		val= self._current
		if isinstance(other, (float,int)):
			val+= other
		else:
			val+= other._current

		val= min(max(val,0), self.max)
		return VitalStat(name=None, max=None, entity=None, current=int(val))